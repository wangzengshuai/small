#! /usr/bin/env python
# -*- coding: utf-8 -*-
import io
import sys

sys.path.append('C:\Python27\Lib\site-packages\libsvm\python')
from libsvm.python.svmutil import *
import requests
from PIL import Image
from imgs_tools import *
from svm_feature import *


def crack_captcha():
    """
    破解验证码,完整的演示流程
    :return:
    """
    start_time = time.time()
    for x in range(50):
        url = 'https://www.bjgjj.gov.cn/wsyw/servlet/PicCheckCode1'
        res = requests.get(url, verify=False, stream=True)

        f = io.BytesIO()
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()

        im = Image.open(f)  # 从网络上请求验证码图片保存在内存中
        # im.show()
        imgs = split_img(remove_noise(to_bin(im), 3))

        model = svm_load_model(model_path)
        img_ocr_name = ''
        for img in imgs:
            feature_list = get_feature(img)
            yt = [0]  # 测试数据标签
            # xt = [{1: 1, 2: 1}]  # 测试数据输入向量
            xt = convert_feature_to_vector(feature_list)  # 将所有的特征转化为标准化的SVM单行的特征向量
            p_label, p_acc, p_val = svm_predict(yt, xt, model)
            img_ocr_name += ('%s' % chr(int(p_label[0])))  # 将识别结果合并起来

        im.save(test_cut_pic_folder + '/' + img_ocr_name + '.png')

        f.close()
    print '用时:%s' % (time.time()-start_time)

crack_captcha()
