# personalized-travel-system

个性化旅游系统

## 项目简介

基于 **Flask + Vue 3** 全栈开发的旅游推荐与导航系统，支持景点推荐、路线规划、日记管理、室外地图导航与室内楼层导航等功能。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Flask 2.x | 轻量级Web框架，Blueprint模块化路由 |
| **前端** | Vue 3 (CDN) | Composition API，响应式数据绑定 |
| **模板** | Jinja2 | 服务端渲染HTML |
| **数据库** | SQLite | 轻量级关系数据库 |
| **室外地图** | 高德地图 JS API 2.0 | POI搜索、驾车/步行/骑行路线规划 |
| **室内地图** | Canvas 2D | 自定义楼层平面图绘制，Dijkstra路径规划 |
| **AI视频** | 火山引擎（即梦3.0） | 根据日记内容生成720p AI视频 |
| **数据存储** | SQLite + Pickle + JSON | 混合存储方案 |
| **图标** | Font Awesome 6.4 | UI图标库 |

## 核心功能

- **旅游推荐**：基于热度和评分排序的景点/美食/名校推荐
- **景点大全**：搜索、标签筛选、排序功能
- **名校游览**：搜索、标签筛选、排序功能
- **特色美食**：搜索、标签筛选、排序功能
- **室外导航**：高德地图集成，POI搜索，支持驾车/步行/骑行三种路线规划
- **室内导航**：Canvas自绘楼层平面图，支持3栋建筑14个楼层、Dijkstra跨楼层路径规划
- **日记管理**：完整的CRUD操作，支持JSON导入导出
- **AI视频生成**：根据日记内容调用即梦3.0(720p)生成旅行视频
- **用户认证**：安全的登录注册机制，Session会话管理

## 项目结构

```
personalized-travel-system/
├── main.py                    # 启动入口
├── requirements.txt           # 后端依赖清单
├── .env / .env.example        # 环境变量配置
├── backend/                   # 后端核心
│   ├── app.py                 # 应用工厂 + 蓝图注册
│   ├── decorators.py          # 登录检查装饰器
│   └── routes/                # 路由模块（auth/diary/map/recommend/video等）
├── config/settings.py         # 全局配置（Amap/Volcengine/DB）
├── models/                    # 数据模型（user/diary）
├── db/                        # 数据库初始化与连接
├── services/                  # 业务服务
│   ├── indoor_service.py      # 室内导航（Dijkstra路径查找）
│   ├── recommend_service.py   # 推荐算法
│   ├── jimeng_service.py      # AI视频生成
│   └── ...
├── algorithms/                # 图算法模块
├── data/                      # 数据目录
│   ├── db/                    # SQLite数据库文件
│   ├── raw/                   # CSV原始数据（spots/food/universities）
│   └── indoor.json            # 室内地图数据（3栋建筑14层150+节点）
├── web_app/                   # 前端应用
│   ├── static/
│   │   ├── css/main.css       # 全局样式
│   │   └── images/            # 背景图/景点图/美食图
│   └── templates/             # Vue 3页面模板（8个页面）
└── data/db/                   # 运行时数据库
```

## 快速开始

### 环境要求

- Python 3.7+
- 浏览器（需联网加载CDN资源）

### 安装依赖

```bash
git clone <repo-url>
cd personalized-travel-system
pip install -r requirements.txt
```

### 配置环境变量

1. 复制 `.env.example` 文件为 `.env`：
```bash
cp .env.example .env    # Linux/Mac
copy .env.example .env  # Windows
```

2. 编辑 `.env` 文件，配置API密钥：
```env
# 高德地图API配置（必须）
# 获取地址: https://console.amap.com/dev/key/app
AMAP_API_KEY=your_amap_api_key_here
AMAP_SECURITY_CODE=your_amap_security_code_here

# 火山引擎（即梦AI视频）配置（可选）
# 获取地址: https://console.volcengine.com/iam/keymanage
VOLCENGINE_ACCESS_KEY=your_access_key_here
VOLCENGINE_SECRET_KEY=your_secret_key_here
```

**获取高德地图API密钥：**
1. 访问 [高德地图开发者平台](https://console.amap.com/)
2. 注册账号并创建应用
3. 选择 Web端(JS API) 平台，获取 Key 和安全码

### 启动系统

```bash
python main.py
```

启动后在浏览器访问 **http://localhost:5000**

### 测试账号

| 用户名 | 密码 |
|--------|------|
| test | 123456 |

## 功能导航

| 页面 | 路径 | 功能说明 |
|------|------|----------|
| **首页** | `/` | 系统介绍和功能概览 |
| **登录/注册** | `/login` `/register` | 统一的认证页面 |
| **旅游推荐** | `/recommend` | 景点/美食/名校三栏推荐 |
| **景点大全** | `/spots` | 搜索、标签筛选、排序 |
| **名校游览** | `/universities` | 搜索、标签筛选、排序 |
| **特色美食** | `/food` | 搜索、标签筛选、排序 |
| **日记管理** | `/diary` | 创建/编辑/删除日记，AI视频生成 |
| **地图导航** | `/map` | 室外高德地图导航 + 室内楼层导航切换 |

## 地图功能说明

### 室外导航
- 高德地图 JS API 2.0 集成
- POI地点搜索，点击地图标记选择起终点
- 三种交通方式：**驾车**、**步行**、**骑行**
- 自动显示路线距离、预计时间和交通方式
- 支持从景点页一键跳转定位

### 室内导航
- **Canvas 2D** 自绘楼层平面图，支持高 DPI 渲染
- **12种节点类型**：入口/电梯/楼梯/教室/服务台/区域/办公室/卫生间/咖啡厅/仓库/健身房/休息区
- **层级选择**：选择建筑 → 选择楼层 → 点击画布节点设置起终点
- **Dijkstra 算法**跨楼层路径规划，通过电梯/楼梯连接不同楼层
- 路径高亮显示（蓝色边 + 放大节点）+ 详细步骤列表（含楼层标注）
- 自动缩放到数据范围，适配不同建筑布局

#### 室内建筑数据

| 建筑 | 楼层 | 节点数 | 边数 | 特色区域 |
|------|------|--------|------|----------|
| 图书馆 | B1~5F (6层) | 66 | 106 | 书库/自习区/电子阅览室/古籍馆/档案馆 |
| 第一教学楼 | 1~5F (5层) | 54 | 84 | 教室/实验室/语音室/计算机房/大讲座厅 |
| 学生活动中心 | 1~3F (3层) | 30 | 46 | 超市/咖啡厅/健身房/乒乓球室/社团办公室 |

## 部署说明

### 开发环境部署

```bash
# 1. 克隆项目
git clone <repo-url>
cd personalized-travel-system

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加高德地图API密钥

# 5. 启动开发服务器
python main.py
```

### 生产环境部署

#### 使用 Gunicorn（Linux/Mac）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

#### 使用 Nginx 反向代理（推荐）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/personalized-travel-system/web_app/static;
    }
}
```

## 注意事项

- 首次运行时系统会自动创建测试账号（test/123456）
- 室外地图需要网络连接以加载高德地图 CDN SDK
- 室内地图为纯前端 Canvas 绘制，离线也可使用
- Vue 3 通过 CDN 引入，首次访问需下载运行时文件
- 未登录状态下点击受保护链接会弹出「请先登录」提示
- AI视频生成功能需要配置火山引擎 API 密钥（可选）

## 许可证

本项目采用 MIT 许可证。
