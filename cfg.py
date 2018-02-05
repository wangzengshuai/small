#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置的config文件
"""

from os.path import join

#   项目图片根目录
base_path = r'/code/persion/python/small_identity_code/small/data/'

origin_pic_folder = join(base_path, 'origin')  # 原始图像目录
bin_clear_folder = join(base_path, 'bin_clear')  # "原始图像 -> 二值 -> 除噪声" 之后的图片文件目录
cut_pic_folder = join(base_path, 'cut_pic')  # 分割后的只含有单个字母的图片 -> 打好标签后, 每个字母单独放置一个文件夹

test_cut_pic_folder = join(base_path, 'cut_test')  # 一组全为 5 的图片集，用于做简单的模型验证测试

# SVM训练相关路径
svm_root = join(base_path, 'svm_train')  # 用于SVM训练的特征文件
train_file_name = join(svm_root, 'train_pix_feature_xy.txt')  # 保存训练集的 像素特征文件
test_feature_file = join(svm_root, 'train_pix_feature_5.txt')  # 只以一组8数字的特征文件为例子来做简单的验证测试
model_path = join(svm_root, 'svm_model_file')  # 训练完毕后，保存的SVM模型参数文件
