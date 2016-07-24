#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
import pickle

Urls = []
def GetUrl(text):
    return "http://45.32.249.213/ss/?q="+text

def SavePage(url,i):

        html = urllib.urlopen(url + "&p=" + str(i))
        html = html.read().decode("utf-8")
        urls = re.findall(r"/ss/\?a=url&k=.{1,}target", html)
        names = re.findall(r'nofollow">.{1,}?</a></h2>', html)
        for name in names:
            i = names.index(name)
            name = name[10:-9]
            if u'<b>' in name:
                a = name.split(u'<b>')[0] + name.split('<b>')[1]
                name = a.split(u"</b>")[0] + a.split("</b>")[1]
            names[i] = name
        for url in urls:
            urls[urls.index(url)] = "http://45.32.249.213" + urls[urls.index(url)].split('target')[0][:-2]
        print names[0]
        print urls[0]
        a = []
        a.append(names)
        a.append(urls)
        return a


def SaveHtml(text,num = 4):
    url = GetUrl(text)
    global Urls
    Urls = []
    for i in range(1,num):
        Urls.append(SavePage(url,i))
    try:
        f = open("result.pk",'wb')
    except:
        pass
    else:
        pickle.dump(Urls,f)
        f.close()

def LoadHtml():
    global Urls
    f = open("result.pk",'rb')
    Urls = pickle.load(f)

def GetPage(num):
    num = num-1
    if not Urls:
        LoadHtml()
    names = Urls[num][0]
    urls = Urls[num][1]
    for i in names:
        j = names.index(i)
        print names[j]
        print urls[j]

GetPage(1)














