#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

'''
analyze /proc/<pid>/smaps
分析进程Code占用的内存（Android中apk的dex，so库）
doc
http://liutaihua.github.io/2013/04/25/process-smaps-analysis.html
http://www.cnblogs.com/jiayy/p/3458076.html
http://www.cnblogs.com/bravery/archive/2012/06/27/2560611.html
'''

import re
import sys

head_regex = re.compile(r"[\da-f]+-[\da-f]+")
item_regex = re.compile(r"(\w+):\s*(\d+)\s*")


def is_head_line(line):
    return head_regex.search(line) != None


def get_head_line_name(line):
    m = re.search(' {3,}', line)
    if m != None:
        return line[m.end():].rstrip()
    # print("can't get name for:" + line)
    return "unknown"


def parse_smap(lines):
    smaps = {}
    i = 0
    while i < len(lines):
        name = get_head_line_name(lines[i])
        if name != None:
            name = name.rstrip()
        else:
            name = 'unknown'

        if not smaps.has_key(name):
            value_map = {}
            smaps[name] = value_map
        else:
            value_map = smaps[name]

        i += 1

        while i < len(lines) and not is_head_line(lines[i]):
            seg_line = lines[i]
            i += 1
            m = item_regex.search(seg_line)
            if m != None:
                type = m.group(1)
                size = m.group(2)
                size = int(size)
                if not value_map.has_key(type):
                    value_map[type] = size
                else:
                    value_map[type] = value_map[type] + size
    return smaps


def sort_smaps(smaps, by_type):
    return sorted(smaps.iteritems(), key=lambda (k, v): (v[by_type], k), reverse=True)


def print_if(smaps, if_cond=lambda name, map: True):
    NAME = "name"
    PSS = "Pss"
    RSS = "Rss"
    SIZE = "Size"
    OTHER = "other"

    print(PSS + "\t\t" + RSS + "\t\t" + SIZE + "\t\t" + NAME + "\t" + OTHER)

    for (name, map) in smaps:
        if if_cond(name, map):
            print("%d kB\t\t%d kB\t\t%d kB\t\t%s\t%s" % (map[PSS], map[RSS], map[SIZE], name, ""))


def count_if(smaps, type, if_cond=lambda name, map: True):
    count = 0
    for (name, map) in smaps:
        if if_cond(name, map):
            count += map[type]
    return count

######## custom report methods #############

def plot_chart(smaps):
    # order by pss
    smaps = sort_smaps(smaps, 'Pss' if len(sys.argv) < 3 else sys.argv[2])

    is_stack = lambda name, map: re.search('\[.*stack.*\]', name) != None
    all_so_maps_if = lambda name, map: re.search('\.so$', name) != None
    all_dex_maps_if = lambda name, map: re.search('\.(dex)|(odex)|(art)$', name) != None
    app_so_maps_if = lambda name, map: re.search('com\.tencent\.radio\.debug.*\.so$', name) != None
    app_lib_so_maps_if = lambda name, map: re.search('com\.tencent\.radio\.debug.*/lib/arm.*\.so$', name) != None
    app_dex_maps_if = lambda name, map: re.search('com\.tencent\.radio\.debug.*oat.*\.(dex)|(odex)|(art)$', name) != None
    app_lib_dex_maps_if = lambda name, map: re.search('com\.tencent\.radio\.debug.*oat.*\.(dex)|(odex)|(art)$', name) != None
    avlive_maps_if = lambda name, map: re.search('txav', name) != None
    tbs_maps_if = lambda name, map: re.search('tbs', name) != None

    print("all data")
    print_if(smaps)

    print("stack maps")
    print_if(smaps, is_stack)

    print("all so maps")
    print_if(smaps, all_so_maps_if)

    print("all dex maps")
    print_if(smaps, all_dex_maps_if)

    print("app so maps")
    print_if(smaps, app_so_maps_if)

    print("app lib so maps")
    print_if(smaps, app_lib_so_maps_if)

    print("app dex maps")
    print_if(smaps,  app_lib_dex_maps_if)

    print("avlive txav maps")
    print_if(smaps, avlive_maps_if)

    print("tbs maps")
    print_if(smaps, tbs_maps_if)

    print("")

    print("map Pss total = %d Kb" % count_if(smaps, 'Pss'))
    print("map Vss total = %d Kb" % count_if(smaps, 'Size'))

    print("stacks Pss = %d kB" % count_if(smaps, 'Pss', is_stack))
    print("stacks Vss = %d kB" % count_if(smaps, 'Size', is_stack))

    print("all so map Pss = %d kB" % count_if(smaps, 'Pss', all_so_maps_if))
    print("all so map Vss = %d kB" % count_if(smaps, 'Size', all_so_maps_if))

    print("all dex map Pss = %d kB" % count_if(smaps, 'Pss', all_dex_maps_if))
    print("all dex map Vss = %d kB" % count_if(smaps, 'Size', all_dex_maps_if))

    print("app so map Rss")
    print("app so map Rss = %d kB" % count_if(smaps, 'Rss', app_so_maps_if))
    print("app so map Vss = %d kB" % count_if(smaps, 'Size', app_so_maps_if))

    print("app dex map Rss")
    print("app dex map Rss = %d kB" % count_if(smaps, 'Rss', app_dex_maps_if))
    print("app  map Vss = %d kB" % count_if(smaps, 'Size', app_dex_maps_if))

    print("app_tbs")
    print("tbs mem map Pss = %d kB" % count_if(smaps, 'Pss', tbs_maps_if))

    print("avlive txav")
    print("tbs mem map Pss = %d kB" % count_if(smaps, 'Pss', avlive_maps_if))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if file == '-':
            file = sys.stdin
        else:
            file = open(file)

        lines = [l.strip('\n') for l in file.readlines()]

        smaps = parse_smap(lines)

        plot_chart(smaps)
    else:
        print(sys.argv[0] + " /proc/<pid>/smaps <order_by>")