#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from taggor import Taggor

pat_entities = [
    {
        'name': 'title1',
        'key': '(^#\s)(.*)',
        'editor': r'<p style="height:32px;line-height:32px;"><font style="font-size: 15px; color: #cfcfcf;">\1</font>' + 
            r'<span style="font-size: 24px; color: #d33131;font-weight: bold;">\2</span></p>',
        'previewer': r'<p style="height:32px;line-height:32px;"><span style="font-size: 24px; color: #d33131;font-weight: bold;">\2</span></p>',
        'catalogue': r'<p style="font-size:18px;">\2</p>',
        'tag': None
    },
    {
        'name': 'title2',
        'key': '(^##\s)(.*)',
        'editor': r'<p style="height:30px;line-height:30px;"><font style="font-size: 15px; color: #cfcfcf;">\1</font>' + 
            r'<span style="font-size: 22px; color: #7ac70c; font-weight: bold;">\2</span></p>',
        'previewer': r'<p style="height:30px;line-height:30px;"><span style="font-size: 22px; color: #7ac70c; font-weight: bold;">\2</span></p>',
        'catalogue': r'<p style="font-size:18px;padding-left:2em;">\2</p>',
        'tag': None
    },
    {
        'name': 'title3',
        'key': '(^###\s)(.*)',
        'editor': r'<p style="height:28px;line-height:28px;"><font style="font-size: 15px; color: #cfcfcf;">\1</font>' + 
            r'<span style="font-size: 20px; color: #1cb0f6; font-weight: bold;">\2</span></p>',
        'previewer': r'<p style="height:28px;line-height:28px;"><span style="font-size: 20px; color: #1cb0f6;font-weight: bold;">\2</span></p>',
        'catalogue': r'<p style="font-size:18px;padding-left:4em;">\2</p>',
        'tag': None
    },
    {
        'name': 'title4',
        'key': '(^####\s)(.*)',
        'editor': r'<p style="height:26px;line-height:26px;"><font style="font-size: 15px; color: #cfcfcf;">\1</font>' + 
            r'<span style="font-size: 18px; color: #8549ba; font-weight: bold;">\2</span></p>',
        'previewer': r'<p style="height:26px;line-height:26px;"><span style="font-size: 18px; color: #8549ba;font-weight: bold;">\2</span></p>',
        'catalogue': r'<p style="font-size:18px;padding-left:6em;">\2</p>',
        'tag': None
    },
    {
        'name': 'title5',
        'key': '(^#####\s)(.*)',
        'editor': r'<p style="height:24px;line-height:24px;"><font style="font-size: 15px; color: #cfcfcf;">\1</font>' + 
            r'<span style="font-size: 16px; color: #4c4c4c;font-weight: bold;">\2</span></p>',
        'previewer': r'<p style="height:24px;line-height:24px;"><span style="font-size: 16px; color: #4c4c4c;font-weight: bold;">\2</span></p>',
        'catalogue': r'<p style="font-size:18px;padding-left:8em;">\2</p>',
        'tag': None
    },
    {
        'name': 'title6',
        'key': '(^######\s)(.*)',
        'editor': r'<p style="height:24px;line-height:24px;"><font style="font-size: 15px; color: #cfcfcf;">\1</font>' + 
            r'<span style="font-size: 15px; color: #14d4f4;font-weight: bold;">\2</span></p>',
        'previewer': r'<p style="height:24px;line-height:24px;"><span style="font-size: 15px; color: #14d4f4;font-weight: bold;">\2</span></p>',
        'catalogue': r'<p style="font-size:18px;padding-left:10em;">\2</p>',
        'tag': None
    },
    {
        'name': 'quote',
        'key': '(^>\s)(.*)',
        'editor': r'<p style="height:24px;line-height:24px;"><font style="font-size:15px;color:#cfcfcf;">\1</font>' + 
            r'<span style="font-size:15px;color:#888888;">\2</span></p>',
        'previewer': r'<p style="height:24px;line-height:24px;"><span style="font-size:15px;color:#888888;">\2</span></p>',
        'tag': None
    },
    {
        'name': 'italic',
        'key': '([^\\*]|^)(\\*{1})([^\\*]+)(\\*{1})([^\\*]|$|\s)',
        'editor': r'\1<font style="font-size:15px;color:#cfcfcf;">\2</font><i>\3</i><font style="font-size:15px;color:#cfcfcf;">\4</font>\5',
        'previewer': r'\1<i>3</i>\5',
        'tag': None
    },
    {
        'name': 'strong',
        'key': '([^\\*]|^)(\\*{2})([^\\*]+)(\\*{2})([^\\*]|$|\s)',
        'editor': r'\1<font style="font-size:15px;color:#cfcfcf;">\2</font><strong>\3</strong><font style="font-size:15px;color:#cfcfcf;">\4</font>\5',
        'previewer': r'\1<strong>\3</strong>\5',
        'tag': None
    },
    {
        'name': 'itastrong',
        'key': '([^\\*]|^)(\\*{3})([^\\*]+)(\\*{3})([^\\*]|$|\s)',
        'editor': r'\1<font style="font-size:15px;color:#cfcfcf;">\2</font><i><strong>\3</strong></i><font style="font-size:15px;color:#cfcfcf;">\4</font>\5',
        'previewer': r'\1<i><strong>\3</strong></i>\5',
        'tag': None
    },
    {
        'name': 'delete',
        'key': '([^~]|^)(~{2})([^~]+)(~{2})([^~]|$|\s)',
        'editor': r'\1<font style="font-size:15px;color:#cfcfcf;">\2</font><s>\3</s><font style="font-size:15px;color:#cfcfcf;">\4</font>\5',
        'previewer': r'\1<s>\3</s>\5',
        'tag': None
    },
    {
        'name': 'underline',
        'key': '([^\\+]|^)(\\+{2})([^\\+]+)(\\+{2})([^\\+]|$|\s)',
        'editor': r'\1<font style="font-size:15px;color:#cfcfcf;">\2</font><u>\3</u><font style="font-size:15px;color:#cfcfcf;">\4</font>\5',
        'previewer': r'\1<u>\3</u>\5',
        'tag': None
    },
    {
        'name': 'highlight',
        'key': '([^=]|^)(={2})([^=]+)(={2})([^=]|$|\s)',
        'editor': r'\1<font style="font-size:15px;color:#cfcfcf;">\2</font><span style="background-color:yellow;">\3</span><font style="font-size:15px;color:#cfcfcf;">\4</font>\5',
        'previewer': r'\1<span style="background-color:yellow;">\3</span>\5',
        'tag': None
    },
    {
        'name': 'linka',
        'key': '(\[)([^\[\]\s]+)(\])(\()([^\(\)]+)(\))',
        'editor': r'\1\2\3\4<a href="\5">\5</a>\6',
        'previewer': r'<a href="\5">\2</a>',
        'tag': None
    },
    {
        'name': 'orderlist',
        'key': '(\*\s)(.+)',
        'editor': r'<li><font style="font-size:15px;color:#cfcfcf;">\1</font>\2</li>',
        'previewer': r'<li>\2</li>',
        'tag': 'ol'
    },
    {
        'name': 'notorderlist',
        'key': '(\+\s)(.+)',
        'editor': r'<li>\1\2</li>',
        'previewer': r'<li>\2</li>',
        'tag': 'ul'
    }
]

pat_ul = [
    {
        'name': 'orderlist',
        'key': '(\*\s)(.+)',
        'editor': r'<li>\1\2</li>',
        'previewer': r'<li>\2</li>',
        'tag': 'ol'
    },
    {
        'name': 'notorderlist',
        'key': '(\+\s)(.+)',
        'editor': r'<li>\1\2</li>',
        'previewer': r'<li>\2</li>',
        'tag': 'ul'
    }
]

class LConverter():
    def __init__(self, article, source='html'):
        self.article = article
        self.soup = BeautifulSoup(article, features='html.parser')
        self.source = source

    def to_editor(self):
        '''
        将输入文章根据markdown语法转换为相应格式的html片段
        此时，需要保留markdown语法关键字，以轻灰色标记出这些关键字
        '''
         
        return self._get_html() 

    def to_previewer(self):
        '''
        将输入文章根据markdown语法转换为相应格式的html片段
        此html片段即浏览器中显示给最重用户的展示效果
        '''
        return self._get_html(style='previewer')

    def to_text(self):
        '''
        去除article中的html标签，保留内容和markdown语法关键字
        '''
        return self._get_text()

    def to_catalogue(self):
        '''返回目录结构（提取标题内容）'''
        html_str = ''
        if self.source == 'html':
            for item in self.soup.body.children:
                if item.name == 'p':
                    p_str = ''
                    if item.string is not None:
                        p_str = item.string
                    else:
                        for item_in_p in item.children:
                            p_str += item_in_p.string if item_in_p.string is not None else ''

                    for pat in pat_entities:
                        reg = re.compile(pat['key'])
                        p_str = re.sub(reg, pat['editor'], p_str)
                    if p_str.startswith('<p'):
                        html_str += p_str
        
        return html_str


    def _get_html(self, style='editor'):
        '''为编辑区的html文本添加markdown解析标签和样式'''
        html_str = ''
        self.tag_of_list = None # 有序列表或无序列表
        self.flowing = 0 # 0代表当前没有可用
        if self.source == 'html':
            for item in self.soup.body.children:
                # 1 如果当前标签为ul或ol：
                if item.name in ['ol', 'ul']:
                    print(11, str(item))
                # 2 判断当前tag_of_list为None，则设置tag_of_list为当前标签，并将标签内li插入
                    if self.tag_of_list is None or self.tag_of_list.name != item.name:
                        self.tag_of_list = Taggor(item.name)

                    for li_in_item in item.children:
                        self.tag_of_list.add_item(str(li_in_item))
                    html_str += self.tag_of_list.get_tag()

                if item.name == 'p':
                    p_str = ''
                    if item.string is not None:
                        p_str = item.string
                    else:
                        for item_in_p in item.children:
                            p_str += item_in_p.string if item_in_p.string is not None else ''

                    for pat in pat_entities:
                        reg = re.compile(pat['key'])
                        p_str = re.sub(reg, pat[style], p_str) 
                        if pat['tag'] is not None:
                            self.list_tag = pat['tag']

                    if p_str == '':
                        p_str = '<p style="height:20px;line-height:20px;margin:0px;"><br/></p>' 
                    elif p_str.startswith('<li'):
                        if self.tag_of_list is None or self.tag_of_list.name != self.list_tag:
                            self.tag_of_list = Taggor(self.list_tag)

                        self.tag_of_list.add_item(p_str)
                        p_str = self.tag_of_list.get_tag()
                        print(10, p_str)
                    elif not p_str.startswith('<p'):
                        p_str = '<p style="height:20px;line-height:20px;margin:0px;">' + p_str + '</p>'
                    
                    html_str += p_str
        elif self.source == 'markdown':
            for item in self.article.splitlines():
                p_str = item
                for pat in pat_entities:
                    reg = re.compile(pat['key'])
                    p_str = re.sub(reg, pat[style], p_str)
                if p_str == '':
                    p_str = '<p style="height:20px;line-height:20px;margin:0px;"><br/></p>'
                if not p_str.startswith('<p'):
                    p_str = '<p style="height:20px;line-height:20px;margin:0px;">' + p_str + '</p>'
 
                html_str += p_str
        #print(html_str)
        return html_str

    #def _get_tag_text(self):
        '''获取标签内部文本，如果有子标签，则循环获取文本'''
        
    
    def _get_text(self):
        '''将编辑区的html文本删除标签，仅保留纯markdown文本标签'''
        html_str = ''
        if self.source == 'html':
            for item in self.soup.body.children:
                if item.name == 'p':
                    p_str = ''
                    if item.string is not None:
                        p_str = item.string 
                    else:
                        for item_in_p in item.children:
                            p_str += item_in_p.string if item_in_p.string is not None else ''
                    p_str += '\n'
                    html_str += p_str

        return html_str
                
