#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
指定されたディレクトリ以下の、
正規表現で指定された拡張子のファイルを
テキストファイルに書かれたフルパスの場所に移動させる。
正規表現が指定されなければデフォルト値が使用される。
"""

import sys
import os
import re
import shutil as sh


def print_help(filename):
    print("Usage: python3 {} ./search/path paths_memo.txt ['ext_regex']".format(filename))


def check_arg(arg_num):
    argvs = sys.argv
    argc = len(argvs)
    if argc <= arg_num:
        print_help(argvs[0])
        quit()
    else:
        return argvs


def main():
    argvs = check_arg(2)  # 引数の数は2つは必要

    search_path = argvs[1]
    path_memo = argvs[2]
    try:
        ext_regex = argvs[3]
    except IndexError:
        ext_regex = '(\.mp4|\.mkv|\.ass|\.srt|\.srt\.bak|\.xml|\.swf|\[IchibaInfo\]\.html|\[Owner\]\.xml|\[ThumbImg\]\.jpeg|\[ThumbInfo\]\.xml)$'

    # search_path = '.'
    # path_memo = '../paths_memo.txt'

    reobj = re.compile(ext_regex)

    # build dst paths dict
    dst_paths = dict()
    cwd = os.getcwd()
    with open(path_memo, encoding='utf-8') as file:
        for path in file:
            full_path = os.path.normpath(os.path.join(cwd, path.rstrip()))
            dst_paths[os.path.basename(full_path)] = os.path.dirname(full_path)
            # print(full_path + "\n" + path)

    for root, dirs, files in os.walk(search_path):
        # print("root: {},\n\tdirs: {},\n\tfiles: {}".format(root, dirs, files))
        for filename in [tgt for tgt in files if reobj.search(tgt)]:
            src_fullpath = os.path.normpath(os.path.join(cwd, root, filename))
            # print(src_fullpath)

            # move tgt dst
            # print(os.path.dirname(src_fullpath) + "\n" + dst_paths[filename])
            src_fulldir = os.path.dirname(src_fullpath)
            dst_fulldir = dst_paths[filename]
            if src_fulldir != dst_fulldir:
                print("target: {}\n  from: {}\n  to:   {}\n".format(filename, src_fulldir, dst_fulldir))
                try:
                    sh.move(src_fullpath, dst_fulldir)
                    pass
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
