#!/usr/bin/env python
#coding=utf-8
import urllib2
import urllib
import re
import pytesser
import StringIO
import Image
import cookielib
import chardet
import time
class ScoreCrawl(object):
    def __init__(self , username = "******" ,password='******'):
        self.username = username
        self.password = password
        self.loginUrl ='http://yjxt.bupt.edu.cn/UserLogin.aspx?exit=1'
        self.imageUrl ='http://yjxt.bupt.edu.cn/Public/ValidateCode.aspx?image=1052561647'
        self.scoreUrl ='http://yjxt.bupt.edu.cn/Gstudent/Course/StudentScoreQuery.aspx?EID=l0RCAjrC!60Alnrcjky12Ad6vU4OJDrqYylAGKDjRFO3OCFxhesOvg==&UID='+username
        self.cookieJar = cookielib.CookieJar()
        httpHandler = urllib2.HTTPHandler(debuglevel=1)  
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)  
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar),httpHandler, httpsHandler)
        self.scores=[]
       
    def getImageCodeAndCookie(self):
        try:
            im = self.opener.open(self.imageUrl).read()       #获取验证码和cookies值
            img_buffer = StringIO.StringIO(im)
            img = Image.open(img_buffer)
            textcode = pytesser.image_to_string(img)
            print 'Cookies:'            
            for item in self.cookieJar:
                if item.name =='ASP.NET_SessionId':
                    self.sessionId = item.value
                print '    Name = '+item.name
                print '    Value = '+item.value  
            print 'ImageCode=',textcode
            return textcode
        except Exception as e:
            print 'Failed to get imagecode!', e
            return ''
    def login(self):
        postdata ={
                    'UserName':self.username,
                    'PassWord':self.password,
                    'drpLoginType':1,
                    'ScriptManager1':'UpdatePanel2|btLogin',
                     '__EVENTTARGET':'btLogin',
                     '__VIEWSTATE':'''/wEPDwULLTE3MzIzNjYwNjMPZBYCAgMPZBYGAg0PZBYCZg9kFgICAQ8PFgIeCEltYWdlVXJsBSp+L1B1YmxpYy9WYWxpZGF0ZUNvZGUuYXNweD9pbWFnZT0xOTg4NjIyMjlkZAIRD2QWAmYPZBYCAgEPEGRkFgFmZAIVD2QWAmYPZBYCAgEPDxYCHgtOYXZpZ2F0ZVVybAUtfi9QdWJsaWMvRW1haWxHZXRQYXNzd2QuYXNweD9FSUQ9VHVyOHZadXVYa3M9ZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDVZhbGlkYXRlSW1hZ2U=''',
                     '__EVENTVALIDATION':'/wEdAApk+MhPeRcW7LbXAbrLM7jrR1LBKX1P1xh290RQyTesRQa+ROBMEf7egV772v+RsRJUvPovksJgUuQnp+WD/+4LQKymBEaZgVw9rfDiAaM1opWKhJheoUmouOqQCzlwTSNWlQTw3DcvmMLY3PAqFoA+uFSTy5ozCEG4XBxL/Ykep0cgC/Irwlr9d8VObb8MnYO0GRqRfbdgDIW2dtIsr6rb',
                     '__ASYNCPOST':'true'
                    }
        code = self.getImageCodeAndCookie()
        postdata['ValidateCode']=code[:4]
        print 'postdata:',postdata
        postdata=urllib.urlencode(postdata)     # POST的数据
        myRequest = urllib2.Request(url = self.loginUrl,data = postdata)
        myRequest.add_header('Accept','*/*')
 #         myRequest.add_header('Content-Length','792')
        myRequest.add_header('Accept-Encoding','gzip,deflate,sdch')
        myRequest.add_header('Accept-Language','zh-CN,zh;q=0.8')
        myRequest.add_header('Cache-Control','no-cache')
        myRequest.add_header('Connection','keep-alive')
        myRequest.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
 #         myRequest.add_header('Cookie:LoginType','LoginType=1; ASP.NET_SessionId='+ self.sessionId)
        myRequest.add_header('Host','yjxt.bupt.edu.cn')
        myRequest.add_header('Origin','http://yjxt.bupt.edu.cn')
        myRequest.add_header('Referer','http://yjxt.bupt.edu.cn/UserLogin.aspx?exit=1')
        myRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 UBrowser/1.0.739.0 Safari/537.36')
        myRequest.add_header('X-MicrosoftAjax','Delta=true')
        myRequest.add_header('X-Requested-With','XMLHttpRequest')
        result = self.opener.open(myRequest).read()
        print result
           
    def getScores(self):
        scorePage = self.opener.open(self.scoreUrl).read()
           
         #统一编码格式
        charset = chardet.detect(scorePage)
        charset = charset['encoding']
        if charset !='utf-8' and charset !='UTF-8':
            scorePage = scorePage.decode('gb2312' , 'ignore').encode("utf-8")
        unicodePage = scorePage.decode('utf-8')
               
        pattern = re.compile('<td align="center">(\d*?)</td><td align="center">(.*?)</td><td align="center">(\d*?)</td><td align="center">(\d*?)</td><td align="center">(\d*?)</td><td align="center">(\d*?)</td><td align="center">(\d*?)</td><td align="center">(\d*?)</td><td align="center" nowrap="nowrap">(.*?)</td><td align="center" nowrap="nowrap">(.*?)</td><td align="center">&nbsp;</td>')
        scores = pattern.findall(unicodePage)
           
        for eachScore in scores:
            score={}
            score['classNo']=eachScore[0]
            score['className']=eachScore[1]
            score['classHours']=eachScore[2]
            score['credit']=eachScore[3]
            score['term']=eachScore[4]
            score['final']=eachScore[5]
            score['complex']=eachScore[6]
            score['rank']=eachScore[7]
            score['family']=eachScore[8]
            score['attribute']=eachScore[9]
            self.scores.append(score)
       
    def showScores(self):
        print '*'*200
        print '%30s%35s%32s%32s%32s%32s%32s%32s%30s%30s' % ('课程编号','课程名称','学时','学分','学期','期末','综合成绩','班级排名','类别','属性')
        for e in self.scores:
            print '%-30s%-35s%-32s%-32s%-32s%-32s%-32s%-32s%-30s%-30s' % (e['classNo'],e['className'],e['classHours'],e['credit'],e['term'],e['final'],e['complex'],e['rank'],e['family'],e['attribute'])
                
           
def main():
    scoreCrawl = ScoreCrawl()
    scoreCrawl.login()
    scoreCrawl.getScores()
    scoreCrawl.showScores()
    print '------'*20
   
if __name__ == '__main__':
    main()
