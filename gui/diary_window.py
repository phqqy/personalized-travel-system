#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记管理窗口模块
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class DiaryWindow:
    """日记管理窗口类"""
    
    def __init__(self, parent):
        """
        初始化日记窗口
        
        Args:
            parent: 父窗口
        """
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("日记管理")
        self.window.geometry("900x600")
        self.create_widgets()
        self.diaries = []  # 模拟日记数据
        self.load_sample_diaries()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建左侧日记列表
        left_frame = ttk.LabelFrame(main_frame, text="日记列表", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, pady=10, ipadx=10)
        
        # 日记列表
        self.diary_list = tk.Listbox(left_frame, width=40, height=20)
        self.diary_list.pack(fill=tk.BOTH, expand=True, pady=5)
        self.diary_list.bind('<<ListboxSelect>>', self.on_diary_select)
        
        # 列表按钮
        list_buttons_frame = ttk.Frame(left_frame)
        list_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(list_buttons_frame, text="新建", command=self.create_diary).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_buttons_frame, text="删除", command=self.delete_diary).pack(side=tk.LEFT, padx=5)
        ttk.Button(list_buttons_frame, text="刷新", command=self.refresh_diary_list).pack(side=tk.LEFT, padx=5)
        
        # 创建右侧日记内容
        right_frame = ttk.LabelFrame(main_frame, text="日记内容", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)
        
        # 标题输入
        title_frame = ttk.Frame(right_frame)
        title_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(title_frame, text="标题:", width=10).pack(side=tk.LEFT, padx=5)
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(title_frame, textvariable=self.title_var)
        title_entry.pack(fill=tk.X, padx=5)
        
        # 内容输入
        content_frame = ttk.Frame(right_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(content_frame, text="内容:", width=10).pack(side=tk.LEFT, padx=5, anchor=tk.N)
        self.content_text = tk.Text(content_frame, wrap=tk.WORD)
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # 内容按钮
        content_buttons_frame = ttk.Frame(right_frame)
        content_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(content_buttons_frame, text="保存", command=self.save_diary).pack(side=tk.RIGHT, padx=5)
        ttk.Button(content_buttons_frame, text="清空", command=self.clear_diary).pack(side=tk.RIGHT, padx=5)
    
    def load_sample_diaries(self):
        """加载示例日记"""
        self.diaries = [
            {"id": 1, "title": "第一次旅行", "content": "这是我的第一次旅行，非常开心！"},
            {"id": 2, "title": "美食之旅", "content": "今天品尝了很多当地美食，回味无穷。"},
            {"id": 3, "title": "登山记", "content": "登上山顶，一览众山小，感觉非常棒！"}
        ]
        self.refresh_diary_list()
    
    def refresh_diary_list(self):
        """刷新日记列表"""
        # 清空列表
        self.diary_list.delete(0, tk.END)
        
        # 添加日记
        for diary in self.diaries:
            self.diary_list.insert(tk.END, diary["title"])
    
    def on_diary_select(self, event):
        """选择日记"""
        selection = self.diary_list.curselection()
        if selection:
            index = selection[0]
            diary = self.diaries[index]
            self.title_var.set(diary["title"])
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(tk.END, diary["content"])
    
    def create_diary(self):
        """新建日记"""
        self.title_var.set("")
        self.content_text.delete(1.0, tk.END)
    
    def save_diary(self):
        """保存日记"""
        title = self.title_var.get()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showerror("错误", "请输入标题")
            return
        
        # 检查是否是编辑现有日记
        selection = self.diary_list.curselection()
        if selection:
            index = selection[0]
            self.diaries[index]["title"] = title
            self.diaries[index]["content"] = content
        else:
            # 新建日记
            new_id = len(self.diaries) + 1
            new_diary = {"id": new_id, "title": title, "content": content}
            self.diaries.append(new_diary)
        
        self.refresh_diary_list()
        messagebox.showinfo("成功", "日记保存成功")
    
    def delete_diary(self):
        """删除日记"""
        selection = self.diary_list.curselection()
        if selection:
            index = selection[0]
            if messagebox.askyesno("确认", "确定要删除这篇日记吗？"):
                del self.diaries[index]
                self.refresh_diary_list()
                self.clear_diary()
                messagebox.showinfo("成功", "日记删除成功")
        else:
            messagebox.showerror("错误", "请选择要删除的日记")
    
    def clear_diary(self):
        """清空日记"""
        self.title_var.set("")
        self.content_text.delete(1.0, tk.END)
