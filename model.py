# -*- coding:utf-8 -*-
# @author jokinkuang
import time
from datetime import datetime

import mailer

KEY_LINK = "link"
KEY_NAME = "name"
KEY_TOTAL = "total"
KEY_CRASH = "crash"
KEY_ANR = "anr"
KEY_ERROR = "error"

MAIL_RECEIVERS = [
                  "kuangzukai@jokin.com"
                  ]
MAIL_SUBJECT = u"Bugly日报"

def getRecievers():
    return MAIL_RECEIVERS

def getSubject():
    return MAIL_SUBJECT

# @return "星期几"
def getDayOfWeek():
    weeks = [u"星期一",u"星期二",u"星期三",u"星期四",u"星期五",u"星期六",u"星期日"]
    dayOfWeek = datetime.now().weekday()
    return weeks[dayOfWeek]

# @return "00:00:00" from startTime
def getPassTime(startTime):
    return time.strftime(u"%H:%M:%S", time.gmtime(time.time()-startTime))

# @return "2018-01-01 00:00:00 星期几"
def getDateTime():
    datetime = time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return datetime + " " + getDayOfWeek()

def getTip():
    tip = u"所有未处理：了解应用的异常是否有跟进</br>"
    tip += u"昨天的异常：了解应用每天的异常情况"
    return tip

# 邮件正文一开始使用中文，邮件就能自动识别为utf-8编码，而使用英文，很可能引起邮件被以非utf-8编码打开！！！当然也可以强制指定邮件编码
def generateMailHtmlText(list):
    # generate from http://www.tablesgenerator.com/html_tables#
    html = u'''
    <style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;border-color:#aaa;}
.tg tr{font-family:Arial, sans-serif;font-size:14px;text-align:center;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#aaa;color:#333;background-color:#fff;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#aaa;color:#fff;background-color:#f38630;}
.tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
.tg .tg-7475{background-color:#FCFBE3;border-color:inherit;vertical-align:top}
.tg .tg-f{border-color:inherit;vertical-align:top}
.tg .tg-s{background-color:#f4f3f3;border-color:inherit;vertical-align:top}
</style>
<table class="tg">
  <tr><td colspan="10" style="border-style:none;">''' + getDateTime() + u'''</td></tr>
  <tr>
    <th class="tg-us36" rowspan="2"><br>应用名称</th>
    <th class="tg-c3ow" colspan="4">全部未处理异常</th>
    <th class="tg-us36"></th>
    <th class="tg-c3ow" colspan="4">昨天发生异常</th>
  </tr>
  <tr>
    <td class="tg-7475">总数</td>
    <td class="tg-7475">Crash</td>
    <td class="tg-7475">ANR</td>
    <td class="tg-7475">Error</td>
    <td class="tg-7475"></td>
    <td class="tg-7475">总数</td>
    <td class="tg-7475">Crash</td>
    <td class="tg-7475">ANR</td>
    <td class="tg-7475">Error</td>
  </tr>
    '''

    for index in range(len(list)):
        # 注意：使用%s与%格式化出现TypeError: not all arguments converted during string formatting没有成功，所以使用format格式化。
        item = list[index]
        row = u'<tr>'
        cls = 'tg-s'
        if index % 2 == 0:
            cls = 'tg-f'
        # create string formater.
        for i in range(10):
            row += u"<td class='"+cls+"'>{"+ str(i) + u'''}</td>'''
        row += u'</tr>'
        html += row.format("<a href='"+item[0][KEY_LINK]+"'>"+item[0][KEY_NAME]+"</a>",
                           item[0][KEY_TOTAL], item[0][KEY_CRASH], item[0][KEY_ANR], item[0][KEY_ERROR], " ",
                           item[1][KEY_TOTAL], item[1][KEY_CRASH], item[1][KEY_ANR], item[1][KEY_ERROR])

    html += u'''</table>'''
    html += getTip() + "</br>"
    print html
    return html

data = [
    [{
        KEY_LINK: "http://www.baidu.com",
        KEY_NAME: "demo1",
        KEY_TOTAL: "1",
        KEY_CRASH: "2",
        KEY_ANR: "3",
        KEY_ERROR: "4"
    }, {
        KEY_LINK: "http://www.baidu.com",
        KEY_NAME: "demo1",
        KEY_TOTAL: "1",
        KEY_CRASH: "2",
        KEY_ANR: "3",
        KEY_ERROR: "4"
    }]
    , [{
        KEY_LINK: "http://www.baidu.com",
        KEY_NAME: "demo2",
        KEY_TOTAL: "1",
        KEY_CRASH: "2",
        KEY_ANR: "3",
        KEY_ERROR: "4"
    },{
        KEY_LINK: "http://www.baidu.com",
        KEY_NAME: "demo2",
        KEY_TOTAL: "1",
        KEY_CRASH: "2",
        KEY_ANR: "3",
        KEY_ERROR: "4"
    }]
]

# Test #
# mailer.sendEmail(MAIL_RECEIVERS, MAIL_SUBJECT, generateMailHtmlText(data))
# print calCostTime(time.time())