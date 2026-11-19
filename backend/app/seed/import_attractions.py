"""从 database/attractions.xlsx 导入京彩行 MySQL attractions 表。

在项目根目录运行:
    python -m pip install openpyxl
    python backend/app/seed/import_attractions.py --check-only
    python backend/app/seed/import_attractions.py
"""
import argparse
import re
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[3]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

COLUMNS = (
    "attraction_id", "name", "category", "description", "duration",
    "opening_hours", "latitude", "longitude", "image_file",
)
CATEGORIES = {"历史人文", "自然风光", "美食探店"}
IMAGE_DIR = ROOT / "static" / "images" / "attractions"
DEFAULT_XLSX = ROOT / "database" / "attractions.xlsx"


def required_text(value, label, row):
    result = str(value).strip() if value is not None else ""
    if not result:
        raise ValueError(f"第 {row} 行：{label} 不能为空")
    return result


def positive_int(value, label, row):
    try:
        number = Decimal(str(value))
        if number != number.to_integral_value() or number <= 0:
            raise ValueError
        return int(number)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"第 {row} 行：{label} 必须是正整数") from None


def coordinate(value, label, low, high, row):
    try:
        number = Decimal(str(value))
        if not number.is_finite() or not low <= number <= high:
            raise ValueError
        return number
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"第 {row} 行：{label} 不在有效范围内") from None


def load_rows(xlsx_path, strict_images=False):
    workbook = load_workbook(xlsx_path, read_only=True, data_only=True)
    try:
        sheet = workbook["景点数据"] if "景点数据" in workbook.sheetnames else workbook.active
        values = sheet.iter_rows(values_only=True)
        headers = [str(v).strip() if v is not None else "" for v in next(values)]
        missing = set(COLUMNS) - set(headers)
        if missing:
            raise ValueError(f"Excel 缺少列：{', '.join(sorted(missing))}")
        indices = {name: headers.index(name) for name in COLUMNS}
        results, seen, missing_images = [], set(), []
        for row_number, cells in enumerate(values, start=2):
            if not any(value is not None and str(value).strip() for value in cells):
                continue
            def cell(name):
                i = indices[name]
                return cells[i] if i < len(cells) else None
            attraction_id = positive_int(cell("attraction_id"), "attraction_id", row_number)
            if attraction_id in seen:
                raise ValueError(f"第 {row_number} 行：重复 attraction_id={attraction_id}")
            seen.add(attraction_id)
            category = required_text(cell("category"), "category", row_number)
            if category not in CATEGORIES:
                raise ValueError(f"第 {row_number} 行：不支持的分类 {category}")
            image_file = required_text(cell("image_file"), "image_file", row_number)
            if not re.fullmatch(rf"{attraction_id}_\d{{3}}\.png", image_file):
                raise ValueError(f"第 {row_number} 行：图片名应为 {attraction_id}_001.png 等格式")
            image_path = IMAGE_DIR / image_file
            if not image_path.is_file():
                missing_images.append(image_file)
            data = dict(
                attraction_id=attraction_id,
                name=required_text(cell("name"), "name", row_number),
                category=category,
                description=required_text(cell("description"), "description", row_number),
                duration=positive_int(cell("duration"), "duration", row_number),
                opening_hours=required_text(cell("opening_hours"), "opening_hours", row_number),
                latitude=coordinate(cell("latitude"), "latitude", Decimal("-90"), Decimal("90"), row_number),
                longitude=coordinate(cell("longitude"), "longitude", Decimal("-180"), Decimal("180"), row_number),
                image_path=f"/images/attractions/{image_file}",
            )
            if len(data["name"]) > 100 or len(data["opening_hours"]) > 100:
                raise ValueError(f"第 {row_number} 行：名称或开放时间超过数据库字段长度（100）")
            results.append(data)
        if not results:
            raise ValueError("Excel 中没有可导入的景点")
        if missing_images:
            print(f"警告：缺少 {len(missing_images)} 张图片：{', '.join(missing_images[:12])}"
                  + (" ..." if len(missing_images) > 12 else ""))
            if strict_images:
                raise ValueError("存在缺失图片，停止导入")
        return results
    finally:
        workbook.close()


def main():
    parser = argparse.ArgumentParser(description="导入北京景点 Excel 数据")
    parser.add_argument("--xlsx", type=Path, default=DEFAULT_XLSX, help="Excel 文件路径")
    parser.add_argument("--check-only", action="store_true", help="仅检查 Excel，不连接数据库")
    parser.add_argument("--strict-images", action="store_true", help="缺少图片时停止")
    args = parser.parse_args()
    if not args.xlsx.is_file():
        parser.error(f"找不到 Excel 文件：{args.xlsx}")
    try:
        rows = load_rows(args.xlsx, args.strict_images)
        print(f"已读取 {len(rows)} 条景点：{dict(Counter(r['category'] for r in rows))}")
        if args.check_only:
            print("检查通过（未修改数据库）。坐标系及景点真实性需人工核实。")
            return
        from sqlalchemy import select
        from app.core.database import SessionLocal
        from app.models.attraction import Attraction

        # 事务提交：任何一条失败则整体回滚；仅新增或更新 Excel 中的 ID，不删除其他数据
        with SessionLocal.begin() as session:
            ids = [row["attraction_id"] for row in rows]
            existing = {
                item.attraction_id: item
                for item in session.scalars(
                    select(Attraction).where(Attraction.attraction_id.in_(ids))
                )
            }
            added = updated = 0
            for row in rows:
                current = existing.get(row["attraction_id"])
                if current is None:
                    session.add(Attraction(**row))
                    added += 1
                else:
                    for key, value in row.items():
                        if key != "attraction_id":
                            setattr(current, key, value)
                    updated += 1
        print(f"导入成功：新增 {added} 条，更新 {updated} 条。")
    except Exception as exc:
        print(f"失败：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
