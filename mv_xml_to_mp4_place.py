#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tgt_dir 以下のファイルにおいて
ext_regex の文字列を含むファイルは
ext_regex 以外の部分文字列が
dst_ext の文字列を含み、dst_ext以外の部分文字列が同じ
dst_ext のパスに移動される
"""

import sys
import os
import re


def print_help(filename):
    print("Usage: python3 {} text".format(filename))


def check_arg(arg_num):
    argvs = sys.argv
    argc = len(argvs)
    if argc <= arg_num:
        print_help(argvs[0])
        quit()
    else:
        return argvs


def main():
    argvs = check_arg(1)  # 引数の数は1つは必要

    # tgt_ext_set = {'.xml', '[IchibaInfo].html', '[Owner].xml', '[ThumbImg].jpeg', '[ThumbInfo].xml'}
    # tgt_ext_list = ['*.xml', '*[IchibaInfo].html', '*[Owner].xml', '*[ThumbImg].jpeg', '*[ThumbInfo].xml', '*.m4b']
    # tgt_ext_str = '*(.xml|[IchibaInfo].html|[Owner].xml|[ThumbImg].jpeg|[ThumbInfo].xml)'
    # tgt_ext_regex = '.*(\.xml|\[IchibaInfo\]\.html|\[Owner\]\.xml|\[ThumbImg\]\.jpeg|\[ThumbInfo\]\.xml)'
    ext_regex = '(\.mp4|\.mkv|\.ass|\.srt|\.srt\.bak|\.xml|\.flv|\.swf|\[IchibaInfo\]\.html|\[Owner\]\.xml|' \
                '\[ThumbImg\]\.jpeg|\[ThumbInfo\]\.xml)'

    # tgt_dir = '/Volumes/Users/ats/Music/iTunes/iTunes Media'
    tgt_dir = argvs[1]
    # print("tgt_dir: " + tgt_dir)

    dst_ext = '.mkv'
    # dst_ext = argvs[1]

    # find contents
    reobj = re.compile(ext_regex)
    tgt_files = dict()
    dst_files = dict()
    for root, dirs, files in os.walk(tgt_dir):
        # for file_ in [n for n in files if reobj.match(n)]:
        for file_ in [reobj.split(n) for n in files if reobj.search(n)]:
            name = file_[0]
            ext = file_[1]
            # print(name, ext)
            full_path = os.path.join(root, ''.join(file_))
            if ext == dst_ext:
                dst_files[name] = full_path
                # print('dst_files[{}]: {}'.format(name, dst_files[name]))
            else:
                if name not in tgt_files:
                    tgt_files[name] = [full_path]
                else:
                    cur_value = tgt_files[name]
                    cur_value.append(full_path)
                    tgt_files[name] = cur_value
                    # print('tgt_files[{}]: {}'.format(name, tgt_files[name]))
    # print('tgt_files: {}'.format(tgt_files))
    # print('dst_files: {}'.format(dst_files))
    # exit()

    # move tgt dst
    import shutil as sh

    for dst_name, dst_path in dst_files.items():
        try:
            tgt_paths = tgt_files[dst_name]
        except KeyError:
            continue

        for tgt_path in tgt_paths:
            tgt_dir = os.path.dirname(tgt_path)
            dst_dir = os.path.dirname(dst_path)
            if tgt_dir == dst_dir:
                continue

            print("mv {} {}".format(tgt_path, dst_dir))
            try:
                sh.move(tgt_path, dst_dir)
            except FileNotFoundError:
                print('FileNotFoundError')
                pass
            except OSError:
                print('OSError: すでにあります')
                # dst_name, dst_ext = os.path.splitext(dst_path)
                # tgt_name, tgt_ext = os.path.splitext(tgt_path)
                # print("mv {} {}".format(tgt_path, "{}_2{}".format(dst_name, tgt_ext)))
                # sh.move(tgt_path, "{}_2{}".format(dst_name, tgt_ext))

# for script
if __name__ == '__main__':
    main()
