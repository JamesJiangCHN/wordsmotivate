#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author Michael Ding <dingyan@freestorm.org>
"""

import httplib
import datetime
import os.path

conn = httplib.HTTPConnection("img.wordsmotivate.me")

def build_list(suffix, start_day=datetime.date(2010,6,20), end_day=datetime.date.today()):
    """
    build path list and filename list
    """
    path_list = []
    filename_list = []
    delta = datetime.timedelta(days=1)

    d = start_day
    while d<= end_day:
        path_list.append("/" + d.strftime("%Y.%m/%Y.%m.%d").replace(".0", ".") + suffix)
        filename_list.append(d.strftime("%Y.%m.%d").replace(".0", ".") + suffix)
        d += delta

    return {
            "path_list":path_list,
            "filename_list":filename_list
            }

def get_pics(conn, dirname, path_list, filename_list):
    """
    get pics according conn, dirname, path_list, filename_list
    @conn: a httplib.HTTPConnection object
    @dirname: name of the directory which will store the pictures
    @path_list: a list of paths of the pictures on the Internet
    @filename_list: a list of filenames which map to the path_list,
        and will be used when store the pictures
    """
    if len(path_list) != len(filename_list):
        raise RuntimeError
    for i in range(len(path_list)):
        filename = os.path.join(dirname, filename_list[i])
        path = path_list[i]
        if not os.path.exists(filename):
            print "="*15
            print "Fetching: %s" % path
            conn.request("GET", path)
            resp = conn.getresponse()
            if resp.status == 200:
                out = open(filename, "wb")
                out.write(resp.read())
                print "Successfully saved as %s" % filename
            else:
                print """Failed to download.\n
                Error code:\n%d.""" % resp.status


if __name__ == "__main__":
    import sys
    import argparse

    res_choices = {
            '1':"1920x1080",
            '2':"1920x1200",
            '3':"1600x1200"
            }

    parser = argparse.ArgumentParser(description='Script to download wallpaper from WordsMotivate.me')
    parser.add_argument("-a", "--auto", action = "store_true", default = False)
    parser.add_argument("-r","--resols", type = str, default = '1', choices=[1,2,3],
            help = """choose the resolutions of pictures to be downloaded\n
            There are three choices:\n
            '1':'1920x1080',\n
            '2':'1920x1200',\n
            '3':'1600x1200'
            """
            )
    parser.add_argument("-d", "--dest", type = str, default = ".",
            help = """The destination directory to store the downloaded pictures"""
            )
    parser.add_argument("-s", "--start", type = int, nargs=3, metavar=("Y", "M", "D"),
            help = """The start of the range of days to download pictures.\n
            It can't be earlier than 2010/6/20\n
            The format of date is "Year" "Month" "Day" seperated with white spaces
            """
            )
    parser.add_argument("-e", "--end", type = int, nargs=3, metavar=("Y", "M", "D"),
            help = """The end of the range of days to download pictures.\n
            The format of date is "Year" "Month" "Day" seperated with white spaces
            """)
    args = parser.parse_args(sys.argv[1:])
    kwargs = vars(args)
    # process args
    if not kwargs["auto"]:
        # interaction mode
        #choose resolution
        resols = raw_input('Choose resolution you wish to download:\n1: %s\n2: %s\n3: %s\n Input your choice and press "Enter"' % (res_choices['1'],res_choices['2'],res_choices['3']))
        if resols not in res_choices:
            print "Invalid choice!"
            sys.exit(1)

        #choose start day
        in_d = raw_input("""The start of the range of days to download pictures.\n
            The format of date is "Year" "Month" "Day" seperated with white spaces\n
            Note: It can't be earlier than 2010/6/20\n
            If nothing input, default date is 2010/6/20""")
        if not in_d:
            start = datetime.date(2010,6,20)
        else:
            if len(in_d) != 3:
                print "Invalid date"
                sys.exit(1)
            try:
                y = int(in_d[0])
                m = int(in_d[1])
                d = int(in_d[2])
                start = datetime.date(y,m,d)
            except ValueError:
                print "Invalid date"
                sys.exit(1)

        #choose start day
        in_d = raw_input("""The end of the range of days to download pictures.\n
            The format of date is "Year" "Month" "Day" seperated with white spaces\n
            If nothing input, default date is TODAY""")
        if not in_d:
            end = datetime.date.today()
        else:
            if len(in_d) != 3:
                print "Invalid date"
                sys.exit(1)
            try:
                y = int(in_d[0])
                m = int(in_d[1])
                d = int(in_d[2])
                end = datetime.date(y,m,d)
            except ValueError:
                print "Invalid date"
                sys.exit(1)

        #input dest
        dt = raw_input("""Input the destiny directory where you want to store the pictures.\n
                Current directory will be used if nothing input""")
        if not dest:
            dest = "."
        else:
            if os.path.exists(dt) and os.path.isdir(dt):
                dest = dt
            else:
                print "Invalid directory!"
                sys.exit(1)

    else:
        resols = kwargs["resols"]
        dest = kwargs["dest"]
        if not (os.path.exists(dest) and os.path.isdir(dest)):
            print "PROG: error: argument --dest/-d: invalid directory"
        if kwargs["start"]:
            try:
                start = datetime.date(*kwargs["start"])
            except ValueError as e:
                print "PROG: error: argument --start/-s: %s" % e
                parser.print_help()
                sys.exit(1)
        else:
            start = datetime.date(2010,6,20)
        if kwargs["end"]:
            try:
                end = datetime.date(*kwargs["end"])
            except ValueError as e:
                print "PROG: error: argument --end/-e: %s" % e
                parser.print_help()
                sys.exit(1)
        else:
            end = datetime.date.today()

    suffix = '_%s.jpg' % res_choices[resols]
    st = build_list(suffix, start, end)
    try:
        get_pics(conn, dest, st["path_list"], st["filename_list"])
    except RuntimeError:
        print "Unexpected Error!"
        sys.exit(1)

