#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Taggor():
    def __init__(self, tag, attrs={}):
        self.name = tag
        self.tag_itr = []
        attr_str = ' '.join(['%s="%s"' % (k, v) for k, v in attrs.items()])
        first_item = '<' + tag + ' ' + attr_str + '>'
        last_item = '</' + tag + '>'
        self.tag_itr.append(first_item)
        self.tag_itr.append(last_item)

    def add_item(self, item):
        self.tag_itr.insert(-1, item)

    def get_tag(self):
        return ''.join(self.tag_itr)
