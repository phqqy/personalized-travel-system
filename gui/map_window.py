#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
地图展示窗口模块
"""

import tkinter as tk
from tkinter import ttk


class MapWindow:
    """地图展示窗口类"""
    
    def __init__(self, parent):
        """
        初始化地图窗口
        
        Args:
            parent: 父窗口
        """
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("地图展示")
        self.window.geometry("900x600")
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建地图展示区域
        map_frame = ttk.LabelFrame(main_frame, text="地图", padding="10")
        map_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 地图画布
        self.map_canvas = tk.Canvas(map_frame, bg="#ecf0f1")
        self.map_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绘制示例地图
        self.draw_sample_map()
        
        # 创建控制区域
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # 缩放控制
        zoom_frame = ttk.Frame(control_frame)
        zoom_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(zoom_frame, text="缩放:").pack(side=tk.LEFT, padx=5)
        self.zoom_scale = ttk.Scale(
            zoom_frame, 
            from_=1, 
            to=5, 
            orient=tk.HORIZONTAL, 
            length=100
        )
        self.zoom_scale.set(1)
        self.zoom_scale.pack(side=tk.LEFT, padx=5)
        
        # 地图类型选择
        map_type_frame = ttk.Frame(control_frame)
        map_type_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(map_type_frame, text="地图类型:").pack(side=tk.LEFT, padx=5)
        self.map_type_var = tk.StringVar()
        map_type_combo = ttk.Combobox(
            map_type_frame, 
            textvariable=self.map_type_var,
            values=["标准地图", "卫星地图", "地形地图"]
        )
        map_type_combo.current(0)
        map_type_combo.pack(side=tk.LEFT, padx=5)
        
        # 刷新按钮
        refresh_btn = ttk.Button(control_frame, text="刷新", command=self.refresh_map)
        refresh_btn.pack(side=tk.RIGHT, padx=10)
    
    def draw_sample_map(self):
        """绘制示例地图"""
        # 绘制道路
        self.map_canvas.create_line(100, 100, 800, 100, width=3, fill="#95a5a6")
        self.map_canvas.create_line(100, 200, 800, 200, width=3, fill="#95a5a6")
        self.map_canvas.create_line(100, 300, 800, 300, width=3, fill="#95a5a6")
        self.map_canvas.create_line(100, 400, 800, 400, width=3, fill="#95a5a6")
        
        self.map_canvas.create_line(100, 100, 100, 400, width=3, fill="#95a5a6")
        self.map_canvas.create_line(300, 100, 300, 400, width=3, fill="#95a5a6")
        self.map_canvas.create_line(500, 100, 500, 400, width=3, fill="#95a5a6")
        self.map_canvas.create_line(700, 100, 700, 400, width=3, fill="#95a5a6")
        
        # 绘制景点
        spots = [
            (200, 150, "景点A"),
            (400, 250, "景点B"),
            (600, 150, "景点C"),
            (200, 350, "景点D"),
            (600, 350, "景点E")
        ]
        
        for x, y, name in spots:
            self.map_canvas.create_oval(x-10, y-10, x+10, y+10, fill="#3498db")
            self.map_canvas.create_text(x, y-15, text=name, fill="#2c3e50")
        
        # 绘制路径示例
        self.map_canvas.create_line(200, 150, 400, 250, 600, 350, width=2, fill="#e74c3c", arrow=tk.LAST)
    
    def refresh_map(self):
        """刷新地图"""
        # 清除画布
        self.map_canvas.delete("all")
        # 重新绘制地图
        self.draw_sample_map()
