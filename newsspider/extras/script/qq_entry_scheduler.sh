#!/bin/bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
echo "hello world !"


echo "开始插入" >> /Users/jiadeng/Downloads/test.txt
cd /Users/jiadeng/Downloads/machinelearningown/spider/newsspider/newsspider/extras/script


# 写入数据源
# 创建任务并将任务上送job 到redis
python write_entries.py -f entries/qq.txt && python scheduler.py -c entry_config -a create -d qq.com -r news_entry_qq