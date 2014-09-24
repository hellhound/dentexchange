# -*- coding:utf-8 -*-
import os
import sys


def path_init():
    this_dir = os.path.dirname(os.path.dirname(__file__))
    root_dir = os.path.join(this_dir, '.', 'dentexchange/project')
    project_dir = os.path.realpath(root_dir)
    sys.path.append(project_dir)


path_init()

bind = '127.0.0.1:9000'
workers = 10
errorlog = '-'
loglevel = 'critical'
