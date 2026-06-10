#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tester Agent — 测试智能体
用法: python scripts/tester_agent.py "要测试的代码或功能描述"
"""

import sys
from agent_base import Agent

TESTER_SYSTEM_PROMPT = """你是一位资深的软件测试工程师，专精于：
- 单元测试: pytest、unittest
- 集成测试、端到端测试
- 边界条件分析、异常路径覆盖
- Mock/Stub 设计
- 性能测试建议

你的任务是对用户提供的代码或功能描述，编写全面的测试用例。请遵循：
1. 使用 pytest 框架
2. 覆盖正常路径、边界条件、异常情况
3. 测试函数命名清晰，注释说明测试意图
4. 使用 fixture 和 parametrize 减少重复
5. 给出可以直接运行的完整测试文件
6. 用中文简要说明测试策略和覆盖范围
"""


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/tester_agent.py \"要测试的代码或功能\"")
        print()
        print("示例:")
        print('  python scripts/tester_agent.py "def add(a,b): return a+b"')
        print('  python scripts/tester_agent.py "一个用户登录API，接收username和password，返回token"')
        sys.exit(1)

    task = sys.argv[1]
    agent = Agent(TESTER_SYSTEM_PROMPT, model="deepseek-chat")

    print("=" * 60)
    print(f"测试任务: {task}")
    print("=" * 60)
    print()

    agent.stream(task)


if __name__ == '__main__':
    main()
