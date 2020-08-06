#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging


class IHaveLogger:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
