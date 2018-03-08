#!/usr/bin/env python
# Author: 'JiaChen'


class BaseResponse(object):
    """响应类"""
    def __init__(self):
        self.status = True
        self.message = None
        self.data = None
        self.error = None
