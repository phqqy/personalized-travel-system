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
│       ├── travel.py         # 旅游服务路由（路径规划/场所查询）
│       └── rating.py         # 评分系统路由
│
├── config/                    # 配置层（所有参数统一管理）
│   ├── __init__.py
│   └── settings.py           # 系统配置（路径、端口、密钥等）
│
├── services/                  # 业务服务层（核心功能）
│   ├── __init__.py
│   ├── user_service.py      # 用户服务（注册、登录、用户管理）
│   ├── diary_service.py       # 日记服务（增删改查、导入导出）
│   ├── recommend_service.py   # 推荐服务（景点、美食、名校推荐）
│   ├── path_service.py       # 路线规划服务（多策略路径规划）
│   ├── query_service.py      # 场所查询服务（设施查询）
│   └── rating_service.py     # 评分服务（评分、评论、统计）
│
├── utils/                     # 工具层（通用能力）
│   ├── __init__.py
│   ├── storage.py           # 数据存储工具（pickle文件读写）
│   └── security.py          # 安全工具（密码加密、验证）
│
├── algorithms/                # 算法层（预留扩展）
│   └── __init__.py
│
├── web_app/                 # Web前端
│   ├── start.py             # Web应用启动脚本
│   ├── static/             # 静态资源
│   │   ├── css/            # 样式文件
│   │   └── images/         # 图片资源
│   └── templates/          # HTML模板
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── recommend.html
│       ├── path.html
│       ├── query.html
│       ├── diary.html
│       └── map.html
│
└── data/                    # 数据层
    ├── db/                 # 数据库文件
    │   └── travel.db
    └── raw/                # 原始数据
        ├── spots.csv
        ├── food.csv
        └── facilities.csv
```

## 架构说明

### 高度可扩展的分层架构设计

本系统采用**分层架构 + 模块化设计 + Flask Blueprint**，实现了高内聚、低耦合的代码组织，每个模块职责单一，便于独立开发、测试和扩展。

#### 1. 配置层 (config/)

- **职责**：统一管理系统配置参数
- **内容**：路径配置、端口配置、密钥配置、数据库配置等
- **优势**：便于环境切换、参数调整，避免硬编码

#### 2. 工具层 (utils/)

- **职责**：提供通用的工具功能
- **模块**：
  - `storage.py`：数据持久化工具，封装pickle文件读写
  - `security.py`：安全工具，密码加密和验证
- **优势**：工具复用，减少重复代码

#### 3. 服务层 (services/)

- **职责**：核心业务逻辑实现，与路由层解耦
- **模块**：
  - `user_service.py`：用户管理（创建、验证、查询）
  - `diary_service.py`：日记管理（CRUD、导入导出）
  - `recommend_service.py`：推荐服务（景点、美食、名校）
  - `path_service.py`：路径规划（多种策略）
  - `query_service.py`：场所查询（过滤、搜索）
  - `rating_service.py`：评分系统（评分、评论、统计）
- **优势**：业务逻辑独立，可单独测试，便于扩展

#### 4. 装饰器层 (backend/decorators.py)

- **职责**：横切关注点处理
- **内容**：`@login_required` 登录状态检查装饰器
- **优势**：AOP思想，避免代码重复

#### 5. 路由层 (backend/routes/)

- **职责**：HTTP请求处理、参数验证、响应组装
- **使用Flask Blueprint实现模块化路由**：
  - `main.py`：主页和页面路由
  - `auth.py`：用户认证（登录/注册/退出）
  - `diary.py`：日记API（/api/diary/*）
  - `recommend.py`：推荐API（/api/recommend/*）
  - `travel.py`：旅游服务（路径规划、场所查询）
  - `rating.py`：评分API（/api/rating/*）
- **优势**：路由模块化，便于管理，可独立挂载

#### 6. 应用入口 (backend/app.py)

- **职责**：Flask应用创建、蓝图注册、初始化
- **功能**：
  - `create_app()`：应用工厂函数
  - `register_blueprints()`：统一注册所有蓝图
  - `init_data()`：数据初始化
- **优势**：集中管理，便于配置

### 模块职责详表

| 层级 | 模块 | 职责 |
|------|------|------|
| 配置 | `config/settings.py` | 系统配置管理 |
| 工具 | `utils/storage.py` | 数据持久化 |
| 工具 | `utils/security.py` | 安全相关功能 |
| 服务 | `services/user_service.py` | 用户业务逻辑 |
| 服务 | `services/diary_service.py` | 日记业务逻辑 |
| 服务 | `services/recommend_service.py` | 推荐业务逻辑 |
| 服务 | `services/path_service.py` | 路径规划业务逻辑 |
| 服务 | `services/query_service.py` | 查询业务逻辑 |
| 服务 | `services/rating_service.py` | 评分系统业务逻辑 |
| 装饰器 | `backend/decorators.py` | 横切关注点（登录检查） |
| 路由 | `backend/routes/main.py` | 主页和页面路由 |
| 路由 | `backend/routes/auth.py` | 用户认证路由 |
| 路由 | `backend/routes/diary.py` | 日记API路由 |
| 路由 | `backend/routes/recommend.py` | 推荐API路由 |
| 路由 | `backend/routes/travel.py` | 旅游服务路由 |
| 路由 | `backend/routes/rating.py` | 评分系统路由 |
| 应用 | `backend/app.py` | Flask应用主程序、蓝图注册 |

### 评分系统说明

新增的评分系统支持对多种类型目标进行评分：

**支持的评分类型**：

- `spot`：景点
- `food`：美食
- `diary`：日记
- `university`：名校

**评分API接口**：

- `POST /api/rating/add`：添加评分和评论
- `GET /api/rating/<type>/<id>`：获取目标的所有评分和平均评分
- `GET /api/rating/<type>/<id>/average`：仅获取平均评分
- `GET /api/rating/my/<type>/<id>`：获取当前用户的评分
- `DELETE /api/rating/<type>/<id>`：删除评分
- `GET /api/rating/top/<type>`：获取评分最高的目标列表

**使用示例**：

```javascript
// 给景点评分
fetch('/api/rating/add', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        target_type: 'spot',
        target_id: '1',
        rating: 5,
        comment: '非常棒的景点！'
    })
});
```

### 扩展指南

#### 添加新功能模块（推荐流程）

如需添加新功能（如照片上传自动生成日记、AIGC动画生成等），请按照以下步骤：

1. **创建服务模块**（在 `services/` 中）

   ```python
   # services/photo_service.py
   class PhotoService:
       @staticmethod
       def generate_diary_from_photo(photo_path):
           # 实现逻辑
           pass
   
   photo_service = PhotoService()
   ```

2. **创建路由模块**（在 `backend/routes/` 中）

   ```python
   # backend/routes/photo.py
   from flask import Blueprint, request, jsonify
   from services.photo_service import photo_service
   from backend.decorators import login_required
   
   photo_bp = Blueprint('photo', __name__, url_prefix='/api/photo')
   
   @photo_bp.route('/generate-diary', methods=['POST'])
   @login_required
   def generate_diary():
       # 实现路由逻辑
       pass
   ```

3. **注册蓝图**（在 `backend/app.py` 的 `register_blueprints()` 中）

   ```python
   from backend.routes.photo import photo_bp
   
   def register_blueprints(app):
       # ... 现有蓝图 ...
       app.register_blueprint(photo_bp)
   ```

4. **添加配置**（如需要，在 `config/settings.py` 中）

5. **添加工具函数**（如需要，在 `utils/` 中）

#### 评分系统扩展

如需支持新的评分类型，只需：

1. 在前端调用API时传入新的 `target_type`
2. 评分服务会自动处理，无需修改后端代码

#### 架构优势

✅ **高内聚**：每个模块职责单一，功能独立  
✅ **低耦合**：层与层之间通过接口调用，依赖清晰  
✅ **易测试**：服务层可独立进行单元测试  
✅ **易扩展**：添加新功能只需新增模块，不影响现有代码  
✅ **易维护**：代码结构清晰，便于定位和修改问题  
✅ **蓝图化**：路由模块化，可独立开发和挂载

## 安装说明

### 后端安装

1. 克隆项目到本地
2. 安装后端依赖：

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
