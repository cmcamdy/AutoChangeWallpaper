import re
import requests
import time
from lxml import etree
import random
import threading
import os
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
base_path = "D:/DesktopImages"

def get_img_url_from_wallpaper_random(time=0):

    base_url = "https://wallpaper.wispx.cn/random"
    try:
        rep = requests.get(base_url, headers=headers)
        html = etree.HTML(rep.text)
        print(rep.text)
        imgurl = html.xpath(
            "//img/@src")[0]

        return imgurl
    except:
        print("爬取错误")
        time = time+1
        if time < 5:
            get_img_url_from_wallpaper_random(time)


def get_img_url_from_wallpaper_by_index(index, time=0):

    base_url = "https://wallpaper.wispx.cn/detail/{}"
    try:
        url = base_url.format(index)
        rep = requests.get(url, headers=headers)
        html = etree.HTML(rep.text)
        # print(rep.text)
        imgurl = html.xpath(
            "//a[@class='mdui-ripple mdui-ripple-white']/@href")[0]

        return imgurl, url
    except:
        print("爬取错误")
        time = time+1
        if time < 5:
            get_img_url_from_wallpaper_by_index(index, time)


def get_img_url_from_obzhi(index, time=0):
    base_url = "http://www.obzhi.com/{}.html"
    url = base_url.format(index)

    try:
        rep = requests.get(url, headers=headers)
        html = etree.HTML(rep.text)
        # print(rep.text)
        imgurl = html.xpath("//*[@id='post_content']/p[2]/a/img/@src")[0]
        return imgurl
    except:
        print("爬取错误")
        time = time+1
        if time < 5:
            get_img_url_from_obzhi(random.randint(30, 3000), time)

        # get_img_url_from_obzhi(url)


def down_img_as_wallpaper(imgurl, url, i):
    header = headers
    header["referer"] = url
    rep = requests.get(imgurl, headers=header)
    # 不存在就创建一个
    if os.path.exists(base_path) == False:
        os.mkdir(base_path)
    if rep.status_code == 200:
        with open('{}/wallpaper{}.jpg'.format(base_path,i), 'wb') as f:
            f.write(rep.content)
    print("thread", i, "下载完成" if rep.status_code == 200 else "下载失败")


def multi_thread_wallpaper():
    
        t = []
        for i in range(10):
            img_index = random.randint(2, 883)
            # print(img_index)
            try:
                img_url, referer_url = get_img_url_from_wallpaper_by_index(img_index)
                t.append(threading.Thread(target=down_img_as_wallpaper, name="{}".format(
                    i), args=(img_url, referer_url, i)))
                # t.append(threading.Thread(target=down_img_as_wallpaper, name="{}".format(
                # i), args=(get_img_url_from_wallpaper_random(), i)))
                t[i].start()
                print("thread{}:start".format(i))
            except:
                print("thread{}:启动失败".format(i))
                pass


def multi_thread_obzhi():
    t = []
    for i in range(5):
        img_index = random.randint(30, 3000)

        t.append(threading.Thread(target=down_img_as_wallpaper, name="{}".format(
            i), args=(get_img_url_from_obzhi(img_index), i+10)))
        t[i].start()
        print("thread{}:start".format(i))


if __name__ == '__main__':
    # base_urls = ['https://wallpaper.wispx.cn/detail/{}',
    #              'http://www.obzhi.com/{}.html']
    # randrange = [[2, 883], [30, 3000]]
    multi_thread_wallpaper()
    # multi_thread_obzhi("http://www.obzhi.com/{}.html")
    # print("完成")
