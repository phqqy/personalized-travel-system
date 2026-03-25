#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
导航界面模块
"""

import tkinter as tk
from tkinter import ttk


class NavWindow:
    """导航界面类"""
    
    def __init__(self, parent):
        """
        初始化导航窗口
        
        Args:
            parent: 父窗口
        """
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("路线规划")
        self.window.geometry("800x500")
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建输入区域
        input_frame = ttk.LabelFrame(main_frame, text="路线规划", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        # 起点输入
        start_frame = ttk.Frame(input_frame)
        start_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(start_frame, text="起点:", width=10).pack(side=tk.LEFT, padx=5)
        self.start_var = tk.StringVar()
        start_entry = ttk.Entry(start_frame, textvariable=self.start_var, width=40)
        start_entry.pack(side=tk.LEFT, padx=5)
        
        # 终点输入
        end_frame = ttk.Frame(input_frame)
        end_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(end_frame, text="终点:", width=10).pack(side=tk.LEFT, padx=5)
        self.end_var = tk.StringVar()
        end_entry = ttk.Entry(end_frame, textvariable=self.end_var, width=40)
        end_entry.pack(side=tk.LEFT, padx=5)
        
        # 规划策略
        strategy_frame = ttk.Frame(input_frame)
        strategy_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(strategy_frame, text="规划策略:", width=10).pack(side=tk.LEFT, padx=5)
        self.strategy_var = tk.StringVar()
        strategy_combo = ttk.Combobox(
            strategy_frame, 
            textvariable=self.strategy_var,
            values=["最短距离", "最快时间", "最少拥挤"]
        )
        strategy_combo.current(0)
        strategy_combo.pack(side=tk.LEFT, padx=5, width=20)
        
        # 交通工具
        transport_frame = ttk.Frame(input_frame)
        transport_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(transport_frame, text="交通工具:", width=10).pack(side=tk.LEFT, padx=5)
        self.transport_var = tk.StringVar()
        transport_combo = ttk.Combobox(
            transport_frame, 
            textvariable=self.transport_var,
            values=["步行", "骑行", "驾车"]
        )
        transport_combo.current(0)
        transport_combo.pack(side=tk.LEFT, padx=5, width=20)
        
        # 规划按钮
        plan_btn = ttk.Button(input_frame, text="规划路线", command=self.plan_route)
        plan_btn.pack(side=tk.RIGHT, padx=10)
        
        # 创建结果区域
        result_frame = ttk.LabelFrame(main_frame, text="规划结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 路径信息
        self.path_info = ttk.Label(result_frame, text="请输入起点和终点并点击规划路线", font=("SimHei", 12))
        self.path_info.pack(pady=10)
        
        # 路径列表
        self.path_list = tk.Listbox(result_frame, height=10)
        self.path_list.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def plan_route(self):
        """规划路线"""
        start = self.start_var.get()
        end = self.end_var.get()
        strategy = self.strategy_var.get()
        transport = self.transport_var.get()
        
        if not start or not end:
            self.path_info.config(text="请输入起点和终点")
            return
        
        # 模拟路线规划结果
        path = [
            f"从 {start} 出发",
            "沿主干道向东行驶",
            "左转进入公园路",
            f"到达 {end}"
        ]
        
        # 更新界面
        self.path_info.config(text=f"规划策略: {strategy}, 交通工具: {transport}")
        
        # 清空列表
        self.path_list.delete(0, tk.END)
        
        # 添加路径
        for step in path:
            self.path_list.insert(tk.END, step)
