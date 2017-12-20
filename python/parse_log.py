#!/bin/python
#encoding:utf-8
__author__ = 'huangqingwei'

import sys
import re
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
fileHandler = logging.FileHandler("process_log.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)


def reg(ss, pattern, pos=0):
    match = pattern.search(ss)
    if match:
        return match.group(pos)
    return "-"


pattern_pkg = re.compile(r'pkg=(.*?)(&|\t)')
pattern_versionName = re.compile(r'vn=(.*?)(&|\t)')

# input: access.log
# output: pkg   vn
def extract_pkg_vn(ins, split_char='\t'):
    for line in ins:
        line_arr = line.strip().split(split_char)
        query_string = line_arr[8]
        pkg = reg(query_string, pattern_pkg, 1)
        vn = reg(query_string, pattern_versionName, 1)
        print "%s\t%s" % (pkg, vn)
        

def parse_access_log(ins, split_char='\t'):
    summary = {}
    line_cnt = 0
    for line in ins:
        try:
            line_arr = line.strip().split(split_char)
            query_string = line_arr[8]

            pkg = reg(query_string, pattern_pkg, 1)
            vn = reg(query_string, pattern_versionName, 1)

            stat_key = "%s\t%s" % (pkg, vn)
            summary.setdefault(stat_key, 0)
            summary[stat_key] += 1
            line_cnt += 1
            if line_cnt % 100000 == 0:
                logger.debug("parse count: %d" % line_cnt)
        except:
            continue
    return summary


if __name__ == "__main__":
    extract_pkg_vn(sys.stdin)
