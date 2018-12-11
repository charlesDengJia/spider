#!/bin/bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
echo "hello world !"



cd /Users/jiadeng/Downloads/machinelearningown/spider/newsspider/newsspider/extras/script

# qq 写入数据源
# 创建任务并将任务上送job 到redis
python write_entries.py -f entries/qq.txt && python scheduler.py -c entry_config -a create -d qq.com -r news_entry_qq


# souhu  写入数据源
# 创建任务并将任务上送job 到redis
python write_entries.py -f entries/souhu.txt && python scheduler.py -c entry_config -a create -d sohu.com -r news_entry_sohu


# wangyi  写入数据源
# 创建任务并将任务上送job 到redis
python write_entries.py -f entries/wangyi.txt && python scheduler.py -c entry_config -a create -d 163.com -r news_entry_wangyi