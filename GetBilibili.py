# !/usr/bin/python
# -*- coding:utf-8 -*-
# Ver: 1.0
# 项目地址: https://github.com/xzy103/GetBilibili
# 原项目地址: https://github.com/Henryhaohao/Bilibili_video_download
# __OriginalAuthor__ == 'Henry'
# __Author__ == 'xzy103'


import os
os.system('color F2')
os.system('title Bilibili Download Tool')
print('感谢原作者 Henry :)')
print('>>>>>程序启动中...')
import time
import hashlib
import urllib.request
import re
import sys
try:
    import requests
    import moviepy.editor as mv
    import easygraphics.dialog as dlg
except ImportError:
    os.system('echo 缺乏运行所需的第三方库 正在为您安装...')
    os.system('pip install --user requests moviepy easygraphics')
    os.system('pause')
    import requests
    import moviepy.editor as mv
    import easygraphics.dialog as dlg

welcome = """在原项目基础上做了以下改变
- 优化代码结构
- 优化提示信息
- 调整运行界面风格
- 增加图形界面窗口
- 删除.mp4选项(格式问题)
- 删除第二种进度条显示方式
- 默认下载到桌面
- 使用最新的requests库
- 使用最新的moviepy库
- 需要安装easygraphics库
"""


def get_play_list(start_url, cid, quality):
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = f'appkey={appkey}&cid={cid}&otype=json&qn={quality}&quality={quality}&type='
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = f'https://interface.bilibili.com/v2/playurl?{params}&sign={chksum}'
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36'
    }
    html = requests.get(url_api, headers=headers).json()
    video_list = [html['durl'][0]['url']]
    return video_list


def Schedule_cmd(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = f"{pervent * 100:.2f}%"
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    f.write('\r')


# 字节bytes转化K\M\G
def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return f"{G:.3f} G/s"
        else:
            return f"{M:.3f} M/s"
    else:
        return f"{kb:.2f} K/s"


#  下载视频
def down_video(video_list, title, start_url, page):
    num = 1
    print(f'>>>>>正在下载P{page}段视频... | <{title}>:') if len(cid_list) > 1 else print('>>>>>下载中...')
    path = os.path.join(desktoppath, 'Bilibili_download', title)  # 当前目录作为下载目录
    for u in video_list:
        opener = urllib.request.build_opener()
        opener.addheaders = [
            # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
            ('Referer', start_url),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        if not os.path.exists(path):
            os.makedirs(path)  # 创建文件夹存放下载的视频
        flv = fr'{title}-{num}.flv' if len(video_list) > 1 else fr'{title}.flv'
        urllib.request.urlretrieve(url=u, filename=os.path.join(path, flv), reporthook=Schedule_cmd)  # 开始下载
        num += 1
    sys.stdout.write('\n')


# 合并视频
def combine_video(video_list, title):
    currentVideoPath = os.path.join(desktoppath, 'bilibili_video', title)  # 当前目录作为下载目录
    if len(video_list) >= 2:
        # 视频大于一段才要合并
        print(f'>>>>>下载完成,正在合并...:')
        ls = []
        root_dir = currentVideoPath
        fils = sorted(os.listdir(root_dir), key=lambda x: int(x[x.rindex("-") + 1:x.rindex(".")]))
        for file in fils:
            if os.path.splitext(file)[1] == '.flv':
                filepath = os.path.join(root_dir, file)  # 拼接成完整路径
                video = mv.VideoFileClip(filepath)  # 载入视频
                ls.append(video)

        final_clip = mv.concatenate_videoclips(ls)  # 拼接视频
        final_clip.to_videofile(os.path.join(root_dir, fr'{title}.mp4'), fps=24, remove_temp=False)  # 生成目标视频文件
        print(f'>>>>>视频合并完成!')
    else:
        print('>>>>>视频下载完成!')  # 视频只有一段则直接打印下载完成
    print()


if __name__ == '__main__':
    os.system('cls')
    print('-' * 30 + 'B站视频下载小助手' + '-' * 30)
    print(welcome)
    print('>>>>>获取视频地址...')
    desktoppath = os.path.join(os.path.expanduser("~"), 'Desktop')
    start = dlg.get_string(message='请输入您要下载的B站av号或视频链接地址', title='BilibiliDownload')
    start = start if start.isdigit() else re.search(r'/av(\d+)/*', start).group(1)
    start_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + start

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    html = requests.get(start_url, headers=headers).json()
    data = html['data']
    video_title = data["title"].replace(" ", "_")
    cid_list = []
    if '?p=' in start:
        p = re.search(r'\?p=(\d+)', start).group(1)
        cid_list.append(data['pages'][int(p) - 1])  # 单独下载分P视频中的一集
    else:
        cid_list = data['pages']  # 如果p不存在就是全集下载

    print('>>>>>获取下载清晰度...')
    tip = f"共{len(cid_list)}个视频\n{data['title']}\n请选择下载清晰度"
    quality = dlg.get_choice(message=tip, choices=['1080p', '720p', '480p', '360p'], title='BilibiliDownload')
    quality = {'1080p': '80', '720p': '64', '480p': '32', '360p': '16'}[quality]
    os.system('cls')
    try:
        for item in cid_list:
            cid = str(item['cid'])
            title = item['part']
            if not title:
                title = video_title
            title = re.sub(r'[/\\:*?"<>|]', '', title)  # 替换为空的
            page = str(item['page'])
            start_url = start_url + "/?p=" + page
            video_list = get_play_list(start_url, cid, quality)
            start_time = time.time()
            down_video(video_list, title, start_url, page)
            combine_video(video_list, title)
        print(f'用时{round(time.time()-start_time)}s')
    except Exception as e:
        print(e)
        input()
    # 如果是windows系统，下载完成后打开下载目录
    currentVideoPath = os.path.join(desktoppath, 'Bilibili_download')
    print(f'文件路径 {currentVideoPath}')
    if sys.platform.startswith('win'):
        os.startfile(currentVideoPath)
    os.system('pause')
    sys.exit()

