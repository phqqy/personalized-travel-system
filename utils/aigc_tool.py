#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AIGC动画生成工具模块
"""

import os
from PIL import Image
import cv2
import numpy as np


def create_travel_animation(images, output_path, duration=300):
    """
    将照片转换为旅游动画
    
    Args:
        images: 图片路径列表
        output_path: 输出视频路径
        duration: 每张图片的显示时长（毫秒）
    
    Returns:
        是否成功生成动画
    """
    if not images:
        return False
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 读取第一张图片获取尺寸
    first_image = Image.open(images[0])
    width, height = first_image.size
    
    # 创建视频 writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 1000 / duration
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # 处理每张图片
    for image_path in images:
        try:
            # 读取图片
            img = Image.open(image_path)
            img = img.resize((width, height))
            
            # 转换为 OpenCV 格式
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # 写入视频
            out.write(img_cv)
        except Exception as e:
            print(f"处理图片 {image_path} 时出错: {e}")
            continue
    
    # 释放资源
    out.release()
    
    return os.path.exists(output_path)


def add_transition_effects(video_path, output_path):
    """
    为视频添加过渡效果
    
    Args:
        video_path: 原始视频路径
        output_path: 输出视频路径
    
    Returns:
        是否成功添加效果
    """
    # 这里简化处理，实际应用中可以添加更复杂的过渡效果
    # 目前只是复制原始视频
    if os.path.exists(video_path):
        import shutil
        shutil.copy2(video_path, output_path)
        return True
    return False
