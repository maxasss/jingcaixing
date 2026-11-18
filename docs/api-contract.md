# 接口契约

- `GET /api/attractions`：景点列表。
- `GET /api/attractions/{id}`：景点详情。
- `POST /api/plans/generate`：行程生成；`AI_PROVIDER=mock` 时使用本地规则，`AI_PROVIDER=qwen` 时调用 Qwen。
- `POST /api/plans/edit/add`、`/delete`：行程编辑。
- `POST /api/routes/query`：高德 Web 服务路线与交通文本；配置 `JCX_MAP_PROVIDER=mock` 时可切回本地 Mock。
- `GET/POST/PUT/DELETE /api/admin/attractions`：本机管理员端景点资料维护接口；当前未接入登录，禁止部署到公网。
