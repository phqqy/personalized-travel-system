#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户服务模块
"""

from datetime import datetime
from config.settings import config
from utils.storage import DataStorage
from utils.security import Security


class UserService:
    """用户服务类"""
    
    def __init__(self):
        self.users = DataStorage.load_data(config.USER_DATA_FILE, {})
    
    def save(self):
        """保存用户数据"""
        DataStorage.save_data(config.USER_DATA_FILE, self.users)
    
    def get_user(self, username):
        """
        获取用户信息
        
        Args:
            username: 用户名
        
        Returns:
            用户信息字典或None
        """
        return self.users.get(username)
    
    def user_exists(self, username):
        """
        检查用户是否存在
        
        Args:
            username: 用户名
        
        Returns:
            是否存在
        """
        return username in self.users
    
    def verify_user(self, username, password):
        """
        验证用户密码
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            是否验证成功
        """
        user = self.get_user(username)
        if user:
            return Security.verify_password(password, user['password'])
        return False
    
    def create_user(self, username, email, password):
        """
        创建新用户
        
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
        
        Returns:
            是否创建成功
        """
        if self.user_exists(username):
            return False
        
        self.users[username] = {
            'name': username,
            'email': email,
            'password': Security.hash_password(password),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.save()
        return True
    
    def create_test_account(self):
        """创建测试账号"""
        if not self.user_exists('test'):
            self.users['test'] = {
                'name': 'test',
                'email': 'test@example.com',
                'password': Security.hash_password('123456'),
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            self.save()
            print("测试账号已创建: 用户名=test, 密码=123456")


user_service = UserService()
