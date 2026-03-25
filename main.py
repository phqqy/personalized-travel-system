#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
个性化旅游系统主入口
"""

import os
import sys
from gui.main_window import MainWindow
import tkinter as tk


def main():
    """主函数，启动整个系统"""
    # 确保数据目录存在
    ensure_directories()
    
    # 初始化主窗口
    root = tk.Tk()
    root.title("个性化旅游系统")
    root.geometry("1000x700")
    
    # 创建并显示主窗口
    app = MainWindow(root)
    
    # 启动主循环
    root.mainloop()


def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        "data/raw",
        "data/graph",
        "data/db",
        "data/static/images",
        "data/static/maps",
        "data/static/diaries",
        "config",
        "algorithms",
        "utils",
        "services",
        "gui"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)


if __name__ == "__main__":
    main()
