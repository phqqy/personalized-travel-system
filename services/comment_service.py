#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记交流服务模块
"""

from utils.db_util import execute_query
from utils.rag_retrieval import RAGRetrieval


class CommentService:
    """日记交流服务"""
    
    def __init__(self, data_dir):
        """
        初始化评论服务
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        self.db_path = f"{data_dir}/db/travel.db"
        self.rag = RAGRetrieval()
        self.init_rag()
    
    def init_rag(self):
        """初始化RAG检索"""
        # 加载所有日记内容到RAG
        query = "SELECT id, content FROM diaries"
        result = execute_query(self.db_path, query)
        
        for row in result:
            diary_id = row['id']
            content = row['content']
            self.rag.add_document(content, diary_id)
    
    def add_comment(self, diary_id, user_id, content):
        """
        添加评论
        
        Args:
            diary_id: 日记ID
            user_id: 用户ID
            content: 评论内容
        
        Returns:
            评论ID
        """
        query = '''
        INSERT INTO comments (diary_id, user_id, content) VALUES (?, ?, ?)
        '''
        params = (diary_id, user_id, content)
        execute_query(self.db_path, query, params)
        
        # 获取生成的评论ID
        query = "SELECT last_insert_rowid()"
        result = execute_query(self.db_path, query)
        return result[0][0] if result else None
    
    def get_comments(self, diary_id):
        """
        获取日记评论
        
        Args:
            diary_id: 日记ID
        
        Returns:
            评论列表
        """
        query = '''
        SELECT * FROM comments WHERE diary_id = ? ORDER BY created_at DESC
        '''
        params = (diary_id,)
        result = execute_query(self.db_path, query, params)
        
        return [dict(row) for row in result]
    
    def add_rating(self, diary_id, user_id, rating):
        """
        添加评分
        
        Args:
            diary_id: 日记ID
            user_id: 用户ID
            rating: 评分（1-5）
        
        Returns:
            是否成功
        """
        # 检查是否已经评分
        query = "SELECT * FROM ratings WHERE diary_id = ? AND user_id = ?"
        params = (diary_id, user_id)
        result = execute_query(self.db_path, query, params)
        
        if result:
            # 更新评分
            query = "UPDATE ratings SET rating = ? WHERE diary_id = ? AND user_id = ?"
            params = (rating, diary_id, user_id)
        else:
            # 插入新评分
            query = "INSERT INTO ratings (diary_id, user_id, rating) VALUES (?, ?, ?)"
            params = (diary_id, user_id, rating)
        
        execute_query(self.db_path, query, params)
        return True
    
    def get_rating(self, diary_id):
        """
        获取日记评分
        
        Args:
            diary_id: 日记ID
        
        Returns:
            平均评分
        """
        query = "SELECT AVG(rating) FROM ratings WHERE diary_id = ?"
        params = (diary_id,)
        result = execute_query(self.db_path, query, params)
        
        return result[0][0] if result and result[0][0] else 0
    
    def search_diaries(self, query, top_k=5):
        """
        搜索日记
        
        Args:
            query: 查询字符串
            top_k: 返回前k个结果
        
        Returns:
            日记列表
        """
        # 使用RAG检索
        results = self.rag.retrieve(query, top_k)
        
        # 获取完整的日记信息
        diaries = []
        for result in results:
            diary_id = result['id']
            diary_query = "SELECT * FROM diaries WHERE id = ?"
            diary_result = execute_query(self.db_path, diary_query, (diary_id,))
            if diary_result:
                diaries.append(dict(diary_result[0]))
        
        return diaries
