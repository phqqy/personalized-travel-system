#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主界面模块
"""

import tkinter as tk
from tkinter import ttk
from gui.map_window import MapWindow
from gui.nav_window import NavWindow
from gui.diary_window import DiaryWindow
from gui.recommend_window import RecommendWindow


class MainWindow:
    """主界面类"""
    
    def __init__(self, root):
        """
        初始化主界面
        
        Args:
            root: 根窗口
        """
        self.root = root
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 设置窗口标题和大小
        self.root.title("个性化旅游系统")
        self.root.geometry("1000x700")
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标题
        title_label = ttk.Label(
            main_frame, 
            text="个性化旅游系统", 
            font=("SimHei", 24, "bold")
        )
        title_label.pack(pady=30)
        
        # 创建功能按钮框架
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # 创建功能按钮
        button_width = 20
        button_height = 2
        
        # 旅游推荐按钮
        recommend_btn = ttk.Button(
            buttons_frame, 
            text="旅游推荐", 
            width=button_width,
            command=self.open_recommend_window
        )
        recommend_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 路线规划按钮
        nav_btn = ttk.Button(
            buttons_frame, 
            text="路线规划", 
            width=button_width,
            command=self.open_nav_window
        )
        nav_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 地图展示按钮
        map_btn = ttk.Button(
            buttons_frame, 
            text="地图展示", 
            width=button_width,
            command=self.open_map_window
        )
        map_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 日记管理按钮
        diary_btn = ttk.Button(
            buttons_frame, 
            text="日记管理", 
            width=button_width,
            command=self.open_diary_window
        )
        diary_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 创建状态标签
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=20)
        
        self.status_label = ttk.Label(
            status_frame, 
            text="欢迎使用个性化旅游系统！", 
            font=("SimHei", 12)
        )
        self.status_label.pack(side=tk.LEFT)
    
    def open_recommend_window(self):
        """打开推荐窗口"""
        recommend_window = RecommendWindow(self.root)
        self.status_label.config(text="打开旅游推荐窗口")
    
    def open_nav_window(self):
        """打开导航窗口"""
        nav_window = NavWindow(self.root)
        self.status_label.config(text="打开路线规划窗口")
    
    def open_map_window(self):
        """打开地图窗口"""
        map_window = MapWindow(self.root)
        self.status_label.config(text="打开地图展示窗口")
    
    def open_diary_window(self):
        """打开日记窗口"""
        diary_window = DiaryWindow(self.root)
        self.status_label.config(text="打开日记管理窗口")
