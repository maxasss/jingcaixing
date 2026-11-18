# 京彩行旅行智能规划系统

Vue 3 + FastAPI + MySQL 8.0。当前所有 AI 与路线能力使用本地 Mock，不需要真实 API Key。

## 本地启动

```bash
cp .env.example .env
docker compose up -d mysql
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

前端开发地址：`http://localhost:5173`；接口文档：`http://127.0.0.1:8000/docs`。
