import json
import os
import pathlib
import random
import shutil
import threading
import time

import cv2
import os

from django.shortcuts import render, redirect

from DjangoVideo.settings import BASE_DIR
from myapp import models

# Create your views here.


def get_file_list(path_):
    """遍历视频图片"""
    for path, _, files in os.walk(path_):
        if files:
            for file in files:
                if file.endswith('.mp4') or file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                    file_path = os.path.join(path, file)
                    video = None
                    if file.endswith('.mp4'):
                        video = models.Video.objects.filter(video_name=file, video_path=str(file_path)).first()
                        if not video:
                            models.Video.objects.create(video_name=file, video_path=str(file_path))

                    # photo = models.Photo.objects.filter(image_name=file, image_path=str(file_path), video=video)
                    # if video and file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                    #     if not photo:
                    #         shutil.copy(str(file_path), './media/image')
                    #         models.Photo.objects.create(image_name=file, image_path=str(os.path.join('media', 'media', 'image', file)), video=video)


def video_to_frames(request):
    """获取视频封面"""
    video_s = models.Video.objects.filter()
    for video in video_s:
        photo_s = models.Photo.objects.filter(video=video)  # 每次获取 删除 旧的
        if photo_s:
            for photo_ in photo_s:
                if os.path.exists(str(photo_.image_path)):
                    os.remove(os.path.join(str(photo_.image_path)))
                photo_.delete()

        video_path = video.video_path
        # 如果文件目录不存在则创建目录
        out_path_dir = os.path.join('media', 'image')
        if not os.path.exists(out_path_dir):
            os.makedirs(out_path_dir)

        # 读取视频帧
        camera = cv2.VideoCapture(video_path)
        # 总帧数
        frames = camera.get(cv2.CAP_PROP_FRAME_COUNT)

        # 分为 15 等份
        times_list = []
        for index_ in range(15):
            times_list.append(int((frames / 15) * index_ + 1))

        # 帧率 -> 总时长
        # fps = camera.get(cv2.CAP_PROP_FPS)
        # print('总时长: ', frames / fps)

        for pi in times_list:
            camera.set(cv2.CAP_PROP_POS_FRAMES, pi)  # 设置要获取的帧号, 直接截取指定 帧
            res, image = camera.read()
            if not res:
                print('not res , not image')
                break

            file = str(time.time()) + '.jpg'
            out_path = os.path.join('media', 'image', file)
            photo = models.Photo.objects.filter(image_name=str(out_path), image_path=str(out_path), video=video)
            if not photo:
                models.Photo.objects.create(image_name=str(out_path), image_path=str(out_path), video=video)

                cv2.imwrite(out_path, image)

        print('图片提取结束')
        # 释放摄像头设备
        camera.release()
    return redirect('/')


def index(request):
    """首页"""
    path_s = models.Path.objects.filter(status=True)
    for path_ in path_s:
        get_file_list(path_.path)

    video_list = []
    video_s = models.Video.objects.filter().order_by('video_name')
    for video in video_s:
        photo_list = []
        photo_s = models.Photo.objects.filter(video=video)
        for photo in photo_s:
            if os.path.exists(str(photo.image_path)):
                photo_list.append(str(photo.image_path))
        video_list.append({'video_name': video.video_name, 'video_path': video.video_path, 'photo_list': photo_list})
    return render(request, 'index.html', {'video_list': video_list})


def play(request):
    """播放"""
    file_path = request.GET.get('file_path', '')
    print(file_path)
    import subprocess
    player = r'D:\Program Files (x86)\xlPlayer\Xmp\Program\XmpStart.exe '
    subprocess.call(player + file_path)
    return redirect('/')


