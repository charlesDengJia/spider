#!/bin/bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
echo "hello world !"


echo "开始插入" >> /Users/jiadeng/Downloads/test.txt
cd /Users/jiadeng/Downloads/machinelearningown/spider/newsspider/newsspider/extras/script




# 创建任务并将任务上送job 到redis
python scheduler.py -c product_config -a create -d sohu.com -r news_product_sohu

