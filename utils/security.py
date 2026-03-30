#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
安全工具模块
"""

import hashlib


class Security:
    """安全工具类"""
    
    @staticmethod
    def hash_password(password):
        """
        密码哈希加密
        
        Args:
            password: 明文密码
        
        Returns:
            SHA256哈希值
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed_password):
        """
        验证密码
        
        Args:
            password: 明文密码
            hashed_password: 哈希值
        
        Returns:
            是否匹配
        """
        return Security.hash_password(password) == hashed_password
