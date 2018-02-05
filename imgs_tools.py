#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback
import uuid
import logging
import requests
import time
from PIL import Image
from PIL import ImageEnhance
from cfg import *

logger = logging.getLogger()
reload(sys)
sys.setdefaultencoding("utf-8")

current_file_path = os.path.abspath(__file__)
current_dir_file_path = os.path.dirname(__file__)
"""
    对图片操作
"""


def dowload():
    """
    下载素材图片
    :return:
    """
    url = 'https://www.bjgjj.gov.cn/wsyw/servlet/PicCheckCode1'
    for x in range(50):
        resp = requests.get(url, verify=False)
        if resp.status_code == 200:
            uuid_ = str(uuid.uuid1()).replace('-', '')
            with open('data/imgs/%s.png' % uuid_, 'wb') as f:
                f.write(resp.content)
                f.flush()
        time.sleep(0.5)


def to_bin(im):
    """
    去除图片的边界线,并二值化
    :return:
    """
    w_1, h_1 = im.size
    l_l = im.getpixel((1, 1))
    im2 = im.crop()
    im2 = im2.resize((w_1, h_1 + 1))
    im2.paste(im, im.getbbox())
    w, h = im2.size
    for wid in range(1, w - 1):
        od = im2.getpixel((wid, h - 2))
        if max(od) < 50:
            im2.putpixel((wid, h - 2), l_l)

    enhancer = ImageEnhance.Contrast(im2)
    im2 = enhancer.enhance(10).convert('1', )
    # im.save('b.jpg')
    w, h = im2.size
    im2 = im2.crop((1, 1, (w - 1), (h - 1)))
    return im2


def get_pixel(im, (x, y)):
    """
    返回改像素值的二值化
    :return: 黑0,白1
    """
    aa = im.getpixel((x, y))
    if aa > 140:
        return 1
    else:
        return 0


def remove_noise(im, count=1):
    """
    图片去噪,依据每个点周围8点,至少有3个点否则认为是噪音.
    四条上的点周边边少于两个黑点认为噪音.
    :return:
    """
    w, h = im.size
    data = im.getdata()
    black_point = 0
    for z in range(count):
        for x in xrange(0, w - 1):
            for y in xrange(0, h - 1):
                mid_pixel = data[w * y + x]  # 中央像素点像素值
                # print mid_pixel
                if mid_pixel == 0:  # 找出上下左右四个方向像素点像素值
                    top_pixel = data[w * (y - 1) + x]
                    left_pixel = data[w * y + (x - 1)]
                    down_pixel = data[w * (y + 1) + x]
                    right_pixel = data[w * y + (x + 1)]
                    # 对角四个点
                    top_pixel1 = data[w * (y - 1) + (x - 1)]
                    left_pixel1 = data[w * (y - 1) + (x + 1)]
                    down_pixel1 = data[w * (y + 1) + (x - 1)]
                    right_pixel1 = data[w * (y + 1) + (x + 1)]

                    # 判断上下左右的黑色像素点总个数
                    if top_pixel == 0:
                        black_point += 1
                    if left_pixel == 0:
                        black_point += 1
                    if down_pixel == 0:
                        black_point += 1
                    if right_pixel == 0:
                        black_point += 1

                    if top_pixel1 == 0:
                        black_point += 1
                    if left_pixel1 == 0:
                        black_point += 1
                    if down_pixel1 == 0:
                        black_point += 1
                    if right_pixel1 == 0:
                        black_point += 1

                    if black_point >= 3:
                        im.putpixel((x, y), 0)
                    else:
                        im.putpixel((x, y), 255)
                    black_point = 0

    # 对四个顶点处理
    if im.getpixel((0, 0)) == 0:
        im.putpixel((0, 0), 255)
    if im.getpixel((0, h - 1)) == 0:
        im.putpixel((0, h - 1), 255)
    if im.getpixel((w - 1, 0)) == 0:
        im.putpixel((w - 1, 0), 255)
    if im.getpixel((w - 1, h - 1)) == 0:
        im.putpixel((w - 1, h - 1), 255)

    # 对四条边进行处理
    # 上 下
    for w_u in range(1, w - 1):
        if im.getpixel((w_u, 0)) == 0:
            point_value = get_pixel(im, (w_u - 1, 0)) + get_pixel(im, (w_u + 1, 1)) \
                          + get_pixel(im, (w_u - 1, 1)) + get_pixel(im, (w_u, 1)) \
                          + get_pixel(im, (w_u + 1, 1))
            if point_value > 3:
                im.putpixel((w_u, 0), 255)
        if get_pixel(im, (w_u, h - 1)) == 0:
            point_value = get_pixel(im, (w_u - 1, h - 1)) + get_pixel(im, (w_u + 1, h - 1)) \
                          + get_pixel(im, (w_u - 1, h - 2)) + get_pixel(im, (w_u, h - 2)) \
                          + get_pixel(im, (w_u + 1, h - 2))
            if point_value > 3:
                im.putpixel((w_u, h - 1), 255)
    # 左 右
    for h_l in range(1, h - 1):
        if im.getpixel((0, h_l)) == 0:
            point_value = get_pixel(im, (0, h_l - 1)) + get_pixel(im, (0, h_l + 1)) \
                          + get_pixel(im, (1, h_l - 1)) + get_pixel(im, (1, h_l)) \
                          + get_pixel(im, (1, h_l + 1))
            if point_value > 3:
                im.putpixel((0, h_l), 255)
        if get_pixel(im, (w - 1, h_l)) == 0:
            point_value = get_pixel(im, (w - 1, h_l - 1)) + get_pixel(im, (w - 1, h_l + 1)) \
                          + get_pixel(im, (w - 2, h_l - 1)) + get_pixel(im, (w - 2, h_l)) \
                          + get_pixel(im, (w - 2, h_l + 1))
            if point_value > 3:
                im.putpixel((w - 1, h_l), 255)

    return im


def show_img(imgs):
    """
    图片展示
    :param imgs:
    :return:
    """
    if isinstance(imgs, list):
        for im in imgs:
            im.show()
    elif isinstance(imgs, Image.Image):
        imgs.show()


def split_img(im):
    """
    图片的切割 切割出来的图片大小为13*13
    1. 对 四条边进行一次
    :return:
    """

    """ x坐标    大小
        5-17	13
        18-30	13
        31-43	13
        44-56	13
    """
    im_list = []
    w, h = im.size
    for x in range(5, 57, 13):
        im_new = im.crop((x, 0, x + 13, h))
        im_list.append(im_new)
    final_img_list = []
    for img in im_list:
        w_i, h_i = img.size
        for a in range(h_i):  # 遍历每一行
            black_count = 0
            for b in range(w_i):  # 遍历每一点
                if get_pixel(img, (b, a)) == 0:
                    black_count += 1

            if black_count > 0:
                print '分割时数轴坐标为:%s 对应黑点数量为:%s' % (a, black_count)
                if black_count == 1 and a < 5:  # 判断此行是否为噪点

                    next_black_count = 0  # 判断下一行是否有黑点
                    for b in range(w_i):  # 遍历每一点
                        if get_pixel(img, (b, a + 1)) == 0:
                            next_black_count += 1
                    if next_black_count > 0:  # 有黑点证明此行非噪点
                        down_point = a + 13  # 判断最下方+1行是否为空白
                        down_count = 0
                        for b in range(w_i):  # 遍历每一列
                            if get_pixel(img, (b, down_point)) == 0:
                                down_count += 1
                        if down_count > 1:
                            final_img = img.crop((0, a + 1, w_i, a + 14))
                            # show_img(final_img)
                            final_img_list.append(final_img)
                            break

                final_img = img.crop((0, a, w_i, a + 13))
                # show_img(final_img)
                final_img_list.append(final_img)
                break

    return final_img_list


def read_img(img_path):
    """
    加载img图片
    """
    paths = os.listdir(img_path)
    result = []
    for path in paths:
        im = Image.open(path)
        result.append(im)
    return result


if __name__ == '__main__':

    dowload()
    listdir = os.listdir(base_path + 'imgs')
    start_time = time.time()
    print '程序开始'
    for last_dir in listdir:

        im = Image.open(base_path+'imgs' + '/' + last_dir)

        im = to_bin(im)
        im = remove_noise(im, 3)

        # im.save('%s/%s' % (bin_clear_folder, last_dir))

        try:
            imgs = split_img(im)
        except Exception as e:
            traceback.format_exc()
        for index in range(len(imgs)):
            imgs[index].save('%s/%s_%s' % (base_path + 'cut_test', index, last_dir))

    # raise TypeError('over')
    # listdir = os.listdir(origin_pic_folder)
    # start_time = time.time()
    # print '程序开始'
    # for last_dir in listdir:
    #
    #     im = Image.open(origin_pic_folder + '/' + last_dir)
    #
    #     im = to_bin(im)
    #     im = remove_noise(im, 3)
    #
    #     im.save('%s/%s' % (bin_clear_folder, last_dir))
    #
    #     try:
    #         imgs = split_img(im)
    #     except Exception as e:
    #         traceback.format_exc()
    #         print '出现错误,错误图片为: %s' % last_dir
    #         with open('error.log', 'a') as f:
    #             f.write(last_dir)
    #             f.write('\n')
    #             f.flush()
    #     for index in range(len(imgs)):
    #         imgs[index].save('%s/%s_%s' % (cut_pic_folder, index, last_dir))

    print '程序结束,用时:%s' % (time.time() - start_time)
