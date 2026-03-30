#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记服务模块
"""

from datetime import datetime
from config.settings import config
from utils.storage import DataStorage


class DiaryService:
    """日记服务类"""
    
    def __init__(self):
        self.user_diaries = DataStorage.load_data(config.DIARY_DATA_FILE, {})
    
    def save(self):
        """保存日记数据"""
        DataStorage.save_data(config.DIARY_DATA_FILE, self.user_diaries)
    
    def get_user_diaries(self, username):
        """
        获取用户的所有日记
        
        Args:
            username: 用户名
        
        Returns:
            日记列表
        """
        return self.user_diaries.get(username, [])
    
    def create_diary(self, username, title, content, date=None):
        """
        创建新日记
        
        Args:
            username: 用户名
            title: 标题
            content: 内容
            date: 日期（可选）
        
        Returns:
            新日记的ID
        """
        if username not in self.user_diaries:
            self.user_diaries[username] = []
        
        diary_id = len(self.user_diaries[username]) + 1
        new_diary = {
            'id': diary_id,
            'title': title,
            'content': content,
            'date': date if date else datetime.now().strftime('%Y-%m-%d'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.user_diaries[username].append(new_diary)
        self.save()
        return diary_id
    
    def update_diary(self, username, diary_id, title=None, content=None):
        """
        更新日记
        
        Args:
            username: 用户名
            diary_id: 日记ID
            title: 新标题（可选）
            content: 新内容（可选）
        
        Returns:
            是否更新成功
        """
        diaries = self.user_diaries.get(username, [])
        for diary in diaries:
            if diary['id'] == diary_id:
                if title is not None:
                    diary['title'] = title
                if content is not None:
                    diary['content'] = content
                diary['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save()
                return True
        return False
    
    def delete_diary(self, username, diary_id):
        """
        删除日记
        
        Args:
            username: 用户名
            diary_id: 日记ID
        
        Returns:
            是否删除成功
        """
        if username not in self.user_diaries:
            return False
        
        original_length = len(self.user_diaries[username])
        self.user_diaries[username] = [d for d in self.user_diaries[username] if d['id'] != diary_id]
        
        if len(self.user_diaries[username]) != original_length:
            self.save()
            return True
        return False
    
    def export_diaries(self, username):
        """
        导出用户日记
        
        Args:
            username: 用户名
        
        Returns:
            导出的数据字典
        """
        return {
            'user': username,
            'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'diaries': self.get_user_diaries(username)
        }
    
    def import_diaries(self, username, imported_diaries):
        """
        导入日记
        
        Args:
            username: 用户名
            imported_diaries: 要导入的日记列表
        
        Returns:
            导入的日记数量
        """
        if username not in self.user_diaries:
            self.user_diaries[username] = []
        
        next_id = len(self.user_diaries[username]) + 1
        count = 0
        
        for diary in imported_diaries:
            diary['id'] = next_id
            diary['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.user_diaries[username].append(diary)
            next_id += 1
            count += 1
        
        self.save()
        return count
    
    def init_user_diaries(self, username):
        """
        初始化用户日记列表
        
        Args:
            username: 用户名
        """
        if username not in self.user_diaries:
            self.user_diaries[username] = []
            self.save()


diary_service = DiaryService()
