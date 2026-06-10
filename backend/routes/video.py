#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI视频生成路由模块
"""

from flask import Blueprint, request, jsonify, session
from datetime import datetime
from services.video_service import video_service
from services.diary_service import diary_service
from services.jimeng_service import jimeng_video_service
from backend.decorators import login_required

video_bp = Blueprint('video', __name__, url_prefix='/api/video')


@video_bp.route('/videos', methods=['GET'])
def get_all_videos():
    """获取所有可用视频"""
    videos = video_service.get_all_videos()
    return jsonify(videos)


@video_bp.route('/analyze', methods=['POST'])
@login_required
def analyze_diary_for_video():
    """
    分析日记内容并生成视频推荐
    请求参数：
        diary_id: 日记ID（可选）
        content: 日记内容（可选）
        title: 日记标题（可选）
    """
    data = request.json
    diary_id = data.get('diary_id')
    content = data.get('content', '')
    title = data.get('title', '')

    if not content and diary_id:
        username = session['user_id']
        diaries = diary_service.get_user_diaries(username)
        for diary in diaries:
            if diary['id'] == diary_id:
                content = diary.get('content', '')
                title = diary.get('title', title)
                break

    if not content:
        return jsonify({'error': 'No diary content provided'}), 400

    analysis_result = video_service.analyze_diary_content(content)

    recommendations = []
    if diary_id:
        recommendations = video_service.generate_video_recommendations(
            diary_id, title, analysis_result
        )

    return jsonify({
        'analysis': analysis_result,
        'recommendations': recommendations,
        'diary_id': diary_id
    })


@video_bp.route('/generate', methods=['POST'])
@login_required
def generate_video():
    """
    为指定日记生成AI视频
    请求参数：
        diary_id: 日记ID
    """
    data = request.json
    diary_id = data.get('diary_id')

    if not diary_id:
        return jsonify({'error': 'Diary ID is required'}), 400

    username = session['user_id']
    diaries = diary_service.get_user_diaries(username)

    target_diary = None
    for diary in diaries:
        if diary['id'] == diary_id:
            target_diary = diary
            break

    if not target_diary:
        return jsonify({'error': 'Diary not found'}), 404

    content = target_diary.get('content', '')
    title = target_diary.get('title', '')

    analysis_result = video_service.analyze_diary_content(content)
    recommendations = video_service.generate_video_recommendations(
        diary_id, title, analysis_result
    )

    generated_videos = []
    for rec in recommendations:
        script = video_service.generate_video_script(content, rec)
        generated_videos.append({
            'video': rec,
            'script': script
        })
        video_service.save_generated_video(diary_id, rec)

    return jsonify({
        'success': True,
        'diary_id': diary_id,
        'diary_title': title,
        'analysis': analysis_result,
        'generated_videos': generated_videos
    })


@video_bp.route('/match', methods=['POST'])
@login_required
def match_video_for_diary():
    """
    手动匹配视频到日记
    请求参数：
        diary_id: 日记ID
        video_id: 视频ID
    """
    data = request.json
    diary_id = data.get('diary_id')
    video_id = data.get('video_id')

    if not diary_id or not video_id:
        return jsonify({'error': 'Diary ID and Video ID are required'}), 400

    username = session['user_id']
    diaries = diary_service.get_user_diaries(username)

    target_diary = None
    for diary in diaries:
        if diary['id'] == diary_id:
            target_diary = diary
            break

    if not target_diary:
        return jsonify({'error': 'Diary not found'}), 404

    videos = video_service.get_all_videos()
    target_video = None
    for video in videos:
        if video['id'] == video_id:
            target_video = video
            break

    if not target_video:
        return jsonify({'error': 'Video not found'}), 404

    content = target_diary.get('content', '')
    analysis_result = video_service.analyze_diary_content(content)

    recommendation = {
        'diary_id': diary_id,
        'diary_title': target_diary.get('title', ''),
        'video_id': target_video['id'],
        'video_name': target_video['name'],
        'video_name_cn': target_video['name_cn'],
        'video_path': target_video['path'],
        'category': target_video['category'],
        'match_score': video_service._calculate_match_score(
            analysis_result,
            {'keywords': [target_video['name_cn']], 'category': target_video['category']}
        ),
        'generated_at': None
    }

    script = video_service.generate_video_script(content, target_video)
    recommendation['script'] = script

    return jsonify({
        'success': True,
        'matched_video': recommendation
    })


@video_bp.route('/generate/ai', methods=['POST'])
@login_required
def generate_ai_video():
    """
    调用即梦API生成AI视频（异步模式）
    请求参数：
        diary_id: 日记ID
        aspect_ratio: 视频宽高比（可选，默认16:9）
    """
    data = request.json
    diary_id = data.get('diary_id')
    aspect_ratio = data.get('aspect_ratio', '16:9')

    if not diary_id:
        return jsonify({'error': 'Diary ID is required'}), 400

    username = session['user_id']
    diaries = diary_service.get_user_diaries(username)

    target_diary = None
    for diary in diaries:
        if diary['id'] == diary_id:
            target_diary = diary
            break

    if not target_diary:
        return jsonify({'error': 'Diary not found'}), 404

    content = target_diary.get('content', '')
    title = target_diary.get('title', '')

    prompt = jimeng_video_service.generate_video_script(title, content)
    submit_result = jimeng_video_service.submit_video_task(prompt, aspect_ratio)

    if not submit_result['success']:
        return jsonify(submit_result)

    task_id = submit_result['task_id']
    
    return jsonify({
        'success': True,
        'task_id': task_id,
        'diary_id': diary_id,
        'prompt': prompt,
        'message': '任务已提交，请轮询查询状态'
    })


@video_bp.route('/query/ai', methods=['POST'])
@login_required
def query_ai_video():
    """
    查询AI视频生成任务状态
    请求参数：
        task_id: 任务ID
        diary_id: 日记ID（可选，用于保存视频）
    """
    data = request.json
    task_id = data.get('task_id')
    diary_id = data.get('diary_id')

    if not task_id:
        return jsonify({'error': 'Task ID is required'}), 400

    result = jimeng_video_service.query_video_task(task_id)

    if not result['success']:
        return jsonify(result)

    status = result.get('status')
    status_lower = status.lower() if status else ""
    
    if status_lower in ['succeeded', 'success', 'completed', 'done']:
        video_url = result.get('video_url')
        local_video_url = None

        if diary_id and video_url:
            local_video_url = jimeng_video_service.download_video(video_url, diary_id)
            if not local_video_url:
                local_video_url = video_url

            username = session['user_id']
            diary_service.add_video_to_diary(
                username=username,
                diary_id=diary_id,
                video_info={
                    'video_url': local_video_url,
                    'task_id': task_id,
                    'prompt': '',
                    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            )

        return jsonify({
            'success': True,
            'task_id': task_id,
            'status': 'completed',
            'video_url': local_video_url or video_url
        })
    elif status_lower in ['failed', 'error']:
        return jsonify({
            'success': True,
            'task_id': task_id,
            'status': 'failed',
            'error': result.get('error_message', 'Unknown error')
        })
    else:
        return jsonify({
            'success': True,
            'task_id': task_id,
            'status': 'processing'
        })


@video_bp.route('/download/video', methods=['POST'])
@login_required
def download_video():
    """
    下载视频到本地
    请求参数：
        diary_id: 日记ID
        video_index: 视频索引（可选，默认0）
    """
    data = request.json
    diary_id = data.get('diary_id')
    video_index = data.get('video_index', 0)

    if not diary_id:
        return jsonify({'error': 'Diary ID is required'}), 400

    username = session['user_id']
    diaries = diary_service.get_user_diaries(username)

    target_diary = None
    for diary in diaries:
        if diary['id'] == diary_id:
            target_diary = diary
            break

    if not target_diary:
        return jsonify({'error': 'Diary not found'}), 404

    videos = target_diary.get('videos', [])
    if not videos or video_index >= len(videos):
        return jsonify({'error': 'Video not found'}), 404

    video = videos[video_index]
    remote_url = video.get('video_url')

    if not remote_url:
        return jsonify({'error': 'No video URL found'}), 400

    if remote_url.startswith('/static/'):
        return jsonify({
            'success': True,
            'already_local': True,
            'message': 'Video already local',
            'video_url': remote_url
        })

    print(f"[INFO] Downloading video for diary {diary_id}: {remote_url[:50]}...")

    local_url = jimeng_video_service.download_video(remote_url, diary_id)

    if local_url:
        videos[video_index]['video_url'] = local_url
        diary_service.save()

        return jsonify({
            'success': True,
            'message': 'Video downloaded successfully',
            'video_url': local_url
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to download video, URL may be expired'
        })


@video_bp.route('/download/all-videos', methods=['POST'])
@login_required
def download_all_videos():
    """
    下载用户所有日记的远程视频到本地
    """
    username = session['user_id']
    diaries = diary_service.get_user_diaries(username)

    results = []
    needs_download = False

    for diary in diaries:
        videos = diary.get('videos', [])
        for i, video in enumerate(videos):
            remote_url = video.get('video_url', '')

            if not remote_url or remote_url.startswith('/static/'):
                continue

            needs_download = True
            print(f"[INFO] Downloading video for diary {diary['id']}: {remote_url[:50]}...")

            local_url = jimeng_video_service.download_video(remote_url, diary['id'])

            if local_url:
                videos[i]['video_url'] = local_url
                results.append({
                    'diary_id': diary['id'],
                    'diary_title': diary.get('title', ''),
                    'success': True,
                    'local_url': local_url
                })
            else:
                results.append({
                    'diary_id': diary['id'],
                    'diary_title': diary.get('title', ''),
                    'success': False,
                    'error': 'URL may be expired'
                })

    if not needs_download:
        return jsonify({
            'success': True,
            'no_need': True,
            'message': '没有需要下载的远程视频'
        })

    if any(r['success'] for r in results):
        diary_service.save()

    success_count = sum(1 for r in results if r['success'])
    failed_count = len(results) - success_count

    return jsonify({
        'success': True,
        'no_need': False,
        'message': f'完成了 {success_count} 个视频下载，{failed_count} 个失败',
        'results': results
    })