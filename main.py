#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
个性化旅游系统主入口
"""

import os
import sys
import subprocess


def load_env():
    """加载.env环境变量文件"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"已加载环境变量文件: {env_path}")

        # ========== 验证API密钥配置 ==========
        ak = os.environ.get('VOLCENGINE_ACCESS_KEY', '')
        sk = os.environ.get('VOLCENGINE_SECRET_KEY', '')

        if not ak or not sk:
            print("=" * 60)
            print("[WARNING] 火山引擎API密钥未完整配置！")
            print("   即梦AI视频生成功能将不可用。")
            print("   请在 .env 文件中配置以下变量：")
            print("     VOLCENGINE_ACCESS_KEY=你的AccessKey")
            print("     VOLCENGINE_SECRET_KEY=你的SecretKey")
            print("   获取地址: https://console.volcengine.com/iam/keymanage")
            print("   开通即梦服务: https://console.volcengine.com/visual/experience")
            print("=" * 60)
        else:
            masked_ak = ak[:8] + '***' + ak[-4:] if len(ak) > 12 else '***'
            print(f"  火山引擎 Access Key: {masked_ak} [OK]")
            print(f"  火山引擎 Secret Key: (已设置) [OK]")
            print("  提示: 如遇 Access Denied 错误，请确认已开通即梦AI服务")
            print("  https://console.volcengine.com/visual/experience")

        amap_key = os.environ.get('AMAP_API_KEY', '')
        if amap_key:
            print(f"  高德地图 API Key: {amap_key[:8]}*** [OK]")
        else:
            print("[WARNING] 高德地图API密钥未配置，地图功能可能受限")
    else:
        print(f"未找到环境变量文件: {env_path}")
        print("=" * 60)
        print("[WARNING] 未找到 .env 配置文件！")
        print("   请复制 .env.example 为 .env 并填入你的API密钥")
        print("=" * 60)


def main():
    """主函数，启动整个系统"""
    print("启动个性化旅游系统Web版...")
    print("请在浏览器中访问: http://localhost:5000")
    print("按 Ctrl+C 停止系统")
    
    # 加载环境变量
    load_env()
    
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
