#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
svm 特征提取
"""
import os
import sys
from os.path import join
reload(sys)
sys.setdefaultencoding("utf-8")

current_file_path = os.path.abspath(__file__)
current_dir_file_path = os.path.dirname(__file__)

from PIL import Image
from imgs_tools import get_pixel
from cfg import *


def get_feature(im):
    """
        获取指定图片的特征值,
        1. 按照每排的像素点,高度为13,则有13个维度,然后为13列,总共13个维度
        :param im:
        :return:一个维度为26（高度）的列表
    """
    w, h = im.size
    pixel_cnt_list = []
    for x in range(w):
        pix_cnt_x = 0
        for y in range(h):
            if get_pixel(im, (x, y)) == 0:
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for y in range(h):
        pix_cnt_y = 0
        for x in range(w):
            if get_pixel(im, (x, y)) == 0:
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list


def convert_values_to_str(dig, dif_list):
    """
    将特征值串转化为标准的svm输入向量:

    9 1:4 2:2 3:2 4:2 5:3 6:4 7:1 8:1 9:1 10:3 11:5 12:3 13:3 14:3 15:3 16:6

    最前面的是 标记值，后续是特征值
    :param dig: 对应的结果 (str)
    :param dif_list: 特征集合
    :type dif_list: list[int]
    :return:
    """
    line = '%s' % dig
    for index, value in enumerate(dif_list):
        line += ' %s:%s' % (index+1, value)
    print line
    return line


def convert_imgs_to_feature_file(dig, svm_feature_file, img_folder):
    """
    将某个目录下二进制图片文件，转换成特征文件
    :param dig:检查的字母
    :param svm_feature_file: svm的特征文件完整路径
    :type dig: str
    :return:
    """
    listdir = os.listdir(img_folder)

    for dir in listdir:
        im = Image.open(img_folder + '/' + dir)
        feature_list = get_feature(im)

        line = convert_values_to_str(dig, feature_list)
        svm_feature_file.write(line)
        svm_feature_file.write('\n')


def get_svm_train_txt():
    """
    获取 测试集 的像素特征文件。
    所有的字母的可能分类为36，分别放在以相应的数字命名的目录中
    存入内容为 ord(str)
    :return:
    """
    d = u'abcdefghigklmnopqrstuvwxyz0123456789'
    svm_feature_file = open(train_file_name, 'w')

    for x in d:
        img_folder = join(cut_pic_folder, x)
        if os.path.exists(img_folder):
            convert_imgs_to_feature_file(ord(x), svm_feature_file, img_folder)


def get_svm_test_txt():
    """
    获取 测试集 的像素特征文件
    :return:
    """

    img_folder = r'E:\code\persion\python\small_identity_code\small\data\cut_test\a'
    test_file = open(r'E:\code\persion\python\small_identity_code\small\data\cut_test\a\aa.txt', 'w')
    convert_imgs_to_feature_file(ord('a'), test_file, img_folder)  # todo 先用0代替
    test_file.close()


def get_one_test_txt():
    img_path = 'E:\\a.png'
    svm_feature_file = open('E:\\a.txt', 'w')
    im = Image.open(img_path)
    feature_list = get_feature(im)

    line = convert_values_to_str(ord('h'), feature_list)
    svm_feature_file.write(line)
    svm_feature_file.write('\n')


def convert_feature_to_vector(feature_list):
    """将特征集合转化为标准svm特征向量"""
    index = 1
    xt_vector = []
    feature_dict = {}
    for item in feature_list:
        feature_dict[index] = item
        index += 1
    xt_vector.append(feature_dict)
    return xt_vector


# get_svm_test_txt()
# get_one_test_txt()
