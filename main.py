#!/usr/bin/python
#-*-coding:utf-8-*-
'''
思路：
1.先获取到首页内容，
2.用正则来找到css,js和img的位置，
3.用当前时间来命名文件并在其下面新建css，js和image文件夹
4.将找到的css等文件写入该路径下，注：图片要以二进制的方式存取。
'''
import urllib2
import os
import re
from datetime import datetime
import time
import requests
import sys, getopt

class Spider():
    #获取页面,返回这个页面的字符串
    #url 是获取页面的url地址
    def getPage(self, url):
        try:
            response = urllib2.urlopen(url)
            #print response.read()
            return response.read()
        except urllib2.URLRrror:
            print u"连接失败"

    #读取页面中的css,js和img 
    #page 是传入页面的字符串形式
    #以字典的形式将css等信息返回
    def downloads(self, page):
        # 使用正则表达式来匹配页面中css的文件存储的位置
        pattern_css = re.compile('<link.*?href="(.*?css)"')
        pattern_js = re.compile('<script.*?src="(.*?js)"')
        #首页图片已jpg和png结尾
        pattern_img = re.compile('<img.*?src="(.*?)(jpg|png)"')
        css = re.findall(pattern_css, page)
        js = re.findall(pattern_js, page)
        img = re.findall(pattern_img, page)
        #将匹配到的图片名和图片的后缀名链接起来
        imgs = [m+n for m,n in img] 
        print '---------------------------'
        return {'css': css, 'js': js, 'imgs': imgs}

    #生成存储路径
    #将新生成的以时间命名的路径返回
    def makedir(self, directory):
        #判断路径是否存在
        if not os.path.exists(directory):
            os.mkdir(directory)
        #取到当前时间并将其转化成字符串
        date = str(datetime.now())
        #提取字符串中的数字取前12个作为路径名
        filename = filter(str.isalnum, date)[:12]
        newdir = directory + '/' + filename
        try:
            os.mkdir(newdir)
            #创建子目录css,ja,images
            list(os.mkdir(newdir + '/' + m) for m in ['css', 'js', 'images'])
            return newdir
        except:
            print u"文件已存在，请过一分钟后再试！"
            sys.exit()

    #将css等文件存储到本地
    #sohufile是downloads()方法返回的字典
    def store(self, sohufile, newdir, page):
        #将首页写入到home.html中
        open(newdir + r'/home.html', 'w+').write(page)

        #读取css的内容将其写入文件中，文件名以最后一个/后的内容命名
        for c in sohufile['css']:
            css_dir = newdir + r'/css/' + c.split('/')[-1]
            css_content = requests.get(c).content
            open(css_dir, 'w+').write(css_content)


        #写js文件
        for j in sohufile['js']:
            js_dir = newdir + r'/js/' + j.split('/')[-1]
            js_content = requests.get(j).content
            open(js_dir, 'w+').write(js_content)
            
        #写图面
        for i in sohufile['imgs']:
            imgs_dir = newdir + r'/images/' + i.split('/')[-1]
            imgs_content = requests.get(i).content
            open(imgs_dir, 'wb+').write(imgs_content)



if __name__ == '__main__':
    #在命令行上通过-d -u -o选项来传递参数
    options, args = getopt.getopt(sys.argv[1:], 'd:u:o:')
    for opt, value in options:
        if opt == '-d':
            t = int(value)
        if opt == '-u':
            u = value
        if opt == '-o':
            d = value
    count = 0
    s = Spider()
    while True:
        try:
            page = s.getPage(u) # r'http://m.sohu.com'
            sohufile = s.downloads(page)
            newdir = s.makedir(d)
            s.store(sohufile, newdir, page)
            count += 1
            print u'执行了 %d 次' % count
            #暂停60秒
            time.sleep(t)
        except KeyboardInterrupt:
            print u'程序已停止!'
            break
