#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
sys.path.append('C:\Python27\Lib\site-packages\libsvm\python')
from libsvm.python.svmutil import *
from libsvm.python.svm import *


from cfg import train_file_name, model_path, test_feature_file


def svm_model_train():
    """
    模型的训练
    :return:
    """
    y, x = svm_read_problem(train_file_name)
    model = svm_train(y, x)
    svm_save_model(model_path, model)


def svm_model_test():
    yt, xt = svm_read_problem(r'E:\a.txt')
    model = svm_load_model(model_path)
    p_label, p_acc, p_val = svm_predict(yt, xt, model)

    cnt = 0
    for item in p_label:
        print('%d' % item)

        cnt += 1
        if cnt % 8 == 0:
            print('')


# svm_model_test()

