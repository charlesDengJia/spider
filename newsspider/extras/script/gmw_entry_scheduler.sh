#!/bin/bash
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


cd /Users/jiadeng/Downloads/machinelearningown/spider/newsspider/newsspider/extras/script



python write_entries.py -f entries/gmw.txt && python scheduler.py -c entry_config -a create -d gmw.cn -r news_entry_gmw