#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
推荐窗口模块
"""

import tkinter as tk
from tkinter import ttk


class RecommendWindow:
    """推荐窗口类"""
    
    def __init__(self, parent):
        """
        初始化推荐窗口
        
        Args:
            parent: 父窗口
        """
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("旅游推荐")
        self.window.geometry("900x600")
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 景点推荐选项卡
        spot_tab = ttk.Frame(notebook)
        notebook.add(spot_tab, text="景点推荐")
        self.create_spot_tab(spot_tab)
        
        # 美食推荐选项卡
        food_tab = ttk.Frame(notebook)
        notebook.add(food_tab, text="美食推荐")
        self.create_food_tab(food_tab)
        
        # 场所查询选项卡
        query_tab = ttk.Frame(notebook)
        notebook.add(query_tab, text="场所查询")
        self.create_query_tab(query_tab)
    
    def create_spot_tab(self, parent):
        """创建景点推荐选项卡"""
        # 创建推荐方式选择
        method_frame = ttk.Frame(parent, padding="10")
        method_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(method_frame, text="推荐方式:", width=10).pack(side=tk.LEFT, padx=5)
        self.spot_method_var = tk.StringVar()
        method_combo = ttk.Combobox(
            method_frame, 
            textvariable=self.spot_method_var,
            values=["热度推荐", "评分推荐", "兴趣推荐"]
        )
        method_combo.current(0)
        method_combo.pack(side=tk.LEFT, padx=5, width=20)
        
        # 兴趣标签（仅在兴趣推荐时显示）
        self.interest_frame = ttk.Frame(parent, padding="10")
        
        ttk.Label(self.interest_frame, text="兴趣标签:", width=10).pack(side=tk.LEFT, padx=5)
        self.interest_var = tk.StringVar()
        interest_combo = ttk.Combobox(
            self.interest_frame, 
            textvariable=self.interest_var,
            values=["自然风光", "历史文化", "娱乐休闲", "美食购物"]
        )
        interest_combo.current(0)
        interest_combo.pack(side=tk.LEFT, padx=5, width=20)
        
        # 推荐按钮
        recommend_btn = ttk.Button(method_frame, text="推荐", command=self.recommend_spots)
        recommend_btn.pack(side=tk.RIGHT, padx=10)
        
        # 推荐结果
        result_frame = ttk.LabelFrame(parent, text="推荐结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.spot_list = tk.Listbox(result_frame, height=15)
        self.spot_list.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def create_food_tab(self, parent):
        """创建美食推荐选项卡"""
        # 创建推荐方式选择
        method_frame = ttk.Frame(parent, padding="10")
        method_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(method_frame, text="推荐方式:", width=10).pack(side=tk.LEFT, padx=5)
        self.food_method_var = tk.StringVar()
        method_combo = ttk.Combobox(
            method_frame, 
            textvariable=self.food_method_var,
            values=["热度推荐", "评分推荐", "分类推荐"]
        )
        method_combo.current(0)
        method_combo.pack(side=tk.LEFT, padx=5, width=20)
        
        # 分类选择（仅在分类推荐时显示）
        self.food_category_frame = ttk.Frame(parent, padding="10")
        
        ttk.Label(self.food_category_frame, text="美食分类:", width=10).pack(side=tk.LEFT, padx=5)
        self.food_category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            self.food_category_frame, 
            textvariable=self.food_category_var,
            values=["川菜", "粤菜", "鲁菜", "淮扬菜", "西餐", "日料"]
        )
        category_combo.current(0)
        category_combo.pack(side=tk.LEFT, padx=5, width=20)
        
        # 推荐按钮
        recommend_btn = ttk.Button(method_frame, text="推荐", command=self.recommend_food)
        recommend_btn.pack(side=tk.RIGHT, padx=10)
        
        # 推荐结果
        result_frame = ttk.LabelFrame(parent, text="推荐结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.food_list = tk.Listbox(result_frame, height=15)
        self.food_list.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def create_query_tab(self, parent):
        """创建场所查询选项卡"""
        # 创建查询条件
        query_frame = ttk.Frame(parent, padding="10")
        query_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(query_frame, text="查询关键词:", width=10).pack(side=tk.LEFT, padx=5)
        self.query_var = tk.StringVar()
        query_entry = ttk.Entry(query_frame, textvariable=self.query_var, width=40)
        query_entry.pack(side=tk.LEFT, padx=5)
        
        # 查询按钮
        query_btn = ttk.Button(query_frame, text="查询", command=self.query_places)
        query_btn.pack(side=tk.RIGHT, padx=10)
        
        # 查询结果
        result_frame = ttk.LabelFrame(parent, text="查询结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.query_list = tk.Listbox(result_frame, height=15)
        self.query_list.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def recommend_spots(self):
        """推荐景点"""
        method = self.spot_method_var.get()
        
        # 模拟推荐结果
        if method == "热度推荐":
            spots = ["故宫博物院", "长城", "颐和园", "西湖", "黄山"]
        elif method == "评分推荐":
            spots = ["九寨沟", "张家界", "丽江古城", "三亚湾", "鼓浪屿"]
        else:  # 兴趣推荐
            interest = self.interest_var.get()
            spots = [f"{interest}景点1", f"{interest}景点2", f"{interest}景点3", f"{interest}景点4", f"{interest}景点5"]
        
        # 更新结果
        self.spot_list.delete(0, tk.END)
        for spot in spots:
            self.spot_list.insert(tk.END, spot)
    
    def recommend_food(self):
        """推荐美食"""
        method = self.food_method_var.get()
        
        # 模拟推荐结果
        if method == "热度推荐":
            foods = ["北京烤鸭", "四川火锅", "广东早茶", "西湖醋鱼", "南京盐水鸭"]
        elif method == "评分推荐":
            foods = ["宫保鸡丁", "麻婆豆腐", "红烧狮子头", "清蒸鲈鱼", "糖醋里脊"]
        else:  # 分类推荐
            category = self.food_category_var.get()
            foods = [f"{category}菜品1", f"{category}菜品2", f"{category}菜品3", f"{category}菜品4", f"{category}菜品5"]
        
        # 更新结果
        self.food_list.delete(0, tk.END)
        for food in foods:
            self.food_list.insert(tk.END, food)
    
    def query_places(self):
        """查询场所"""
        query = self.query_var.get()
        
        # 模拟查询结果
        if not query:
            places = ["请输入查询关键词"]
        else:
            places = [f"{query}场所1", f"{query}场所2", f"{query}场所3", f"{query}场所4", f"{query}场所5"]
        
        # 更新结果
        self.query_list.delete(0, tk.END)
        for place in places:
            self.query_list.insert(tk.END, place)
