# personalized-travel-system

个性化旅游系统

## 项目简介

个性化旅游系统是一个基于Python开发的旅游推荐与导航系统，旨在为用户提供个性化的旅游体验。系统支持景点推荐、路线规划、场所查询、日记管理等功能，帮助用户更好地规划和享受旅游过程。

## 架构重构 (2026-03)

本次重构将项目升级为高度可扩展的模块化架构：

### 核心改进

1. **更深层次的模块化拆分**
   - 装饰器层：横切关注点处理（登录检查等）
   - 路由层：使用Flask Blueprint实现完全模块化
   - 路由模块细分：主页、认证、日记、推荐、旅游服务、评分系统

2. **新增评分系统**
   - 支持多种评分类型（景点、美食、日记、名校）
   - 1-5星评分 + 文字评论
   - 平均评分、个人评分、评分排行榜
   - 完整的CRUD操作

3. **架构优势**
   - 高内聚低耦合
   - 易于测试和扩展
   - 完整的文档指南

## 功能特点

- **旅游推荐**：基于热度、评价和用户兴趣的个性化推荐
- **路线规划**：支持多种策略的路线规划（距离、时间、交通工具、室内导航）
- **场所查询**：附近设施查询和分类过滤
- **日记管理**：支持日记的增删改查、压缩存储和热度排序
- **评分系统**：支持对景点、美食、日记等进行1-5星评分和评论
- **美食推荐**：基于排序和模糊查询的美食推荐
- **地图可视化**：直观展示地图和路径
- **AIGC动画生成**：预留扩展接口，支持将照片转换为旅游动画

## 技术栈

- **后端**：Python, Flask, Flask Blueprint
- **前端**：HTML, CSS, JavaScript (Jinja2模板)
- **数据存储**：SQLite, Pickle
- **地图处理**：预留NetworkX, Leaflet接口
- **架构模式**：分层架构 + 模块化设计

## 项目结构

```
personalized-travel-system/
├── .gitignore                # Git忽略文件
├── README.md                   # 项目说明、运行指南、功能介绍
├── requirements.txt            # 后端依赖清单（Python库）
├── main.py                     # 项目主入口
│
├── backend/                   # 后端代码
│   ├── __init__.py
│   ├── app.py                # 后端Flask应用主文件（蓝图注册中心）
│   ├── decorators.py         # 装饰器（登录检查等）
│   └── routes/               # 路由模块（Flask Blueprint）
│       ├── __init__.py
│       ├── main.py           # 主页和页面路由
│       ├── auth.py           # 用户认证路由（登录/注册/退出）
│       ├── diary.py          # 日记API路由
│       ├── recommend.py      # 推荐API路由
│       └── rating.py         # 评分系统路由
│
├── config/                    # 配置管理
│   ├── __init__.py
│   └── settings.py          # 系统配置（数据库连接、服务配置等）
│
├── services/                  # 业务逻辑服务
│   ├── __init__.py
│   ├── user_service.py       # 用户服务（注册、登录、验证）
│   ├── diary_service.py      # 日记服务（CRUD操作、存储管理）
│   ├── rating_service.py     # 评分服务（评分操作、排行榜）
│   └── recommend_service.py  # 推荐服务（景点、美食推荐）
│
├── utils/                     # 工具模块
│   ├── __init__.py
│   ├── security.py           # 安全工具（密码加密、验证）
│   └── storage.py            # 存储工具（文件、缓存管理）
│
├── data/                      # 数据目录
│   ├── db/                   # 数据库文件
│   └── raw/                  # 原始数据文件
│
├── cache/                     # 缓存目录（地图数据、临时文件）
│
└── web_app/                   # 前端Web应用
    ├── static/               # 静态资源（CSS、图片、JavaScript）
    └── templates/            # HTML模板
        ├── index.html        # 首页
        ├── auth.html         # 登录/注册页面（整合版）
        ├── diary.html        # 日记管理页面
        ├── map.html          # 地图展示页面
        └── recommend.html    # 旅游推荐页面
```

### 核心模块说明

| 模块 | 主要职责 | 文件位置 | <mcfile>引用 |
| ---- | ------- | -------- | ----------- |
| **认证系统** | 用户注册/登录/退出 | `backend/routes/auth.py` | <mcfile name="auth.py" path="backend/routes/auth.py"></mcfile> |
| **日记系统** | 日记的增删改查、存储管理 | `backend/routes/diary.py` | <mcfile name="diary.py" path="backend/routes/diary.py"></mcfile> |
| **推荐系统** | 景点和美食推荐 | `backend/routes/recommend.py` | <mcfile name="recommend.py" path="backend/routes/recommend.py"></mcfile> |
| **评分系统** | 评分和评论管理 | `backend/routes/rating.py` | <mcfile name="rating.py" path="backend/routes/rating.py"></mcfile> |
| **用户服务** | 用户管理和验证 | `services/user_service.py` | <mcfile name="user_service.py" path="services/user_service.py"></mcfile> |
| **日记服务** | 日记业务逻辑 | `services/diary_service.py` | <mcfile name="diary_service.py" path="services/diary_service.py"></mcfile> |
| **评分服务** | 评分业务逻辑 | `services/rating_service.py` | <mcfile name="rating_service.py" path="services/rating_service.py"></mcfile> |
| **推荐服务** | 推荐算法和逻辑 | `services/recommend_service.py` | <mcfile name="recommend_service.py" path="services/recommend_service.py"></mcfile> |

## 快速开始

### 环境要求

- Python 3.7+
- Flask 2.0+

### 安装依赖

1. 克隆项目：

   ```bash
   git clone https://github.com/phqqy/personalized-travel-system.git
   cd personalized-travel-system
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 启动后端服务：

   ```bash
   python main.py
   ```

   或者从web_app目录启动：

   ```bash
   cd web_app
   python start.py
   ```

### 访问系统

启动后，在浏览器中打开 <http://localhost:5000>

## 使用方法

### 启动系统

1. **启动系统**：

   ```bash
   python main.py
   ```

   或者

   ```bash
   cd web_app
   python start.py
   ```

2. **访问系统**：
   在浏览器中打开 <http://localhost:5000>

3. **测试账号**：
   - 用户名：test
   - 密码：123456

4. **功能介绍**：
   - **首页**：系统介绍和功能概览
   - **旅游推荐**：查看系统推荐的景点和美食
   - **路线规划**：输入起点和终点，选择规划策略
   - **场所查询**：搜索附近的设施和场所
   - **日记管理**：创建、查看旅游日记
   - **地图展示**：查看地图和景点位置

## 数据说明

- 系统默认包含200+景区/校园数据
- 每个景区包含≥20个建筑数据
- 服务设施包含≥10种、≥50个
- 道路数据包含≥200条边

## 注意事项

- 首次运行时，系统会自动初始化数据库和加载数据
- 请确保有足够的存储空间用于存储日记和图片
- 部分功能可能需要网络连接

## 许可证

本项目采用 MIT 许可证，详情请查看 LICENSE 文件。