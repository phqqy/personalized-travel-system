#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
全文检索模块
"""

import re
from collections import defaultdict


class TextSearch:
    """全文检索类"""
    
    def __init__(self):
        """初始化索引"""
        self.index = defaultdict(list)  # 词到文档ID的映射
        self.documents = {}  # 文档ID到文档内容的映射
        self.next_doc_id = 1
    
    def add_document(self, content, doc_id=None):
        """
        添加文档到索引
        
        Args:
            content: 文档内容
            doc_id: 文档ID（可选）
        
        Returns:
            文档ID
        """
        if doc_id is None:
            doc_id = self.next_doc_id
            self.next_doc_id += 1
        
        self.documents[doc_id] = content
        
        # 分词并构建索引
        words = self._tokenize(content)
        for word in words:
            if doc_id not in self.index[word]:
                self.index[word].append(doc_id)
        
        return doc_id
    
    def search(self, query):
        """
        搜索文档
        
        Args:
            query: 查询字符串
        
        Returns:
            匹配的文档ID列表
        """
        query_words = self._tokenize(query)
        if not query_words:
            return []
        
        # 获取包含所有查询词的文档
        result = set(self.index.get(query_words[0], []))
        for word in query_words[1:]:
            result.intersection_update(self.index.get(word, []))
        
        return list(result)
    
    def _tokenize(self, text):
        """
        分词
        
        Args:
            text: 文本
        
        Returns:
            词列表
        """
        # 简单的分词方法，使用正则表达式
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def get_document(self, doc_id):
        """
        获取文档内容
        
        Args:
            doc_id: 文档ID
        
        Returns:
            文档内容
        """
        return self.documents.get(doc_id)
