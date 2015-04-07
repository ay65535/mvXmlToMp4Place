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
    print("Usage: python3 {} ./target/path".format(filename))


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
    ext_regex = '(\.mp4|\.mkv|\.ass|\.srt|\.srt\.bak|\.flv|\.swf|\[IchibaInfo\]\.html|\[Owner\]\.xml|' \
                '\[ThumbImg\]\.jpeg|\[ThumbInfo\]\.xml|\.xml)$'

    # tgt_dir = '/Volumes/Users/ats/Music/iTunes/iTunes Media'
    tgt_dir = os.path.normpath(argvs[1])
    # print("tgt_dir: " + tgt_dir)

    dst_ext = '.mkv'
    # dst_ext = argvs[1]
    print("拡張子 {} の場所に {} にマッチするファイルを移動します。\n".format(dst_ext, ext_regex))

    # find contents
    reobj = re.compile(ext_regex)
    tgt_files = dict()
    dst_files = dict()
    for root, dirs, files in os.walk(tgt_dir):
        # TODO: avoid hard coding exclude folders
        if re.match("{}/(\.git|Automatically Add to iTunes|Mobile Applications|system)".format(tgt_dir), root):
            continue
        # print(root)
        # for file_ in [n for n in files if reobj.match(n)]:
        # for file_ in [n for n in files if reobj.search(n)]:
        for file_ in [reobj.split(n) for n in files if reobj.search(n)]:
            full_path = os.path.join(root, ''.join(file_))
            key_name = file_[0]
            match_str = file_[1]
            # print("{},\t{}".format(key_name, match_str))
            # nicowari_suffix = re.split("\[Nicowari\]\[nm[0-9]+\]$", key_name)
            # if len(nicowari_suffix) != 1:
            #     key_name = nicowari_suffix[0]
            video_id = re.search(" - \[(sm|so|nm)?[0-9]+\]", key_name)
            if not video_id:
                # print("{}\n{}\t{}\n\n".format(full_path, key_name, match_str))
                print("skipping {}".format(full_path))
                continue
            video_id = video_id.group(0)
            if match_str == dst_ext:
                dst_files[video_id] = full_path
                # print('dst_files[{}]:\n\t{}'.format(video_id, dst_files[video_id]))
            else:
                if video_id not in tgt_files:
                    tgt_files[video_id] = [full_path]
                else:
                    cur_value = tgt_files[video_id]
                    cur_value.append(full_path)
                    tgt_files[video_id] = cur_value
                    # print('tgt_files[{}]:\n\t{}'.format(video_id, tgt_files[video_id]))
    # print('tgt_files: {}'.format(tgt_files))
    # print('dst_files: {}'.format(dst_files))
    # exit()

    # move tgt dst
    import shutil as sh
    import datetime

    for dst_id, dst_path in dst_files.items():
        try:
            tgt_paths = tgt_files[dst_id]
        except KeyError:
            # print('KeyError')
            continue

        for tgt_path in tgt_paths:
            tgt_basename = os.path.basename(tgt_path)
            tgt_dir = os.path.dirname(tgt_path)
            dst_dir = os.path.dirname(dst_path)
            if tgt_dir == dst_dir:
                continue

            print("\ntarget: {}\n  from: {}\n    to: {}".format(tgt_basename, tgt_dir, dst_dir))
            try:
                sh.move(tgt_path, os.path.join(dst_dir, tgt_basename))
                pass
            except FileNotFoundError:
                print('FileNotFoundError')
                pass
            except OSError:
                print('OSError: すでにあります')
                stat = os.stat(tgt_path)
                last_modified = stat.st_mtime
                # print(last_modified)
                dt = datetime.datetime.fromtimestamp(last_modified)
                date_str = dt.strftime("%Y%m%d%H%M%S")
                dst_fulltitle, dst_ext = os.path.splitext(dst_path)
                tgt_fulltitle, tgt_ext = os.path.splitext(tgt_path)
                tgt_basetitle = os.path.basename(tgt_fulltitle)
                print("target: {}\n  from: {}\n    to: {}"
                      .format(tgt_basename, tgt_path, os.path.join(dst_dir, "{}_{}{}".format(tgt_basetitle, date_str, tgt_ext))))
                # print("\t" + tgt_path + " ->\n\t"
                #       + os.path.join(dst_dir, "{}_{}{}".format(tgt_basetitle, date_str, tgt_ext)))
                sh.move(tgt_path, os.path.join(dst_dir, "{}_{}{}".format(tgt_basetitle, date_str, tgt_ext)))

# for script
if __name__ == '__main__':
    main()
