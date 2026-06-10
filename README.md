# 个性化旅游系统

基于 **Flask + Vue 3** 的全栈旅游推荐与导航平台，集成 AI 视频生成、室内外导航、日记社区等功能。

## 项目简介

提供一站式旅游服务：智能景点/美食/名校推荐、高德地图路线规划、室内跨楼层导航、旅行日记记录与分享、AI 视频生成。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Flask 2.x + Blueprint | 模块化 RESTful API |
| **前端** | Vue 3 (CDN) + Jinja2 | Composition API，服务端渲染 |
| **地图** | 高德地图 JS API 2.0 | POI 搜索、驾车/步行/骑行规划 |
| **室内导航** | Canvas 2D + Dijkstra | 自定义楼层平面图，跨楼层路径 |
| **AI 视频** | 火山引擎即梦 3.0 | 日记内容 → 720p AI 视频 |
| **AI Agent** | DeepSeek API | 编码助手 + 测试助手 |
| **算法库** | 纯 Python 实现 | 图论、排序、DP、数据结构等 |
| **存储** | Pickle + CSV | 用户/日记持久化，景点数据管理 |

## 核心功能

### 旅游推荐
- 景点/美食/名校三栏推荐，按热度/评分排序
- 搜索、标签筛选、排序切换
- 370 个景点、56 所名校、10 种美食数据

### 地图导航
- **室外导航**：高德地图集成，POI 搜索，驾车/步行/骑行路线
- **室内导航**：Canvas 自绘 3 栋建筑 14 层平面图，Dijkstra 跨楼层最短路径
- 12 种室内节点类型（教室/电梯/卫生间/咖啡厅等）

### 日记社区
- 全部用户日记公开共享，支持浏览他人游记
- CRUD 操作 + JSON 导入导出
- ❤️ 点赞 + 💬 评论互动
- AI 视频生成：根据日记内容生成旅行短视频

### AI Agent（命令行工具）
- **Coder Agent**：Python/Flask/Vue 编码助手
- **Tester Agent**：pytest 测试用例生成器
- 基于 DeepSeek API，流式输出

### 算法库（`algorithms/`）
- **图论**：Dijkstra、Bellman-Ford、Floyd-Warshall、Prim、Kruskal、拓扑排序
- **排序**：快排、归并、堆排、插入、计数、桶排
- **数据结构**：BST、线段树、树状数组、LRU 缓存、Trie
- **DP & 贪心**：背包、LCS/LIS、编辑距离、区间调度、Huffman 编码
- **搜索**：二分、KMP、Rabin-Karp
- **数学**：素数筛、GCD、快速幂、组合数、矩阵运算

## 项目结构

```
personalized-travel-system/
├── main.py                     # 启动入口
├── requirements.txt            # Python 依赖
├── .env / .env.example         # API 密钥配置
│
├── backend/                    # 后端核心
│   ├── app.py                  # Flask 应用工厂 + 蓝图注册
│   ├── decorators.py           # @login_required 装饰器
│   └── routes/                 # 路由模块
│       ├── auth.py             # 登录/注册/登出
│       ├── diary.py            # 日记 CRUD + 点赞 + 评论
│       ├── video.py            # AI 视频生成
│       ├── recommend.py        # 推荐 + 搜索 API
│       ├── map.py              # 地图相关
│       └── main.py             # 页面路由
│
├── services/                   # 业务逻辑层
│   ├── diary_service.py        # 日记服务（含点赞/评论/视频关联）
│   ├── recommend_service.py    # CSV 数据加载 + 推荐排序
│   ├── jimeng_service.py       # 火山引擎即梦 AI 视频生成
│   ├── video_service.py        # 视频匹配与脚本生成
│   ├── user_service.py         # 用户认证
│   ├── indoor_service.py       # 室内导航（Dijkstra 路径搜索）
│   └── rating_service.py       # 评分服务
│
├── algorithms/                 # 算法库（独立模块，可复用）
│   ├── graph.py                # 最短路径 / 最小生成树 / 拓扑排序
│   ├── sorting.py              # 比较排序 / 非比较排序
│   ├── structures.py           # BST / 线段树 / 树状数组 / LRU / Trie
│   ├── optimize.py             # 动态规划 / 贪心
│   ├── search.py               # 二分搜索 / KMP / Rabin-Karp
│   └── math.py                 # 数论 / 组合 / 矩阵
│
├── config/settings.py          # 全局配置
├── utils/storage.py            # Pickle 持久化工具
│
├── scripts/                    # 工具脚本
│   ├── agent_base.py           # AI Agent 基类（DeepSeek API）
│   ├── coder_agent.py          # 编码智能体
│   ├── tester_agent.py         # 测试智能体
│   ├── expand_data.py          # 数据扩充脚本
│   └── fix_images.py           # 图片修复脚本
│
├── data/
│   ├── raw/                    # CSV 原始数据
│   │   ├── spots.csv           # 370 个景点
│   │   ├── universities.csv    # 56 所名校
│   │   └── food.csv            # 10 种美食
│   ├── db/                     # Pickle 持久化文件
│   └── indoor.json             # 室内地图数据（3 栋 14 层 150+ 节点）
│
└── web_app/                    # 前端
    ├── static/
    │   ├── css/main.css        # 全局样式
    │   └── images/             # 景点/美食/背景图片
    └── templates/              # 8 个 Vue 3 页面
        ├── index.html          # 首页
        ├── login.html          # 登录/注册
        ├── recommend.html      # 旅游推荐
        ├── spots.html          # 景点大全
        ├── universities.html   # 名校游览
        ├── food.html           # 特色美食
        ├── diary.html          # 日记社区
        └── map.html            # 地图导航
```

## 快速开始

### 环境要求

- Python 3.7+
- 浏览器（需联网加载 CDN）

### 安装

```bash
git clone <repo-url>
cd personalized-travel-system
pip install -r requirements.txt
```

### 配置 API 密钥

编辑 `.env` 文件：

```env
# 高德地图 API（必须 — 地图功能）
AMAP_API_KEY=你的Key
AMAP_SECURITY_CODE=你的安全码

# 火山引擎（可选 — AI 视频生成）
VOLCENGINE_ACCESS_KEY=你的AK
VOLCENGINE_SECRET_KEY=你的SK

# DeepSeek API（可选 — AI Agent）
DEEPSEEK_API_KEY=sk-xxxxxxxx
```

- 高德 Key：https://console.amap.com/dev/key/app → 选择 Web端(JS API)
- 火山引擎：https://console.volcengine.com/iam/keymanage → 需开通即梦AI服务
- DeepSeek：https://platform.deepseek.com → 注册即送额度

### 启动

```bash
python main.py
```

浏览器访问 **http://localhost:5000**

### 测试账号

| 用户名 | 密码 |
|--------|------|
| test | 123456 |

## 页面导航

| 路径 | 页面 | 说明 |
|------|------|------|
| `/` | 首页 | 系统介绍 |
| `/login` | 登录 | 用户认证 |
| `/register` | 注册 | 创建账号 |
| `/recommend` | 旅游推荐 | 景点/美食/名校三栏推荐 |
| `/spots` | 景点大全 | 370 个景点搜索筛选 |
| `/universities` | 名校游览 | 56 所大学搜索筛选 |
| `/food` | 特色美食 | 10 种美食搜索筛选 |
| `/diary` | 日记社区 | 全部用户日记共享，点赞评论，AI 视频 |
| `/map` | 地图导航 | 室外高德 + 室内楼层导航 |

## AI Agent 使用

```bash
# 编码助手
python scripts/coder_agent.py "写一个Python函数对list去重并保持顺序"

# 测试助手
python scripts/tester_agent.py "def add(a, b): return a + b"
```

需在 `.env` 中配置 `DEEPSEEK_API_KEY`。

## 室内导航数据

| 建筑 | 楼层 | 节点 | 边 | 特色 |
|------|------|------|-----|------|
| 图书馆 | B1~5F (6层) | 66 | 106 | 书库/自习区/电子阅览室 |
| 第一教学楼 | 1~5F (5层) | 54 | 84 | 教室/实验室/计算机房 |
| 学生活动中心 | 1~3F (3层) | 30 | 46 | 超市/咖啡厅/健身房 |

## 部署

### 开发环境

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
pip install -r requirements.txt
python main.py
```

### 生产环境（Gunicorn）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## 许可证

MIT License
