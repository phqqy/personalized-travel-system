#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coder Agent — 编码智能体
用法: python scripts/coder_agent.py "你的编码任务"
"""

import sys
from agent_base import Agent

CODER_SYSTEM_PROMPT = """你是一位资深的 Python 全栈开发专家，精通以下技术栈：
- 后端: Python、Flask、FastAPI
- 前端: Vue 3、HTML/CSS/JavaScript
- 数据库: SQLite、MySQL、PostgreSQL
- 测试: pytest、unittest
- 工具: Git、Docker、RESTful API 设计

你的任务是根据用户的需求，编写高质量、可运行的代码。请遵循以下原则：
1. 代码简洁清晰，注释恰当
2. 遵循 PEP 8 编码规范
3. 包含必要的错误处理
4. 优先使用标准库和常见依赖
5. 输出完整可直接使用的代码
6. 用中文简要说明代码的设计思路
"""


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/coder_agent.py \"你的编码任务\"")
        print()
        print("示例:")
        print('  python scripts/coder_agent.py "写一个Python函数对list去重并保持顺序"')
        print('  python scripts/coder_agent.py "创建一个Flask API端点返回用户列表"')
        sys.exit(1)

    task = sys.argv[1]
    agent = Agent(CODER_SYSTEM_PROMPT, model="deepseek-chat")

    print("=" * 60)
    print(f"任务: {task}")
    print("=" * 60)
    print()

    agent.stream(task)


if __name__ == '__main__':
    main()
