# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com

import os
import re
import errno
import hashlib
import sys
from datetime import datetime
import string
import random
import glob
import shutil

# 1. utils to handle android logs like main.log, radio.log, kernel.log
# 2. find pid by keyword
# 3. line grep

class logutils():
    def __init__(self):
        pass

    class dotdict(dict):
        """dot.notation access to dictionary attributes"""
        def __getattr__(self, attr):
            return self.get(attr)
        __setattr__ = dict.__setitem__
        __delattr__ = dict.__delitem__

    def converttime(self, timestring):
        """
        fruit is "day time"
        input is android time format like: 09-21 18:17:34.556
        return should be datetime format
        :param orig:
        :return:
        """
        regex = "(\d+)-(\d+)[ \t](\d+):(\d+):(\d+)\.(\d+)"

        pattern = re.compile(regex)
        match = pattern.search(timestring)

        month = int(match.group(1).lstrip("0"))
        day = int(match.group(2).lstrip("0"))

        hour = int(match.group(3).lstrip("0"))
        minute = int(match.group(4).lstrip("0"))
        if match.group(5) == '00':
            sec = 0
        else:
            sec = int(match.group(5).lstrip("0"))
        microsec = match.group(6)

        microsec = '0.' + microsec
        microsec = float(microsec)
        microsec = int(microsec * 1000000)

        """
        # for microsec logic is wrong
        .067, .006
        microsec = microsec[:3]
        mlen = len(microsec)
        if mlen < 3:
            microsec += (3 - mlen) * '0'

        microsec = int(microsec) * 1000
        """

        output = datetime(year=datetime.today().year, month=month, day=day, hour=hour, minute=minute, second=sec, microsecond=microsec)
        #print output
        return output

    # similar to "mkdir -p"
    def mkdirp(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    # mv wildcard src file/dir to dst
    def mv(self, src, dst):
        if os.path.isdir(dst):
            for srcfile in glob.glob(src):
                shutil.move(srcfile, dst)
        else:
            print 'not dir'

    def checkint(self, s):
        s = s.strip()
        if s[0] in ('-', '+'):
            return s[1:].isdigit()
        return s.isdigit()

    def wordinline(self, word, line):
        if word in line:
            return True
        else:
            return False

    def patterninline(self, pattern, line):
        regex = re.compile(pattern)
        if regex.search(line):
            return True
        else:
            return False

    def findfields(self, fields):
        """
        log format is changed in android O
        00D347 08-23 19:57:51.585  1205  1254 D LEMON
        :return:
        """
        datepattern= "\d\d-\d\d"
        dpattern = re.compile(datepattern)
        first = fields[0]
        match = dpattern.match(first)
        fruit = dict()
        fruit['day'] = ""
        fruit['time'] = ""
        fruit['pid'] = ""
        if match:
            fruit['day'] = fields[0]
            fruit['time'] = fields[1]
            fruit['pid'] = fields[2]
        else:
            fruit['day'] = fields[1]
            fruit['time'] = fields[2]
            fruit['pid'] = fields[3]
        # pid should be integer, or return None
        if not self.checkint(fruit['pid']):
            fruit['pid'] = None
        return fruit

    def md5sum(self, file=''):
        try:
            fd = open(file, 'rb')
            content = fd.read()
            fd.close()
            md5 = hashlib.md5(content).hexdigest()
            return md5
        except:
            etype = sys.exc_info()[0]
            evalue = sys.exc_info()[1]
            estr = str(etype) + ' ' + str(evalue)
            raise RuntimeError(estr)

    def replaceSpace(self, src, char):
        return re.sub(r'[\s+]', char, src)


    def revertdict(self, orig):
        if orig:
            #https://stackoverflow.com/questions/483666/python-reverse-invert-a-mapping
            return {v: k for k, v in orig.iteritems()}
        else:
            return None

    def asciistr_generator(self, size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        #https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
        return ''.join(random.choice(chars) for _ in range(size))

    def int_generator(self, start, end):
        if end >= start:
            return random.randint(start,end)
        else:
            return random.randint(end, start)

if __name__ == "__main__":
    lutils = logutils()
    line = "02D429 08-31 16:18:20.260  4117  4286 I MME     : 16:18:20.260 MVD: INFO: StrmOpen rtp timeout 5 "
    print lutils.patterninline("MME.*MVD", line)

    beginstr = "08-31 16:18:20.260"
    begin = lutils.converttime(beginstr)

    endstr = "09-01 17:08:10.120"
    end = lutils.converttime(endstr)
    print lutils.md5sum("./logutils.py")

    print lutils.asciistr_generator(size=3, chars="zhihuaye")
    print lutils.int_generator(0,9)
    print lutils.int_generator(9,0)

    lutils.mv("mme.*log", 'test')
