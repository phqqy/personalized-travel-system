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
    print("启动个性化旅游系统Web版...")
    print("请在浏览器中访问: http://localhost:5000")
    print("按 Ctrl+C 停止系统")
    
    try:
        project_dir = os.path.dirname(os.path.abspath(__file__))
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


if __name__ == "__main__":
    main()
