#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试视频URL是否可访问
"""

import requests

video_url = "https://v26-aiop.aigc-cloud.com/7cd41210f44b5cda1607f7ca1901648c/6a0353bb/video/tos/cn/tos-cn-v-242bcc/9aa8a03d2aa542149a4a90711bc94a53/?a=764792&ch=0&cr=0&dr=0&er=0&lr=default&cd=0%7C0%7C0%7C0&br=5475&bt=5475&cs=0&ds=3&ft=GbtG6uO3pyygZmo0PaKIUgkVQ9w6x&mime_type=video_mp4&qs=13&rc=anJudjZrb2luOzgzNGczM0BpanJudjZrb2luOzgzNGczM0BsbmRscWduMi5hLS1kXi9zYSNsbmRscWduMi5hLS1kXi9zcw%3D%3D&btag=c0000e00008000&dy_q=1778599334&l=20260512232214A9F3416B77DBC4185075"

print("=== 测试视频URL ===")
print(f"URL: {video_url[:100]}...")

try:
    response = requests.head(video_url, timeout=10, allow_redirects=True)
    print(f"\n状态码: {response.status_code}")
    print(f"Headers:")
    for key, value in response.headers.items():
        if key.lower() in ['content-type', 'content-length', 'content-disposition']:
            print(f"  {key}: {value}")

    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        content_length = response.headers.get('Content-Length', 'Unknown')
        print(f"\n✓ 视频URL有效!")
        print(f"  Content-Type: {content_type}")
        print(f"  Content-Length: {content_length} bytes")

        if 'video' in content_type:
            print("  这是一个有效的视频文件!")
        else:
            print("  警告: Content-Type不是视频类型")
    else:
        print(f"\n✗ 视频URL无效，状态码: {response.status_code}")

except Exception as e:
    print(f"\n✗ 错误: {str(e)}")