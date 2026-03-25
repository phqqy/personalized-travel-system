#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记管理服务模块
"""

from utils.db_util import get_db_connection, execute_query
from algorithms.compress import compress_data, decompress_data, should_compress
import os


class DiaryService:
    """日记管理服务"""
    
    def __init__(self, data_dir):
        """
        初始化日记服务
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        self.db_path = f"{data_dir}/db/travel.db"
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        from utils.db_util import init_database
        init_database(self.db_path)
    
    def create_diary(self, user_id, title, content):
        """
        创建日记
        
        Args:
            user_id: 用户ID
            title: 标题
            content: 内容
        
        Returns:
            日记ID
        """
        # 压缩内容
        if should_compress(content):
            content = compress_data(content)
        
        query = '''
        INSERT INTO diaries (user_id, title, content) VALUES (?, ?, ?)
        '''
        params = (user_id, title, content)
        result = execute_query(self.db_path, query, params)
        
        # 获取生成的日记ID
        query = "SELECT last_insert_rowid()"
        result = execute_query(self.db_path, query)
        return result[0][0] if result else None
    
    def get_diary(self, diary_id):
        """
        获取日记
        
        Args:
            diary_id: 日记ID
        
        Returns:
            日记信息
        """
        query = "SELECT * FROM diaries WHERE id = ?"
        params = (diary_id,)
        result = execute_query(self.db_path, query, params)
        
        if not result:
            return None
        
        diary = dict(result[0])
        
        # 解压缩内容
        try:
            # 尝试解压缩，如果失败则认为未压缩
            diary['content'] = decompress_data(diary['content'])
        except:
            pass
        
        return diary
    
    def update_diary(self, diary_id, title=None, content=None):
        """
        更新日记
        
        Args:
            diary_id: 日记ID
            title: 标题（可选）
            content: 内容（可选）
        
        Returns:
            是否成功
        """
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        
        if content is not None:
            # 压缩内容
            if should_compress(content):
                content = compress_data(content)
            updates.append("content = ?")
            params.append(content)
        
        if not updates:
            return True
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(diary_id)
        
        query = f"UPDATE diaries SET {', '.join(updates)} WHERE id = ?"
        execute_query(self.db_path, query, params)
        return True
    
    def delete_diary(self, diary_id):
        """
        删除日记
        
        Args:
            diary_id: 日记ID
        
        Returns:
            是否成功
        """
        query = "DELETE FROM diaries WHERE id = ?"
        params = (diary_id,)
        execute_query(self.db_path, query, params)
        return True
    
    def get_user_diaries(self, user_id, page=1, page_size=20):
        """
        获取用户日记列表
        
        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页大小
        
        Returns:
            日记列表
        """
        offset = (page - 1) * page_size
        query = '''
        SELECT * FROM diaries WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?
        '''
        params = (user_id, page_size, offset)
        result = execute_query(self.db_path, query, params)
        
        diaries = []
        for row in result:
            diary = dict(row)
            # 解压缩内容
            try:
                diary['content'] = decompress_data(diary['content'])
            except:
                pass
            diaries.append(diary)
        
        return diaries
    
    def increase_heat(self, diary_id):
        """
        增加日记热度
        
        Args:
            diary_id: 日记ID
        """
        query = "UPDATE diaries SET 热度 = 热度 + 1 WHERE id = ?"
        params = (diary_id,)
        execute_query(self.db_path, query, params)
