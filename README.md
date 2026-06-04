# personalized-travel-system

个性化旅游系统

## 项目简介

基于 **Flask + Vue 3** 全栈开发的旅游推荐与导航系统，支持景点推荐、路线规划、日记管理、地图导航等功能。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Flask 2.x | 轻量级Web框架，Blueprint模块化路由 |
| **前端** | Vue 3 (CDN) | Composition API，响应式数据绑定 |
| **模板** | Jinja2 | 服务端渲染HTML |
| **数据库** | SQLite | 轻量级数据库 |
| **地图** | 高德地图 JS API 2.0 | POI搜索/路线规划/室内导航 |
| **数据存储** | SQLite + Pickle | 混合存储方案 |
| **图标** | Font Awesome 6.4 | UI图标库 |

## 核心功能

- **旅游推荐**：基于热度和评分排序的景点/美食/名校推荐
- **景点大全**：搜索、标签筛选、排序功能
- **名校游览**：搜索、标签筛选、排序功能
- **特色美食**：搜索、标签筛选、排序功能
- **地图导航**：高德地图集成，支持室外导航和室内导航切换
- **日记管理**：完整的CRUD操作，支持JSON导入导出
- **用户认证**：安全的登录注册机制，Session会话管理

## 项目结构

```
personalized-travel-system/
├── main.py                    # 启动入口
├── requirements.txt           # 后端依赖清单
├── .env.example              # 环境变量示例
├── backend/                   # 后端核心
│   ├── app.py                 # 应用工厂 + 蓝图注册
│   ├── decorators.py          # 登录检查装饰器
│   └── routes/                # 路由模块
├── config/settings.py         # 全局配置
├── models/                    # 数据模型
├── db/                        # 数据库初始化
├── services/                  # 业务服务
├── data/                      # 数据目录
│   ├── db/                    # 数据库文件
│   └── raw/                   # CSV原始数据
└── web_app/                   # 前端应用
    ├── static/                # 静态资源
    └── templates/             # Vue 3页面模板
```

## 快速开始

### 环境要求

- Python 3.7+
- Flask 2.0+
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
copy .env.example .env
```

2. 编辑 `.env` 文件，配置高德地图API：
```env
# 高德地图API配置
AMAP_API_KEY=your_amap_api_key_here
AMAP_SECURITY_CODE=your_amap_security_code_here
```

**获取高德地图API密钥：**
1. 访问 [高德地图开发者平台](https://console.amap.com/)
2. 注册账号并创建应用
3. 获取 Web端 API Key 和安全码

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
| **旅游推荐** | `/recommend` | 景点/美食/名校三栏展示 |
| **景点大全** | `/spots` | 搜索、标签筛选、排序 |
| **名校游览** | `/universities` | 搜索、标签筛选、排序 |
| **特色美食** | `/food` | 搜索、标签筛选、排序 |
| **日记管理** | `/diary` | 创建/编辑/删除日记，JSON导入导出 |
| **地图导航** | `/map` | 高德地图，室外导航，室内导航切换 |

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
copy .env.example .env
# 编辑 .env 文件，添加高德地图API密钥

# 5. 启动开发服务器
python main.py
```

### 生产环境部署

#### 使用 Gunicorn（Linux/Mac）

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动生产服务器
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

## 地图功能说明

### 室外导航
- 支持POI搜索
- 多种路线规划（驾车、步行、公交）
- 地图中心默认定位北京邮电大学沙河校区

### 室内导航
- 基于高德室内地图API
- 支持楼层切换
- 默认显示朝阳大悦城室内地图
- 支持室内POI搜索

## 注意事项

- 首次运行时系统会自动创建测试账号
- 地图功能需要网络连接以加载高德地图SDK
- Vue 3通过CDN引入，首次访问需要下载运行时文件
- 未登录状态下点击受保护链接会弹出「请先登录」提示弹窗
- 室内导航功能需要高德地图API密钥配置正确才能正常显示

## 许可证

本项目采用 MIT 许可证。
