#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
个性化旅游系统 - Web应用
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import hashlib
import pickle
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于会话加密

# 静态文件配置
app.static_folder = 'static'
app.static_url_path = '/static'

# 数据存储文件
USER_DATA_FILE = 'user_data.pkl'
DIARY_DATA_FILE = 'diary_data.pkl'

# 初始化数据
users = {}
user_diaries = {}

# 加载数据
def load_data():
    global users, user_diaries
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'rb') as f:
                users = pickle.load(f)
        if os.path.exists(DIARY_DATA_FILE):
            with open(DIARY_DATA_FILE, 'rb') as f:
                user_diaries = pickle.load(f)
    except:
        users = {}
        user_diaries = {}

# 保存数据
def save_data():
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(users, f)
    with open(DIARY_DATA_FILE, 'wb') as f:
        pickle.dump(user_diaries, f)

# 密码加密
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 初始化数据
load_data()

# 创建测试账号
def create_test_account():
    global users, user_diaries
    if 'test' not in users:
        users['test'] = {
            'name': 'test',
            'email': 'test@example.com',
            'password': hash_password('123456'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        user_diaries['test'] = []
        save_data()
        print("测试账号已创建: 用户名=test, 密码=123456")

create_test_account()



# 装饰器：检查登录状态
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    # 为装饰后的函数设置与原函数相同的名称，避免端点冲突
    decorated_function.__name__ = f.__name__
    return decorated_function

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            if users[username]['password'] == hash_password(password):
                session['user_id'] = username
                session['user_name'] = users[username]['name']
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='密码错误')
        else:
            return render_template('login.html', error='用户不存在')
    return render_template('login.html')

# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username in users:
            return render_template('register.html', error='用户名已存在')
        
        if password != confirm_password:
            return render_template('register.html', error='两次密码不一致')
        
        # 创建用户
        users[username] = {
            'name': username,
            'email': email,
            'password': hash_password(password),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 为用户创建日记列表
        user_diaries[username] = []
        
        save_data()
        
        return render_template('login.html', success='注册成功，请登录')
    return render_template('register.html')

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# 推荐页面
@app.route('/recommend')
@login_required
def recommend():
    return render_template('recommend.html')

# 路线规划页面
@app.route('/path')
@login_required
def path():
    return render_template('path.html')

# 场所查询页面
@app.route('/query')
@login_required
def query():
    return render_template('query.html')

# 日记管理页面
@app.route('/diary')
@login_required
def diary():
    return render_template('diary.html')

# 地图展示页面
@app.route('/map')
@login_required
def map_page():
    return render_template('map.html')



@app.route('/api/diary', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def diary_operations():
    username = session['user_id']
    
    if request.method == 'GET':
        diaries = user_diaries.get(username, [])
        return jsonify(diaries)
    
    elif request.method == 'POST':
        data = request.json
        new_diary = {
            'id': len(user_diaries.get(username, [])) + 1,
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if username not in user_diaries:
            user_diaries[username] = []
        
        user_diaries[username].append(new_diary)
        save_data()
        return jsonify({'id': new_diary['id']})
    
    elif request.method == 'PUT':
        data = request.json
        diary_id = int(data.get('id', 0))
        
        diaries = user_diaries.get(username, [])
        for diary in diaries:
            if diary['id'] == diary_id:
                diary['title'] = data.get('title', diary['title'])
                diary['content'] = data.get('content', diary['content'])
                diary['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_data()
                return jsonify({'success': True})
        return jsonify({'error': 'Diary not found'}), 404
    
    elif request.method == 'DELETE':
        diary_id = int(request.args.get('id', 0))
        
        diaries = user_diaries.get(username, [])
        user_diaries[username] = [d for d in diaries if d['id'] != diary_id]
        save_data()
        return jsonify({'success': True})

# 导出日记为文件
@app.route('/api/diary/export')
@login_required
def export_diary():
    username = session['user_id']
    diaries = user_diaries.get(username, [])
    
    # 生成JSON格式
    export_data = {
        'user': username,
        'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'diaries': diaries
    }
    
    return jsonify(export_data)

# 导入日记
@app.route('/api/diary/import', methods=['POST'])
@login_required
def import_diary():
    username = session['user_id']
    data = request.json
    
    if 'diaries' in data:
        imported_diaries = data['diaries']
        if username not in user_diaries:
            user_diaries[username] = []
        
        # 为导入的日记分配新ID
        next_id = len(user_diaries[username]) + 1
        for diary in imported_diaries:
            diary['id'] = next_id
            diary['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_diaries[username].append(diary)
            next_id += 1
        
        save_data()
        return jsonify({'success': True, 'imported': len(imported_diaries)})
    
    return jsonify({'error': 'Invalid data'}), 400

# 获取用户登录状态
@app.route('/api/user/status')
def get_user_status():
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session['user_id'],
            'user_name': session.get('user_name', session['user_id'])
        })
    else:
        return jsonify({'logged_in': False})

# API: 旅游推荐 - 景点
@app.route('/api/recommend/spots')
def recommend_spots():
    method = request.args.get('method', 'hot')
    n = int(request.args.get('n', 6))
    
    # 模拟数据
    spots = [
        {"id": 1, "name": "故宫", "rating": 4.2, "popularity": 98, "category": "文化景点", "location": "北京市东城区"},
        {"id": 2, "name": "长城", "rating": 4.7, "popularity": 95, "category": "自然景点", "location": "北京市怀柔区"},
        {"id": 3, "name": "颐和园", "rating": 4.6, "popularity": 90, "category": "文化景点", "location": "北京市海淀区"},
        {"id": 4, "name": "天坛", "rating": 4.8, "popularity": 85, "category": "文化景点", "location": "北京市东城区"},
        {"id": 5, "name": "天安门", "rating": 4.5, "popularity": 99, "category": "文化景点", "location": "北京市东城区"},
        {"id": 6, "name": "圆明园", "rating": 4.4, "popularity": 80, "category": "文化景点", "location": "北京市海淀区"}
    ]
    
    if method == 'rating':
        spots.sort(key=lambda x: x['rating'], reverse=True)
    else:  # hot
        spots.sort(key=lambda x: x['popularity'], reverse=True)
    
    return jsonify(spots[:n])

# API: 旅游推荐 - 美食
@app.route('/api/recommend/food')
def recommend_food():
    method = request.args.get('method', 'hot')
    n = int(request.args.get('n', 6))
    
    # 模拟数据
    food = [
        {"id": 1, "name": "北京烤鸭", "rating": 4.8, "popularity": 95, "category": "烤鸭", "location": "北京市东城区"},
        {"id": 2, "name": "炸酱面", "rating": 4.5, "popularity": 85, "category": "面食", "location": "北京市西城区"},
        {"id": 3, "name": "豆汁", "rating": 4.0, "popularity": 70, "category": "传统小吃", "location": "北京市东城区"},
        {"id": 4, "name": "炒肝", "rating": 4.3, "popularity": 75, "category": "传统小吃", "location": "北京市东城区"},
        {"id": 5, "name": "卤煮火烧", "rating": 4.4, "popularity": 80, "category": "传统小吃", "location": "北京市西城区"},
        {"id": 6, "name": "涮羊肉", "rating": 4.6, "popularity": 88, "category": "火锅", "location": "北京市朝阳区"}
    ]
    
    if method == 'rating':
        food.sort(key=lambda x: x['rating'], reverse=True)
    else:  # hot
        food.sort(key=lambda x: x['popularity'], reverse=True)
    
    return jsonify(food[:n])

# API: 旅游推荐 - 名校
@app.route('/api/recommend/universities')
def recommend_universities():
    method = request.args.get('method', 'hot')
    n = int(request.args.get('n', 6))
    
    # 模拟数据
    universities = [
        {"id": 1, "name": "北京大学", "rating": 4.9, "popularity": 98, "category": "高等学府", "location": "北京市海淀区"},
        {"id": 2, "name": "清华大学", "rating": 4.9, "popularity": 97, "category": "高等学府", "location": "北京市海淀区"},
        {"id": 3, "name": "复旦大学", "rating": 4.8, "popularity": 95, "category": "高等学府", "location": "上海市杨浦区"},
        {"id": 4, "name": "上海交通大学", "rating": 4.8, "popularity": 94, "category": "高等学府", "location": "上海市闵行区"},
        {"id": 5, "name": "浙江大学", "rating": 4.7, "popularity": 93, "category": "高等学府", "location": "浙江省杭州市"},
        {"id": 6, "name": "南京大学", "rating": 4.7, "popularity": 92, "category": "高等学府", "location": "江苏省南京市"}
    ]
    
    if method == 'rating':
        universities.sort(key=lambda x: x['rating'], reverse=True)
    else:  # hot
        universities.sort(key=lambda x: x['popularity'], reverse=True)
    
    return jsonify(universities[:n])

# API: 路线规划
@app.route('/api/path/plan', methods=['POST'])
def plan_path():
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    strategy = data.get('strategy', 'shortest')
    
    # 模拟数据
    path = [start, "中间点1", "中间点2", end]
    distance = 10000  # 10公里
    time = 30  # 30分钟
    transport = "公共交通"
    
    if strategy == 'fastest':
        time = 20
        transport = "出租车"
    elif strategy == 'least_crowded':
        distance = 12000
        time = 40
        transport = "共享单车"
    
    return jsonify({"path": path, "distance": distance, "time": time, "transport": transport})

# API: 场所查询
@app.route('/api/query/places', methods=['POST'])
def query_places():
    data = request.get_json()
    keyword = data.get('keyword', '')
    category = data.get('category', 'all')
    location = data.get('location', '')
    
    # 模拟数据
    places = [
        {"name": "故宫", "category": "景点", "location": "北京市东城区", "rating": 4.8, "description": "中国明清两代的皇家宫殿"},
        {"name": "长城", "category": "景点", "location": "北京市怀柔区", "rating": 4.7, "description": "中国古代伟大的防御工程"},
        {"name": "颐和园", "category": "景点", "location": "北京市海淀区", "rating": 4.6, "description": "中国古典园林"},
        {"name": "全聚德烤鸭店", "category": "餐厅", "location": "北京市东城区", "rating": 4.5, "description": "著名的北京烤鸭店"},
        {"name": "北京饭店", "category": "酒店", "location": "北京市东城区", "rating": 4.6, "description": "豪华五星级酒店"},
        {"name": "王府井步行街", "category": "购物", "location": "北京市东城区", "rating": 4.4, "description": "著名的商业街"},
        {"name": "北京站", "category": "交通", "location": "北京市东城区", "rating": 4.3, "description": "重要的铁路枢纽"},
        {"name": "北京南站", "category": "交通", "location": "北京市丰台区", "rating": 4.4, "description": "现代化高铁站"}
    ]
    
    # 过滤结果
    filtered_places = []
    for place in places:
        if keyword and keyword not in place['name']:
            continue
        if category != 'all' and place['category'] != category:
            continue
        if location and location not in place['location']:
            continue
        filtered_places.append(place)
    
    return jsonify(filtered_places)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
