#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Zimeng Qiu <zimengq@andrew.cmu.edu>
# Licensed under the Apache License v2.0 - http://www.apache.org/licenses/

import os
<<<<<<< HEAD

=======
import re
import multiprocessing as mp
from glob import glob
>>>>>>> 8ca1d760cbb5966d0f96505b071a427524ca2211

def extract_files_data(file_paths):
    data = []
<<<<<<< HEAD
    for (dirpath, dirs, files) in os.walk(data_path):
        for file in files:
            with open(os.path.join(dirpath, file), "r") as f:
                lines = f.readlines()
                for line in lines:
                    text = []
                    for token in line.decode('UTF-8').split()[3:]:
                        if is_english_word(token.encode('ascii', 'ignore')) \
                                or (is_chinese_word(token) and len(token) == 1):
                            text.append(token)
                        else:
                            tmp = ""
                            for char in token:
                                if is_chinese_word(char):
                                    if len(tmp) > 0:
                                        text.append(tmp)
                                        tmp = ""
                                    text.append(char)
                                else:
                                    tmp += char
                    assert(all(len(word) == 1 for word in text if is_chinese_word(word)))
                    data.append([word.encode('UTF-8') for word in text])
=======
    for file_path in file_paths:
        with open(file_path, "r") as f:
            text = f.readlines()
            data.extend([[word for word in line.strip().split(" ")[3:] if word != '<v-noise>'] for line in text])
    return data

def read_dataset(data_path, num_workers=1):
    data = []
    all_file_paths = glob(os.path.join(data_path, '**/*.txt'), recursive=True)
    num_files = len(all_file_paths)
    files_per_worker = num_files // num_workers

    pool = mp.Pool(processes=num_workers)

    extraction_result = pool.map(extract_files_data,
                                 (all_file_paths[start_idx:start_idx+files_per_worker]
                                  for start_idx in range(0, num_files, files_per_worker)))

    for result in extraction_result:
        data.extend(result)
>>>>>>> 8ca1d760cbb5966d0f96505b071a427524ca2211
    return data


def is_english_word(word):
    """
    Decide if a token in a document is an valid English word.
    For this project, we define valid English words to be ASCII strings that
    contain only letters (both upper and lower case), single quotes ('),
    double quotes ("), and hyphens (-). Double quotes may only appear at the
    beginning or end of a token unless the beginning/end of a token is no-letter
    characters. Double quotes cannot appear in the middle of letter characters.
    (for example, "work"- is valid, but home"work and -bi"cycle- are not).
    Tokens cannot be empty.
    :param word: A token in document.
    :return: Boolean value, True or False
    """
    return all([char in ["\"", "\'", "-"] or char.isalpha() for char in word]) and len(word) > 0


def is_chinese_word(char):
    if len(char) > 1:
        return False
    ranges = [
        {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},  # compatibility ideographs
        {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},  # compatibility ideographs
        {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},  # compatibility ideographs
        {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},  # Japanese Hiragana
        {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},  # Japanese Katakana
        {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},  # cjk radicals supplement
        {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
        {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
    ]
    return any([range["from"] <= ord(char) <= range["to"] for range in ranges])