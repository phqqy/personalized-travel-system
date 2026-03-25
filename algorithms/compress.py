#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
无损压缩模块
"""

import zlib
import base64


def compress_data(data, level=6):
    """
    压缩数据
    
    Args:
        data: 待压缩的数据（字符串或字节）
        level: 压缩级别（1-9）
    
    Returns:
        压缩后的Base64编码字符串
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    compressed = zlib.compress(data, level)
    return base64.b64encode(compressed).decode('utf-8')


def decompress_data(compressed_data):
    """
    解压缩数据
    
    Args:
        compressed_data: 压缩后的Base64编码字符串
    
    Returns:
        解压后的字符串
    """
    compressed = base64.b64decode(compressed_data)
    decompressed = zlib.decompress(compressed)
    return decompressed.decode('utf-8')


def should_compress(data, min_size=1024):
    """
    判断是否应该压缩
    
    Args:
        data: 待压缩的数据
        min_size: 最小压缩大小（字节）
    
    Returns:
        是否应该压缩
    """
    if isinstance(data, str):
        data_size = len(data.encode('utf-8'))
    else:
        data_size = len(data)
    
    return data_size >= min_size
