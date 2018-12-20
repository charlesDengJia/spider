#!/bin/bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

cd /Users/jiadeng/Downloads/machinelearningown/spider/newsspider/newsspider/extras/script




# qq
/anaconda3/bin/python scheduler.py -c product_config -a create -d qq.com -r news_product_qq

# sohu
/anaconda3/bin/python scheduler.py -c product_config -a create -d sohu.com -r news_product_sohu

# wangyi
/anaconda3/bin/python scheduler.py -c product_config -a create -d 163.com -r news_product_wangyi

# gmw
/anaconda3/bin/python scheduler.py -c product_config -a create -d gmw.cn -r news_product_gmw