#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记服务模块
支持：全局共享、点赞、评论
"""

import uuid
from datetime import datetime
from config.settings import config
from utils.storage import DataStorage


class DiaryService:
    """日记服务类"""

    def __init__(self):
        raw_data = DataStorage.load_data(config.DIARY_DATA_FILE, None)
        if raw_data is None:
            self.user_diaries = {}       # {username: [diary, ...]}
            self._next_ids = {}          # {username: next_local_id}
            self.likes = {}              # {global_id: [username, ...]}
            self.comments = {}           # {global_id: [{id, username, content, created_at}, ...]}
        elif isinstance(raw_data, dict) and '_next_ids' in raw_data:
            self.user_diaries = raw_data.get('user_diaries', {})
            self._next_ids = raw_data.get('_next_ids', {})
            self.likes = raw_data.get('likes', {})
            self.comments = raw_data.get('comments', {})
        else:
            # 兼容旧数据格式
            self.user_diaries = raw_data
            self._next_ids = {}
            self.likes = {}
            self.comments = {}

        # 确保已有日记都有 global_id（迁移旧数据）
        self._migrate_global_ids()

    def _migrate_global_ids(self):
        """为旧日记补充 global_id"""
        migrated = False
        for username, diaries in self.user_diaries.items():
            for diary in diaries:
                if 'global_id' not in diary:
                    diary['global_id'] = str(uuid.uuid4())[:12]
                    migrated = True
        if migrated:
            self.save()

    def save(self):
        """保存日记数据"""
        DataStorage.save_data(config.DIARY_DATA_FILE, {
            'user_diaries': self.user_diaries,
            '_next_ids': self._next_ids,
            'likes': self.likes,
            'comments': self.comments
        })

    def _get_next_id(self, username):
        """获取下一个自增ID，确保唯一性"""
        current_id = self._next_ids.get(username, 0) + 1
        self._next_ids[username] = current_id
        return current_id

    # ==================== 日记 CRUD ====================

    def get_user_diaries(self, username):
        """获取用户的所有日记"""
        return self.user_diaries.get(username, [])

    def get_all_diaries(self):
        """
        获取所有用户的所有日记（全局共享）
        按创建时间倒序排列
        """
        all_diaries = []
        for username, diaries in self.user_diaries.items():
            for diary in diaries:
                # 附加点赞数和评论数
                gid = diary.get('global_id', '')
                diary_copy = dict(diary)
                diary_copy['like_count'] = len(self.likes.get(gid, []))
                diary_copy['comment_count'] = len(self.comments.get(gid, []))
                all_diaries.append(diary_copy)

        all_diaries.sort(key=lambda d: d.get('created_at', ''), reverse=True)
        return all_diaries

    def get_diary_by_global_id(self, global_id):
        """通过 global_id 查找日记"""
        for username, diaries in self.user_diaries.items():
            for diary in diaries:
                if diary.get('global_id') == global_id:
                    return diary, username
        return None, None

    def create_diary(self, username, title, content, date=None):
        """
        创建新日记
        """
        if username not in self.user_diaries:
            self.user_diaries[username] = []

        diary_id = self._get_next_id(username)
        global_id = str(uuid.uuid4())[:12]
        new_diary = {
            'id': diary_id,
            'global_id': global_id,
            'username': username,
            'title': title,
            'content': content,
            'date': date if date else datetime.now().strftime('%Y-%m-%d'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.user_diaries[username].append(new_diary)
        self.likes[global_id] = []
        self.comments[global_id] = []
        self.save()
        return diary_id, global_id

    def update_diary(self, username, diary_id, title=None, content=None):
        """更新日记"""
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
        """删除日记（同时清理点赞和评论）"""
        if username not in self.user_diaries:
            return False

        # 找到要删除的日记获取 global_id
        target_global_id = None
        for d in self.user_diaries[username]:
            if d['id'] == diary_id:
                target_global_id = d.get('global_id')
                break

        original_length = len(self.user_diaries[username])
        self.user_diaries[username] = [d for d in self.user_diaries[username] if d['id'] != diary_id]

        if len(self.user_diaries[username]) != original_length:
            # 清理点赞和评论
            if target_global_id and target_global_id in self.likes:
                del self.likes[target_global_id]
            if target_global_id and target_global_id in self.comments:
                del self.comments[target_global_id]
            self.save()
            return True
        return False

    # ==================== 点赞功能 ====================

    def toggle_like(self, username, global_id):
        """
        切换点赞状态（点赞/取消点赞）
        返回: (liked: bool, like_count: int)
        """
        diary, owner = self.get_diary_by_global_id(global_id)
        if not diary:
            return None, 0

        if global_id not in self.likes:
            self.likes[global_id] = []

        likers = self.likes[global_id]

        if username in likers:
            likers.remove(username)
            liked = False
        else:
            likers.append(username)
            liked = True

        self.save()
        return liked, len(likers)

    def get_like_status(self, username, global_id):
        """获取当前用户对某日记的点赞状态"""
        likers = self.likes.get(global_id, [])
        return {
            'liked': username in likers,
            'like_count': len(likers)
        }

    def get_likes_batch(self, username, global_ids):
        """批量获取点赞状态"""
        result = {}
        for gid in global_ids:
            result[gid] = self.get_like_status(username, gid)
        return result

    # ==================== 评论功能 ====================

    def add_comment(self, username, global_id, content):
        """
        添加评论
        返回评论对象或 None
        """
        diary, owner = self.get_diary_by_global_id(global_id)
        if not diary:
            return None

        if global_id not in self.comments:
            self.comments[global_id] = []

        comment = {
            'id': len(self.comments[global_id]) + 1,
            'username': username,
            'content': content.strip(),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        self.comments[global_id].append(comment)
        self.save()
        return comment

    def get_comments(self, global_id):
        """获取某日记的所有评论（按时间正序）"""
        return self.comments.get(global_id, [])

    def delete_comment(self, username, global_id, comment_id):
        """删除评论（仅作者可删）"""
        if global_id not in self.comments:
            return False

        comments = self.comments[global_id]
        for i, c in enumerate(comments):
            if c['id'] == comment_id and c['username'] == username:
                comments.pop(i)
                self.save()
                return True
        return False

    # ==================== 导出/导入 ====================

    def export_diaries(self, username):
        """导出用户日记"""
        return {
            'user': username,
            'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'diaries': self.get_user_diaries(username)
        }

    def import_diaries(self, username, imported_diaries):
        """导入日记"""
        if username not in self.user_diaries:
            self.user_diaries[username] = []

        count = 0
        for diary in imported_diaries:
            diary['id'] = self._get_next_id(username)
            diary['global_id'] = str(uuid.uuid4())[:12]
            diary['username'] = username
            diary['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.user_diaries[username].append(diary)
            self.likes[diary['global_id']] = []
            self.comments[diary['global_id']] = []
            count += 1

        self.save()
        return count

    def init_user_diaries(self, username):
        """初始化用户日记列表"""
        if username not in self.user_diaries:
            self.user_diaries[username] = []
            self.save()

    # ==================== 视频关联 ====================

    def add_video_to_diary(self, username, diary_id, video_info):
        """将生成的视频关联到日记"""
        diaries = self.user_diaries.get(username, [])
        for diary in diaries:
            if diary['id'] == diary_id:
                if 'videos' not in diary:
                    diary['videos'] = []

                video_entry = {
                    'video_url': video_info.get('video_url'),
                    'task_id': video_info.get('task_id'),
                    'prompt': video_info.get('prompt'),
                    'generated_at': video_info.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                }

                diary['videos'].append(video_entry)
                diary['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save()
                return True
        return False


diary_service = DiaryService()
