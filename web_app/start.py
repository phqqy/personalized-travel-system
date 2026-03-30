#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
个性化旅游系统 - 启动脚本
"""

import os
import sys
import subprocess


def print_banner():
    """打印启动横幅"""
    print("=" * 50)
    print("个性化旅游系统 - 整合版Web前端")
    print("=" * 50)
    print("正在启动系统...")


def check_dependencies():
    """检查依赖项"""
    print("检查依赖项...")
    try:
        import flask
        print("所有依赖项已安装")
    except ImportError as e:
        print(f"缺少依赖项: {e}")
        print("正在安装依赖项...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "Flask"], 
                          check=True, capture_output=True)
            print("依赖项安装成功")
        except subprocess.CalledProcessError:
            print("依赖项安装失败，请手动运行:")
            print("  pip install Flask")
            sys.exit(1)


def start_app():
    """启动Flask应用"""
    print("启动Flask应用...")
    try:
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_dir)
        from backend.app import main
        main()
    except KeyboardInterrupt:
        print("\n系统已停止")
    except Exception as e:
        print(f"启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """主函数"""
    print_banner()
    check_dependencies()
    print("\n系统启动成功！")
    print("请在浏览器中访问: http://localhost:5000")
    print("\n按 Ctrl+C 停止系统")
    print("=" * 50)
    start_app()


if __name__ == "__main__":
    main()
