# 个性化旅游系统 - 整合版Web前端

## 项目介绍

这是一个整合版的个性化旅游系统Web前端，基于Flask框架开发，包含以下核心功能：

- 旅游推荐：基于热度和评分的景点和美食推荐
- 路线规划：支持最短距离、最快时间和最少拥挤三种策略
- 场所查询：支持关键词搜索附近设施
- 日记管理：支持创建、编辑、删除和查看日记
- 地图展示：直观展示景点和美食位置

## 技术栈

- 后端：Python, Flask, Flask-CORS, NetworkX
- 前端：HTML, CSS, JavaScript, Font Awesome, Leaflet.js

## 项目结构

```
web_app/
├── templates/          # HTML模板
│   ├── index.html      # 首页
│   ├── recommend.html  # 旅游推荐
│   ├── path.html       # 路线规划
│   ├── query.html      # 场所查询
│   ├── diary.html      # 日记管理
│   └── map.html        # 地图展示
├── app.py              # Flask应用主文件
├── start.py            # 启动脚本
└── README.md           # 说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install Flask Flask-CORS networkx pyyaml pandas
```

### 2. 启动系统

```bash
# 方法1：直接运行启动脚本
python start.py

# 方法2：手动运行
cd web_app
python app.py
```

### 3. 访问系统

在浏览器中打开：http://localhost:5000

## 功能说明

### 旅游推荐
- 支持热度推荐和评分推荐两种方式
- 可查看景点和美食的详细信息

### 路线规划
- 支持最短距离、最快时间和最少拥挤三种策略
- 支持步行、骑行和驾车三种交通方式
- 显示详细的路线步骤和距离信息

### 场所查询
- 支持关键词搜索附近设施
- 显示场所的详细信息，包括位置、联系方式和营业时间

### 日记管理
- 支持创建、编辑、删除和查看日记
- 按时间排序展示日记列表

### 地图展示
- 使用Leaflet.js显示地图
- 支持显示景点和美食的位置标记
- 可点击标记查看详细信息

## 注意事项

1. 系统默认使用端口5000，如果该端口被占用，请修改app.py中的端口设置
2. 系统使用示例数据，实际使用时可替换为真实数据
3. 地图展示使用的是OpenStreetMap，需要网络连接

## 故障排除

### 常见问题

1. **依赖项安装失败**
   - 确保pip版本是最新的：`pip install --upgrade pip`
   - 尝试使用管理员权限运行命令

2. **端口被占用**
   - 修改app.py中的端口设置：`app.run(debug=True, host='0.0.0.0', port=8000)`

3. **地图加载失败**
   - 检查网络连接
   - 确保Leaflet.js库加载正常

4. **数据加载失败**
   - 确保data目录下有正确的CSV数据文件
   - 检查数据文件格式是否正确

## 许可证

MIT License
