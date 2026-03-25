#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAG检索工具模块
"""

from algorithms.text_search import TextSearch


class RAGRetrieval:
    """RAG检索类"""
    
    def __init__(self):
        """初始化检索器"""
        self.search_engine = TextSearch()
    
    def add_document(self, content, doc_id=None):
        """
        添加文档到检索库
        
        Args:
            content: 文档内容
            doc_id: 文档ID（可选）
        
        Returns:
            文档ID
        """
        return self.search_engine.add_document(content, doc_id)
    
    def retrieve(self, query, top_k=5):
        """
        检索相关文档
        
        Args:
            query: 查询字符串
            top_k: 返回前k个文档
        
        Returns:
            相关文档列表
        """
        doc_ids = self.search_engine.search(query)
        
        # 获取文档内容
        documents = []
        for doc_id in doc_ids[:top_k]:
            content = self.search_engine.get_document(doc_id)
            if content:
                documents.append({
                    'id': doc_id,
                    'content': content
                })
        
        return documents
    
    def generate_response(self, query, context):
        """
        基于检索到的上下文生成响应
        
        Args:
            query: 查询字符串
            context: 检索到的上下文
        
        Returns:
            生成的响应
        """
        # 简单的响应生成，实际应用中可以使用LLM
        response = f"针对您的问题：{query}\n\n"
        response += "根据相关信息：\n"
        
        for i, doc in enumerate(context):
            response += f"{i+1}. {doc['content'][:100]}...\n"
        
        response += "\n基于以上信息，我为您提供以下建议："
        return response
