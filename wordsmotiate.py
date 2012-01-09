#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author Michael Ding <dingyan@freestorm.org>
"""

import urllib
import os
import datetime
import sys

#判断运行参数，如果有参数，则设置为自动运行模式，否则交互模式
if len(sys.argv) == 2:
    auto = True
else:
    auto = False

#选择分辨率，自动运行模式下，分辨率由命令行参数指定，交互模式下由用户输入
resols = {
        '1':'1920x1080',
        '2':'1920x1200',
        '3':'1600x1200'
        }

if auto:
    choice = str(sys.argv[1])
else:
    choice = raw_input('Choose resolution you wish to download:\n1: %s\n2: %s\n3: %s\n' % (resols['1'],resols['2'],resols['3']))

if not resols.has_key(choice):
    print "Invalid Choice!\n"
    sys.exit(0)

#由选择得分辨率组成url后缀
urlbase = 'http://img.wordsmotivate.me/'
urlpostfix = '_%s.jpg' % resols[choice]

#设置起始日期位2010年6月21日
start_day = datetime.date(2011,7,25)

#选择截止日期，自动运行模式下，截止日期为当天，交互模式下由用户输入
if auto:
    end_day = datetime.date.today()
else:
    day_input = input('Input the end day untill witch you\'d like to fetch the wallpaper:\n(format: \'[year,month,day]\')\n')
    try:
        y = int(day_input[0])
        m = int(day_input[1])
        d = int(day_input[2])
        end_day = datetime.date(y,m,d)
    except:
        print 'Invalid Date!\n'
        sys.exit(0)

urllist = []
filenamelist = []

delta = datetime.timedelta(days=1)
d = start_day

#生成Url列表
while d <= end_day:
    urllist.append(urlbase + d.strftime("%Y.%m/%Y.%m.%d").replace('.0','.') + urlpostfix)
    filenamelist.append(d.strftime("%Y.%m.%d").replace('.0','.') + urlpostfix)
    d += delta

i = 0

#根据Url列表循环下载图片
for url in urllist:
    filename = filenamelist[i]
    if not os.path.exists(filename):
        print "fetching: %s\nto: %s" % (url, filename)
        try:
            urllib.urlretrieve(url,filename)
        except:
            print "fetch failed\n"
            if os.path.exists(filename):
                os.remove(filename)
                sys.exit(1)
    i+=1
