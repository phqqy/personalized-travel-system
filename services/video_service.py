#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI视频生成服务模块
根据用户日记内容生成AI视频推荐
"""

import os
import random
from datetime import datetime


class VideoService:
    """AI视频生成服务类"""

    def __init__(self):
        self.video_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'aigc-foodvideo'
        )
        self.available_videos = [
            {
                'id': 1,
                'name': 'Beijing Luzhu Huoshao Vlog.mp4',
                'name_cn': '北京卤煮火烧',
                'keywords': ['卤煮火烧', '火烧', '小吃', '北京', '传统美食'],
                'category': 'food'
            },
            {
                'id': 2,
                'name': 'Beijing Shabu Shabu Food Tour Vlog.mp4',
                'name_cn': '北京涮羊肉探店',
                'keywords': ['涮羊肉', '火锅', '探店', '羊肉', '北京'],
                'category': 'food'
            },
            {
                'id': 3,
                'name': 'Beijing Chaogan Vlog.mp4',
                'name_cn': '北京炒肝',
                'keywords': ['炒肝', '猪肝', '北京', '传统小吃', '早餐'],
                'category': 'food'
            },
            {
                'id': 4,
                'name': 'Beijing Zhajiang Noodles Vlog.mp4',
                'name_cn': '北京炸酱面',
                'keywords': ['炸酱面', '面条', '北京', '传统美食', '面食'],
                'category': 'food'
            },
            {
                'id': 5,
                'name': 'Beijing Roast Duck Vlog.mp4',
                'name_cn': '北京烤鸭',
                'keywords': ['烤鸭', '北京烤鸭', '北京', '美食', '招牌菜'],
                'category': 'food'
            },
            {
                'id': 6,
                'name': 'Beijing Douzhi Food Tour Vlog.mp4',
                'name_cn': '北京豆汁探店',
                'keywords': ['豆汁', '北京', '传统小吃', '探店', '特色'],
                'category': 'food'
            }
        ]

    def analyze_diary_content(self, content):
        """
        分析日记内容，提取关键词和情感

        Args:
            content: 日记内容

        Returns:
            分析结果字典
        """
        content_lower = content.lower()
        found_keywords = []
        mentioned_categories = set()

        for video in self.available_videos:
            for keyword in video['keywords']:
                if keyword.lower() in content_lower:
                    found_keywords.append(keyword)
                    mentioned_categories.add(video['category'])
                    break

        food_related = any(word in content_lower for word in [
            '吃', '美食', '餐厅', '饭店', '菜', '饭', '小吃', '品尝',
            'eat', 'food', 'restaurant', 'dish', 'taste', 'delicious'
        ])

        travel_related = any(word in content_lower for word in [
            '旅游', '旅行', '游玩', '参观', '游览', '景点', '地方',
            'travel', 'trip', 'visit', 'tour', 'sightseeing'
        ])

        mood = 'positive'
        if any(word in content_lower for word in ['开心', '高兴', '愉快', '快乐', '美味', '好吃', '不错', 'happy', 'good', 'nice', 'delicious']):
            mood = 'positive'
        elif any(word in content_lower for word in ['失望', '糟糕', '差', '失望', 'bad', 'terrible', 'disappointed']):
            mood = 'negative'
        else:
            mood = 'neutral'

        return {
            'found_keywords': list(set(found_keywords)),
            'categories': list(mentioned_categories),
            'food_related': food_related,
            'travel_related': travel_related,
            'mood': mood,
            'content_length': len(content)
        }

    def generate_video_recommendations(self, diary_id, diary_title, analysis_result):
        """
        根据日记分析结果生成视频推荐

        Args:
            diary_id: 日记ID
            diary_title: 日记标题
            analysis_result: 分析结果

        Returns:
            视频推荐列表
        """
        recommendations = []
        matched_videos = []

        if analysis_result['found_keywords']:
            for video in self.available_videos:
                for keyword in video['keywords']:
                    if keyword.lower() in ' '.join(analysis_result['found_keywords']).lower():
                        matched_videos.append(video)
                        break

        if not matched_videos:
            matched_videos = random.sample(
                self.available_videos,
                min(2, len(self.available_videos))
            )

        for video in matched_videos[:3]:
            video_info = {
                'diary_id': diary_id,
                'diary_title': diary_title,
                'video_id': video['id'],
                'video_name': video['name'],
                'video_name_cn': video['name_cn'],
                'video_path': f'/aigc-foodvideo/{video["name"]}',
                'category': video['category'],
                'match_score': self._calculate_match_score(analysis_result, video),
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            recommendations.append(video_info)

        return recommendations

    def _calculate_match_score(self, analysis_result, video):
        """
        计算视频与日记的匹配度分数

        Args:
            analysis_result: 分析结果
            video: 视频信息

        Returns:
            匹配度分数 (0-100)
        """
        score = 50

        if video['category'] in analysis_result['categories']:
            score += 20

        if analysis_result['mood'] == 'positive':
            score += 15

        if analysis_result['food_related']:
            score += 10

        if analysis_result['travel_related']:
            score += 5

        return min(score, 100)

    def get_all_videos(self):
        """
        获取所有可用视频

        Returns:
            视频列表
        """
        return [
            {
                'id': v['id'],
                'name': v['name'],
                'name_cn': v['name_cn'],
                'category': v['category'],
                'path': f'/aigc-foodvideo/{v["name"]}'
            }
            for v in self.available_videos
        ]

    def generate_video_script(self, diary_content, video_info):
        """
        为视频生成AI解说脚本（模拟）

        Args:
            diary_content: 日记内容
            video_info: 视频信息

        Returns:
            生成的脚本
        """
        scripts = [
            f"这是一段关于{video_info['video_name_cn']}的精彩视频，让我们一起跟随镜头感受北京的美食魅力。",
            f"跟随我们的镜头，一起探索{video_info['video_name_cn']}的独特风味，体验地道的北京美食文化。",
            f"今天我们将为大家呈现{video_info['video_name_cn']}的完整制作过程，感受传统美食的匠心独运。"
        ]

        return random.choice(scripts)

    def save_generated_video(self, diary_id, video_recommendation):
        """
        保存生成的视频记录

        Args:
            diary_id: 日记ID
            video_recommendation: 视频推荐信息

        Returns:
            是否保存成功
        """
        return True


video_service = VideoService()