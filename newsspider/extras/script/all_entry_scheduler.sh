#!/bin/bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-



cd /Users/jiadeng/Downloads/machinelearningown/spider/newsspider/newsspider/extras/script

# qq
/anaconda3/bin/python write_entries.py -f entries/qq.txt && /anaconda3/bin/python scheduler.py -c entry_config -a create -d qq.com -r news_entry_qq


# souhu
/anaconda3/bin/python write_entries.py -f entries/souhu.txt && /anaconda3/bin/python scheduler.py -c entry_config -a create -d sohu.com -r news_entry_sohu


# wangyi
/anaconda3/bin/python write_entries.py -f entries/wangyi.txt && /anaconda3/bin/python scheduler.py -c entry_config -a create -d 163.com -r news_entry_wangyi

# gmw
/anaconda3/bin/python write_entries.py -f entries/gmw.txt && /anaconda3/bin/python scheduler.py -c entry_config -a create -d gmw.cn -r news_entry_gmw