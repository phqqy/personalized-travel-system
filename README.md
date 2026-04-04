# personalized-travel-system

个性化旅游系统

## 项目简介

个性化旅游系统是一个基于 **Flask + Vue 3** 全栈开发的旅游推荐与导航系统，旨在为用户提供个性化的旅游体验。系统支持景点推荐、路线规划、日记管理、地图导航等功能，帮助用户更好地规划和享受旅游过程。

## 架构演进 (2026-04)

### 本次重构亮点

1. **前端全面升级为 Vue 3**
   - 所有页面从原生 HTML/JS 迁移至 Vue 3 Composition API
   - 使用 `{$ $}` 自定义定界符解决与 Jinja2 模板的冲突
   - 后端新增 JSON API 支持，前后端通过 `fetch` 异步通信
   - 响应式状态管理，UI 实时更新无需刷新页面

2. **高德地图深度集成**
   - POI 地点搜索与标记交互选择
   - 三种交通方式路线规划：驾车 / 步行 / 骑行
   - URL 参数自动定位（`?spot=景点名`）
   - 地理编码自动更新搜索范围

3. **代码质量优化**
   - 日记 ID 改用自增计数器，彻底消除删除后 ID 冲突问题
   - 清理无效路由引用，确保所有注册路由均有对应模板

4. **MySQL 数据库架构预留**（骨架已就绪）
   - 新增 `models/` ORM 模型层（User / Diary 模型定义）
   - 新增 `db/` 数据库初始化层（SQLAlchemy 引擎 + 连接池配置）
   - `config/settings.py` 已包含 DATABASE_URL 等完整数据库配置
   - `backend/app.py` 已预留 `init_db()` 调用（注释形式）
   - 取消注释即可完成 Pickle → MySQL 的平滑迁移

### 核心改进历史

- **模块化分层架构**：装饰器层 → 路由层(Flask Blueprint) → 服务层 → 工具层
- **评分系统**：支持景点/美食/日记/名校的 1-5 星评分 + 文字评论 + 排行榜
- **高内聚低耦合**：每个模块职责单一，易于测试和扩展

## 功能特点

- **旅游推荐**：基于热度和评分排序的景点/美食/名校推荐
- **地图导航**：高德地图集成，支持 POI 搜索和多种路线规划
- **日记管理**：完整的 CRUD 操作，支持 JSON 导入导出
- **评分系统**：多维度 1-5 星评分和文字评论
- **用户认证**：安全的登录注册机制，Session 会话管理

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端框架** | Flask 2.x | Python Web 框架，Blueprint 模块化路由 |
| **前端框架** | Vue 3 (CDN) | Composition API，响应式数据绑定 |
| **模板引擎** | Jinja2 | 服务端渲染 HTML 模板 |
| **ORM 框架** | SQLAlchemy 2.x (预留) | Python 标准 ORM，支持 MySQL 连接池 |
| **数据库** | MySQL 8.x (预留) | 关系型数据库，替代 Pickle 文件存储 |
| **地图服务** | 高德地图 JS API 2.0 | POI 搜索 / 路线规划 / 地理编码 |
| **数据存储** | Pickle 文件 (当前) → MySQL (目标) | 当前使用 Pickle，架构已预留 MySQL 迁移路径 |
| **密码安全** | SHA256 哈希 | 密码加密存储 |
| **图标库** | Font Awesome 6.4 | UI 图标 |

> **关于 Redis 缓存**：当前阶段暂不引入。当用户量破万、推荐算法变复杂、或需要分布式部署时再考虑加入。

## 项目结构

```
personalized-travel-system/
├── main.py                     # 项目主入口
├── requirements.txt            # 后端依赖清单
├── 整体架构.md                  # 架构设计文档（含 MySQL ER 图、DDL、迁移路线图）
│
├── backend/                    # 后端核心
│   ├── app.py                 # Flask 应用工厂 + 蓝图注册中心 + DB 初始化预留
│   ├── decorators.py          # 装饰器（登录检查 @login_required）
│   └── routes/                # 路由模块（Flask Blueprint）
│       ├── main.py            # 页面路由（首页/推荐/日记/地图）
│       ├── auth.py            # 认证路由（登录/注册/退出 + JSON API）
│       ├── diary.py           # 日记 CRUD API（GET/POST/PUT/DELETE）
│       ├── recommend.py       # 推荐数据 API
│       └── rating.py          # 评分系统 API
│
├── config/                     # 配置管理
│   └── settings.py            # 系统配置（路径/密钥/端口/DATABASE_URL/连接池参数）
│
├── models/                     # 【新增】ORM 模型层（MySQL 预留）
│   ├── __init__.py
│   ├── user_model.py          # User 模型（users 表映射）
│   └── diary_model.py         # Diary 模型（diaries 表映射）
│
├── db/                         # 【新增】数据库初始化层（MySQL 预留）
│   ├── __init__.py
│   └── db.py                  # SQLAlchemy 实例 + init_db() 入口
│
├── services/                   # 业务逻辑层
│   ├── user_service.py        # 用户服务（当前: Pickle / 目标: ORM）
│   ├── diary_service.py       # 日记服务（当前: Pickle / 目标: ORM）
│   ├── rating_service.py      # 评分服务（评分操作/排行榜）
│   └── recommend_service.py   # 推荐服务（景点/美食/名校数据）
│
├── utils/                      # 工具层
│   ├── security.py            # 安全工具（SHA256 密码哈希）
│   └── storage.py             # 存储工具（Pickle 序列化读写，迁移后可废弃）
│
├── data/                       # 数据目录
│   ├── db/                    # Pickle 数据文件（迁移后可删除）
│   │   ├── user_data.pkl     # ~~用户信息库~~
│   │   └── diary_data.pkl    # ~~日记数据库~~
│   └── raw/                   # 原始 CSV 数据（spots / food / facilities）
│
├── cache/                      # 缓存目录（推荐算法中间结果）
│
└── web_app/                    # 前端应用（Vue 3，不受迁移影响）
    ├── static/                # 静态资源
    │   ├── css/main.css       # 全局样式
    │   └── images/            # 图片资源（景点/美食/背景图）
    └── templates/             # Vue 3 页面模板
        ├── index.html         # 首页
        ├── auth.html          # 登录/注册页面
        ├── recommend.html     # 旅游推荐页面（热门/评分切换）
        ├── diary.html         # 日记管理页面（CRUD + 导入导出）
        └── map.html           # 地图导航页面（高德地图集成）
```

### 核心模块说明

| 模块 | 主要职责 | 关键特性 |
| ---- | ------- | -------- |
| **认证系统** (`auth`) | 用户注册/登录/退出 | 表单提交 + JSON API 双模式兼容 |
| **主页路由** (`main`) | 页面渲染分发 | 4 个有效页面路由（index/recommend/diary/map） |
| **日记系统** (`diary`) | 日记完整生命周期 | 自增 ID / 导入导出 / 时间戳追踪 |
| **推荐系统** (`recommend`) | 多维度推荐数据 | 热度排序 / 评分排序双策略 |
| **评分系统** (`rating`) | 多类型评分管理 | 1-5 星 / 评论 / 排行榜 |

### 分层架构总览

```
表现层 (Vue 3 模板)        ← web_app/templates/
         ↓ fetch() JSON
路由控制层 (Blueprint)     ← backend/routes/
         ↓
业务逻辑层 (Service)       ← services/
         ↓
数据访问层 (ORM, 预留)     ← models/  +  db/
         ↓
持久层                     ← Pickle(当前) / MySQL(目标)
```

详细架构说明请参阅 [整体架构.md](./整体架构.md)。

### 前后端通信架构

```
浏览器 (Vue 3)
    │
    │  fetch() JSON API
    ▼
Flask 后端 (Jinja2 渲染初始页面)
    │
    ├─ /api/user/status   →  登录状态查询
    ├─ /api/login         →  登录认证
    ├─ /api/register      →  用户注册
    ├─ /api/diary         →  日记 CRUD
    ├─ /api/diary/export  →  日记导出
    ├─ /api/diary/import  →  日记导入
    ├─ /api/spots         →  景点推荐数据
    ├─ /api/food          →  美食推荐数据
    └─ /api/universities  →  名校推荐数据
```

## 快速开始

### 环境要求

- Python 3.7+
- Flask 2.0+
- 浏览器（需联网加载 CDN 资源）

### 安装依赖

```bash
git clone <repo-url>
cd personalized-travel-system
pip install -r requirements.txt
```

### 启动系统

```bash
python main.py
```

启动后在浏览器访问 **http://localhost:5000**

### 测试账号

| 用户名 | 密码 |
|--------|------|
| test | 123456 |

## MySQL 迁移指南（可选）

当前系统使用 Pickle 文件存储数据，适合单机 Demo 场景。如需迁移到 MySQL：

### 前置条件

```bash
# 安装额外依赖
pip install flask-sqlalchemy pymysql

# 确保 MySQL 8.x 已安装并运行
# 创建数据库
mysql -u root -p -e "CREATE DATABASE travel_system DEFAULT CHARSET utf8mb4;"
```

### 启用步骤

1. **修改连接串**：编辑 `config/settings.py` 中的 `DATABASE_URL`，填入实际的用户名和密码
2. **取消注释启用 ORM**：
   - `backend/app.py`：取消注释 import 和 init_db 调用
   - `db/db.py`：取消注释 SQLAlchemy 实例化代码
   - `models/user_model.py`：取消注释 User 类定义
   - `models/diary_model.py`：取消注释 Diary 类定义
3. **重写 Service 层**：将 `user_service.py` 和 `diary_service.py` 中的 dict 操作替换为 `db.session.query(Model)` 
4. **数据迁移**：编写脚本读取旧 `.pkl` 文件并批量 INSERT 到 MySQL
5. **清理旧文件**：移除 `utils/storage.py`、删除 `data/db/*.pkl`

> 详细 DDL 语句、ER 图、ORM 示例代码和完整的 4 Phase 迁移路线图请参阅 [整体架构.md §四~§八](./整体架构.md)。

## 使用指南

| 页面 | 路径 | 功能说明 |
|------|------|----------|
| **首页** | `/` | 系统介绍和功能概览，无需登录即可访问 |
| **登录/注册** | `/login` `/register` | 统一的认证页面，Vue 3 表单验证 |
| **旅游推荐** | `/recommend` | 景点/美食/名校三栏展示，热门/评分双模式切换 |
| **日记管理** | `/diary` | 创建/编辑/删除日记，JSON 格式导入导出 |
| **地图导航** | `/map` | 高德地图，POI 搜索选点，驾车/步行/骑行路线规划 |

## 注意事项

- 首次运行时系统会自动创建测试账号
- 地图功能需要网络连接以加载高德地图 SDK
- Vue 3 通过 CDN 引入，首次访问需要下载约 150KB 的运行时文件
- 当前使用 Pickle 作为数据存储方案；架构已预留 MySQL 迁移路径，详见 [整体架构.md](./整体架构.md)
- 未登录状态下点击受保护链接会弹出「请先登录」提示弹窗，而非直接跳转

## 许可证

本项目采用 MIT 许可证，详情请查看 LICENSE 文件。
