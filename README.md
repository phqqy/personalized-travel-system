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
| **数据库** | MySQL 8.x (预留) | 关系型数据库，替代Pickle文件存储 |
| **地图** | 高德地图 JS API 2.0 | POI搜索/路线规划 |
| **数据存储** | Pickle文件 (当前) | 适合单机Demo场景 |
| **图标** | Font Awesome 6.4 | UI图标库 |

## 核心功能

- **旅游推荐**：基于热度和评分排序的景点/美食/名校推荐
- **景点大全**：搜索、标签筛选、排序功能
- **名校游览**：搜索、标签筛选、排序功能
- **特色美食**：搜索、标签筛选、排序功能
- **地图导航**：高德地图集成，支持POI搜索和多种路线规划
- **日记管理**：完整的CRUD操作，支持JSON导入导出
- **用户认证**：安全的登录注册机制，Session会话管理

## 项目结构

```
personalized-travel-system/
├── main.py                    # 启动入口
├── requirements.txt           # 后端依赖清单
├── 整体架构.md                  # 架构设计文档
├── backend/                   # 后端核心
│   ├── app.py                 # 应用工厂 + 蓝图注册
│   ├── decorators.py          # 登录检查装饰器
│   └── routes/                # 路由模块
├── config/settings.py         # 全局配置
├── models/                    # ORM模型（预留）
├── db/                        # 数据库初始化（预留）
├── services/                  # 业务服务
├── data/                      # 数据目录
│   ├── db/                    # Pickle数据文件
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
| **地图导航** | `/map` | 高德地图，POI搜索，路线规划 |

## MySQL 迁移（可选）

当前系统使用Pickle文件存储数据，适合单机Demo场景。如需迁移到MySQL，详见 [整体架构.md](./整体架构.md)。

## 注意事项

- 首次运行时系统会自动创建测试账号
- 地图功能需要网络连接以加载高德地图SDK
- Vue 3通过CDN引入，首次访问需要下载运行时文件
- 未登录状态下点击受保护链接会弹出「请先登录」提示弹窗

## 许可证

本项目采用 MIT 许可证。
