#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-

f = open('config_file', 'r')
dict = {}
for lines in f:
    lines = lines.strip()
    token = lines.split('=')
    dict[token[0]] = token[1]