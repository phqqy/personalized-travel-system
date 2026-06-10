#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Agent 共享基类
使用 DeepSeek API（OpenAI 兼容格式）
"""

import os
import sys
from openai import OpenAI


def load_env_from_project():
    """从项目根目录的 .env 加载环境变量"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    env_path = os.path.join(project_dir, '.env')

    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key not in os.environ:
                        os.environ[key] = value
        return True
    return False


# 自动加载 .env
load_env_from_project()

# DeepSeek 客户端
_client = None


def get_client():
    """获取 DeepSeek 客户端（懒加载）"""
    global _client
    if _client is None:
        api_key = os.environ.get('DEEPSEEK_API_KEY', '')
        if not api_key:
            print("错误: 未设置 DEEPSEEK_API_KEY")
            print("请在 .env 中添加: DEEPSEEK_API_KEY=sk-xxxxxxxx")
            print("注册地址: https://platform.deepseek.com")
            sys.exit(1)

        _client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
    return _client


class Agent:
    """通用 AI Agent，通过 System Prompt 定制角色"""

    def __init__(self, system_prompt, model="deepseek-chat"):
        self.system_prompt = system_prompt
        self.model = model
        self.client = get_client()

    def ask(self, user_message, temperature=0.7, max_tokens=4096):
        """
        向 Agent 提问

        Args:
            user_message: 用户输入
            temperature: 随机性 (0-2)
            max_tokens: 最大返回长度

        Returns:
            Agent 的回复文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Agent 调用失败] {str(e)}"

    def stream(self, user_message):
        """流式输出回复"""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    print(chunk.choices[0].delta.content, end='', flush=True)
            print()  # 换行
        except Exception as e:
            print(f"\n[Agent 调用失败] {str(e)}")
