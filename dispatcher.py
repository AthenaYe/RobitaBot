#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import random

import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


class Dispatcher():

    rules = {}
    def __init__(self):
        f = open('rules', 'r')
        for lines in f:
            token = lines.strip().split("=")
            self.rules[token[0].encode('utf-8').decode('utf-8')] = token[1]

    def preprocess(self, word_list):
        word_list = re.sub('@.*_bot ', ' ', word_list)
        return word_list

    def dispatch(self, word_list):
        ans = []
        word_list = self.preprocess(word_list)
        for i in range(0, len(word_list)):
            word = ''
            for j in range(0,3):
                word = word_list[i:i+j+1]
                if self.rules.has_key(word):
                    ans.append(self.rules[word])
        length = len(ans)
        if length == 0:
            return u'洛比哒现在还很弱，不懂你在说什么0 0'
        return ans[random.randint(0, length-1)]

