#!/bin/bash
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
echo "hello world !"


cd /Users/jiadeng/Downloads/machinelearningown/spider/newsspider/newsspider/extras/script


/anaconda3/bin/python write_entries.py -f entries/wangyi.txt && /anaconda3/bin/python scheduler.py -c entry_config -a create -d 163.com -r news_entry_wangyi