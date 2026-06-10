#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复图片分配：景点用景点图，学校用学校/景点图，美食用美食图
"""
import os
import csv
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPOTS_IMAGES_DIR = os.path.join(BASE_DIR, 'web_app', 'static', 'images', 'spots')
FOOD_IMAGES_DIR = os.path.join(BASE_DIR, 'web_app', 'static', 'images', 'food')

random.seed(2026)


def get_images(dir_path, prefix):
    """获取目录下所有真实图片"""
    if not os.path.exists(dir_path):
        return []
    images = []
    for f in os.listdir(dir_path):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')) and not f.startswith('default'):
            images.append(f'{prefix}/{f}')
    return sorted(images)


SPOT_IMAGES = get_images(SPOTS_IMAGES_DIR, '/static/images/spots')
FOOD_IMAGES = get_images(FOOD_IMAGES_DIR, '/static/images/food')

print(f"景点图片池 ({len(SPOT_IMAGES)} 张):")
for img in SPOT_IMAGES:
    print(f"  {img}")
print(f"\n美食图片池 ({len(FOOD_IMAGES)} 张):")
for img in FOOD_IMAGES:
    print(f"  {img}")


def fix_csv(filename, img_col, allowed_prefixes, fallback_img):
    """
    修复 CSV 文件中的图片分配
    - filename: CSV 文件名
    - img_col: 图片字段的列索引
    - allowed_prefixes: 允许的图片路径前缀列表
    - fallback_img: 当图片不属于允许范围时的替换函数
    """
    filepath = os.path.join(BASE_DIR, 'data', 'raw', filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [r for r in reader if r and r[0].strip()]

    fixed = 0
    for row in rows:
        if len(row) > img_col:
            img = row[img_col].strip()
            is_allowed = any(img.startswith(p) for p in allowed_prefixes)
            if not is_allowed:
                row[img_col] = fallback_img()
                fixed += 1

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    return len(rows), fixed


# Fix spots.csv: only allow /static/images/spots/ images
print("\n" + "=" * 60)
print("修复 spots.csv — 景点只使用景点图片")
spots_count, spots_fixed = fix_csv(
    'spots.csv',
    img_col=5,
    allowed_prefixes=['/static/images/spots/'],
    fallback_img=lambda: random.choice(SPOT_IMAGES)
)
print(f"  总计: {spots_count} 条, 修复: {spots_fixed} 条")


# Fix universities.csv: only allow /static/images/spots/ images (school images are in spots/)
print("\n" + "=" * 60)
print("修复 universities.csv — 学校只使用学校/景点图片")
uni_count, uni_fixed = fix_csv(
    'universities.csv',
    img_col=6,
    allowed_prefixes=['/static/images/spots/'],
    fallback_img=lambda: random.choice(SPOT_IMAGES)
)
print(f"  总计: {uni_count} 条, 修复: {uni_fixed} 条")


# Fix food.csv: only allow /static/images/food/ images
print("\n" + "=" * 60)
print("修复 food.csv — 美食只使用美食图片")
food_count, food_fixed = fix_csv(
    'food.csv',
    img_col=5,
    allowed_prefixes=['/static/images/food/'],
    fallback_img=lambda: random.choice(FOOD_IMAGES)
)
print(f"  总计: {food_count} 条, 修复: {food_fixed} 条")


# ==================== 验证 ====================
print("\n" + "=" * 60)
print("验证结果:")

for fname, col, label in [
    ('spots.csv', 5, '景点'),
    ('universities.csv', 6, '学校'),
    ('food.csv', 5, '美食'),
]:
    with open(os.path.join(BASE_DIR, 'data', 'raw', fname), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        rows = [r for r in reader if r and r[0].strip()]

    spot_imgs = sum(1 for r in rows if len(r) > col and '/spots/' in r[col])
    food_imgs = sum(1 for r in rows if len(r) > col and '/food/' in r[col])
    default_imgs = sum(1 for r in rows if len(r) > col and 'default' in r[col].lower())

    status = "OK" if (
        (label == '美食' and spot_imgs == 0) or
        (label in ('景点', '学校') and food_imgs == 0)
    ) else "ISSUE"

    print(f"  {label}: {len(rows)} 条 | spots图: {spot_imgs} | food图: {food_imgs} | default: {default_imgs} [{status}]")

print("\n完成！")
