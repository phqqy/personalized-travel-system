#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件工具模块
"""

import os
import shutil
from PIL import Image


def resize_image(image_path, output_path, max_size=1024):
    """
    调整图片大小
    
    Args:
        image_path: 图片路径
        output_path: 输出路径
        max_size: 最大尺寸（宽度或高度）
    
    Returns:
        是否成功调整大小
    """
    try:
        img = Image.open(image_path)
        
        # 计算新尺寸
        width, height = img.size
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        # 调整大小
        resized_img = img.resize((new_width, new_height))
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存图片
        resized_img.save(output_path)
        return True
    except Exception as e:
        print(f"调整图片大小出错: {e}")
        return False


def get_file_size(file_path):
    """
    获取文件大小
    
    Args:
        file_path: 文件路径
    
    Returns:
        文件大小（字节）
    """
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0


def delete_file(file_path):
    """
    删除文件
    
    Args:
        file_path: 文件路径
    
    Returns:
        是否成功删除
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"删除文件出错: {e}")
            return False
    return True


def copy_file(src, dst):
    """
    复制文件
    
    Args:
        src: 源文件路径
        dst: 目标文件路径
    
    Returns:
        是否成功复制
    """
    try:
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"复制文件出错: {e}")
        return False
