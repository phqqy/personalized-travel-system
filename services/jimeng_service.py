#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI视频生成服务模块
调用字节跳动即梦API生成实际视频
使用火山引擎官方SDK确保签名正确
"""

import os
import time
import json
import requests
from datetime import datetime

from config.settings import config
from volcengine.visual.VisualService import VisualService

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_DOWNLOAD_DIR = os.path.join(BASE_DIR, 'web_app', 'static', 'videos', 'ai')
os.makedirs(VIDEO_DOWNLOAD_DIR, exist_ok=True)


class JimengVideoService:
    """
    即梦AI视频生成服务
    调用火山引擎即梦API生成视频
    """

    def __init__(self):
        self.access_key = config.VOLCENGINE_ACCESS_KEY
        self.secret_key = config.VOLCENGINE_SECRET_KEY

        # Masked key for debug display
        if self.access_key:
            masked_ak = self.access_key[:8] + '***' + self.access_key[-4:] if len(self.access_key) > 12 else '***'
        else:
            masked_ak = '(空)'
        masked_sk = '(已设置)' if self.secret_key else '(空)'

        print(f"[INIT] JimengVideoService initialized")
        print(f"[INIT]   Access Key: {masked_ak}")
        print(f"[INIT]   Secret Key: {masked_sk}")

        if not self.access_key or not self.secret_key:
            print("[WARN] *** 火山引擎API密钥未配置！请在 .env 文件中设置 VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY")
            print("[WARN]  获取地址: https://console.volcengine.com/iam/keymanage")
            print("[WARN]  开通即梦服务: https://console.volcengine.com/visual/experience")

        self.service = VisualService()
        self.service.set_ak(self.access_key)
        self.service.set_sk(self.secret_key)

    def download_video(self, video_url, diary_id):
        """
        下载视频到本地目录

        Args:
            video_url: 远程视频URL
            diary_id: 日记ID

        Returns:
            本地视频路径或None
        """
        try:
            filename = f"diary_{diary_id}_{int(time.time())}.mp4"
            local_path = os.path.join(VIDEO_DOWNLOAD_DIR, filename)

            print(f"[INFO] Downloading video from: {video_url[:50]}...")
            print(f"[INFO] Saving to: {local_path}")

            response = requests.get(video_url, timeout=60, stream=True)
            response.raise_for_status()

            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            file_size = os.path.getsize(local_path)
            print(f"[INFO] Video downloaded successfully: {file_size} bytes")

            return f'/static/videos/ai/{filename}'
        except Exception as e:
            print(f"[ERROR] Failed to download video: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def submit_video_task(self, prompt, aspect_ratio="16:9", duration=5):
        """
        提交视频生成任务

        Args:
            prompt: 视频生成提示词
            aspect_ratio: 宽高比，可选 "16:9" 或 "9:16"
            duration: 视频时长（秒），可选5或10

        Returns:
            任务响应字典
        """
        try:
            frames = 121 if duration == 5 else 241
            
            body = {
                "req_key": "jimeng_t2v_v30",
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "frames": frames,
                "seed": -1
            }

            print(f"[DEBUG] Submitting task with prompt: {prompt[:50]}...")
            
            response = self.service.cv_sync2async_submit_task(body)
            
            if isinstance(response, bytes):
                response = response.decode('utf-8')
            
            if isinstance(response, str):
                response_dict = json.loads(response)
            else:
                response_dict = response
            
            if response_dict.get("ResponseMetadata", {}).get("Error"):
                error = response_dict["ResponseMetadata"]["Error"]
                return {
                    'success': False,
                    'error': f"{error.get('Code', 'Unknown')}: {error.get('Message', 'Unknown error')}"
                }
            
            print(f"[DEBUG] Response: {response_dict}")
            
            code = response_dict.get("code")
            
            if code == 10000:
                task_id = response_dict.get("data", {}).get("task_id")
                if task_id:
                    return {
                        'success': True,
                        'task_id': task_id
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No task ID returned'
                    }
            elif code == 50400:
                return {
                    'success': False,
                    'error': 'Access Denied: 访问被拒绝，请检查火山引擎API密钥是否正确配置，以及是否已开通即梦AI（jimeng）服务',
                    'code': 50400,
                    'help': '开通地址: https://console.volcengine.com/visual/experience | 密钥管理: https://console.volcengine.com/iam/keymanage'
                }
            elif code == 50430:
                return {
                    'success': False,
                    'error': 'API并发限制，请稍后重试（免费版通常限制1个并发任务）',
                    'code': 50430
                }
            else:
                return {
                    'success': False,
                    'error': response_dict.get("message", "Unknown error"),
                    'code': code
                }

        except Exception as e:
            print(f"[ERROR] submit_video_task Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

    def query_video_task(self, task_id):
        """
        查询视频生成任务状态

        Args:
            task_id: 任务ID

        Returns:
            任务状态字典
        """
        try:
            body = {
                "req_key": "jimeng_t2v_v30",
                "task_id": task_id
            }

            response = self.service.cv_sync2async_get_result(body)
            
            if isinstance(response, bytes):
                response = response.decode('utf-8')
            
            if isinstance(response, str):
                response_dict = json.loads(response)
            else:
                response_dict = response
            
            print(f"[DEBUG] Query Response: {response_dict}")
            
            if response_dict.get("code") != 10000:
                return {
                    'success': False,
                    'error': response_dict.get("message", "Unknown error")
                }
            
            result = response_dict.get("data", {})
            return {
                'success': True,
                'task_id': task_id,
                'status': result.get("status"),
                'video_url': result.get("video_url"),
                'error_message': result.get("error_message")
            }

        except Exception as e:
            print(f"[ERROR] query_video_task Exception: {str(e)}")
            return {'success': False, 'error': str(e)}

    def wait_for_video(self, task_id, max_wait=300):
        """
        等待视频生成完成

        Args:
            task_id: 任务ID
            max_wait: 最大等待时间（秒）

        Returns:
            视频信息字典
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            result = self.query_video_task(task_id)
            
            if not result['success']:
                return result
            
            status = result.get('status')
            
            status_lower = status.lower() if status else ""
            
            if status_lower in ['succeeded', 'success', 'completed', 'done']:
                return {
                    'success': True,
                    'task_id': task_id,
                    'video_url': result.get('video_url'),
                    'status': 'completed'
                }
            
            if status_lower in ['failed', 'error']:
                return {
                    'success': False,
                    'task_id': task_id,
                    'error': result.get('error_message', 'Unknown error'),
                    'status': 'failed'
                }
            
            if status_lower in ['processing', 'running', 'generating', 'pending', 'queued', 'waiting']:
                time.sleep(5)
                continue
            
            print(f"[WARN] Unknown status: {status}, treating as still processing")
            time.sleep(5)
        
        return {
            'success': False,
            'task_id': task_id,
            'error': 'Timeout waiting for video generation',
            'status': 'timeout'
        }

    def generate_video_from_diary(self, diary_id, diary_title, diary_content, aspect_ratio="16:9"):
        """
        根据日记内容生成视频

        Args:
            diary_id: 日记ID
            diary_title: 日记标题
            diary_content: 日记内容
            aspect_ratio: 宽高比

        Returns:
            视频生成结果字典
        """
        prompt = self.generate_video_script(diary_title, diary_content)
        
        print(f"[INFO] Generating video for diary: {diary_title}")
        print(f"[INFO] Prompt: {prompt}")
        
        submit_result = self.submit_video_task(prompt, aspect_ratio)
        
        if not submit_result['success']:
            return submit_result
        
        task_id = submit_result['task_id']
        print(f"[INFO] Task submitted successfully, task_id: {task_id}")
        
        wait_result = self.wait_for_video(task_id)
        
        if wait_result['success']:
            return {
                'success': True,
                'task_id': task_id,
                'video_url': wait_result['video_url'],
                'prompt': prompt,
                'diary_id': diary_id,
                'diary_title': diary_title,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            return wait_result

    def generate_video_script(self, title, content):
        """
        根据日记内容生成视频提示词

        Args:
            title: 日记标题
            content: 日记内容

        Returns:
            视频提示词
        """
        keywords = self._extract_keywords(content)
        keywords_str = ', '.join(keywords) if keywords else title

        prompt = f"A beautiful travel scene: {keywords_str}, high quality, cinematic, vibrant colors, stunning landscape, smooth motion"

        return prompt

    def _extract_keywords(self, text):
        """
        从文本中提取关键词

        Args:
            text: 输入文本

        Returns:
            关键词列表
        """
        food_keywords = ['烤鸭', '炸酱面', '涮羊肉', '卤煮', '炒肝', '豆汁', '美食', '小吃', '餐厅', '餐馆']
        sight_keywords = ['长城', '故宫', '天安门', '颐和园', '天坛', '圆明园', '景点', '风景', '游览', '参观']
        travel_keywords = ['旅行', '旅游', '行程', '路线', '打卡', '拍照', '体验']
        
        keywords = []
        
        for kw in food_keywords:
            if kw in text:
                keywords.append(kw)
        
        for kw in sight_keywords:
            if kw in text:
                keywords.append(kw)
        
        for kw in travel_keywords:
            if kw in text:
                keywords.append(kw)
        
        return keywords[:5]


jimeng_video_service = JimengVideoService()
