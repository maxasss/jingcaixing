# 详细设计

当前使用 MySQL 保存景点资料；行程仅保存在浏览器 sessionStorage。后端按 API、Service、Repository、Model 分层，前端按 View、Component、API、Store、Utils 分层。AI 规划可通过 `AI_PROVIDER` 在本地 Mock 与 Qwen 间切换，路线服务暂为本地 Mock。
