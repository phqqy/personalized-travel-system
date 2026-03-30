#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
个性化旅游系统主入口
"""

import os
import sys
import subprocess


def main():
    """主函数，启动整个系统"""
    # 确保数据目录存在
    ensure_directories()
    
    # 启动Web应用
    print("启动个性化旅游系统Web版...")
    print("请在浏览器中访问: http://localhost:5000")
    print("按 Ctrl+C 停止系统")
    
    # 切换到web_app目录并启动
    web_app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_app")
    os.chdir(web_app_dir)
    
    try:
        subprocess.run([sys.executable, "start.py"], check=True)
    except KeyboardInterrupt:
        print("\n系统已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)


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
        "web_app",
        "web_app/templates"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)


if __name__ == "__main__":
    main()
