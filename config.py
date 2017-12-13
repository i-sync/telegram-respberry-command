#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import json


class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

#base_path = '/home/pi/monitor'
base_path = ''
with open('{}/config.json'.format(base_path), 'r') as f:
    config = json.load(f)
    #print(config)

Config = objectview(config)