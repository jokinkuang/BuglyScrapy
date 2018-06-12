# -*- coding:utf-8 -*-
# @author jokinkuang

from selenium import webdriver

import time
import json

from selenium.webdriver import chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import model
from model import KEY_TOTAL, KEY_NAME, KEY_LINK
from model import KEY_CRASH
from model import KEY_ANR
from model import KEY_ERROR
import mailer

# // Hard Code //

# step1.
QQ_USER_NAME = "2153413946@qq.com"#mailter.mail_user
QQ_PASSWORD = "bugly"#mailter.mail_pass

# 【使用QQ某个方便的登录页，s_url表示登录后跳转的页面】
LOGIN_URL = "https://ui.ptlogin2.qq.com/cgi-bin/login?appid=636026402&hln_css=https://mat1.gtimg.com/www/webapp/images/shipei_logo.png&style=8" \
            "&s_url=https%3a%2f%2fbugly.qq.com%2fv2%2fworkbench%2fapps&pt_no_onekey=1"
SUCCESS_URL = "https://bugly.qq.com/v2/workbench/apps"

# 【动态内容的根，Bugly所有页面都是动态生成的】
ROOT_ELEMENT = "return document.getElementById('root')"

# step2.

# 【列表】
#  <div class="_1bPqZ_46W99zJg_a_ceYQf">Welcome</div>  => Welcome
#  <a class="fwdCYw4oJ2IzdKsot4EmO" href="/v2/product/apps/82e5618042?pid=1">设置</a>  => 82e5618042?pid=1
APP_NAME_CLASS = "_1bPqZ_46W99zJg_a_ceYQf"
APP_ID_CLASS = "fwdCYw4oJ2IzdKsot4EmO"

# step3.

# @status 0=未处理 1=已处理 2=处理中 all=所有状态
# @date last_1_day=最近一天 last_7_day=最近7天 last_30_day=最近30天
def GET_SEARCH_URL(appId, date, status='all'):
    # https://bugly.qq.com/v2/crash-reporting/advanced-search/3cfeec429f?pid=1&status=0
    return "https://bugly.qq.com/v2/crash-reporting/advanced-search/"+appId+"&status="+status+"&date="+date

# 【搜索】
# <a class="btn btn_blue _2K0YWokiPhQguP-OdnwAzz">查询</a>
SEARCH_BTN_CLASS = "btn_blue"

# 【内容】
# <li class="main-content"><span>共 250 个异常（</span><span> 161 个崩溃，</span><span> 89 个ANR，</span><span> 0 个错误 ）</span></li>
SEARCH_CONTENT_CLASS = "main-content"


# // Hard Code End //

g_data = {
    "total":0,
    "crash":0,
    "anr":0,
    "error":0
}

g_appList = {
    "name":"",
    "data":{
        "not_handle":{
            "total":0,
            "crash":0,
            "anr":0,
            "error":0
        }
    }
}


g_browser = None
g_wait = None

def untilTrue(until):
    while True:
        if until():
            return

# @return object{ total crash anr error }
def search(url):
    global g_browser
    print "search:"+url

    g_browser.get(url)
    time.sleep(1)

    htmlElement = None
    while True:
        htmlElement = g_browser.execute_script(ROOT_ELEMENT)
        if htmlElement is not None:
            break
        time.sleep(1)


    g_wait.until(EC.presence_of_all_elements_located)

    btnSearch = None
    while True:
        btnSearch = htmlElement.find_element_by_class_name(SEARCH_BTN_CLASS)
        if btnSearch is not None:
            break
        time.sleep(1)


    # wait for document loaded
    g_wait.until(EC.presence_of_all_elements_located)
    # wait for btn clickable
    g_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, SEARCH_BTN_CLASS)))

    while True:
        try:
            btnSearch.click()
            break
        except:
            time.sleep(1)
            continue

    # wait for document loaded
    g_wait.until(EC.presence_of_all_elements_located)

    time.sleep(5)
    # wait for result

    content = g_browser.find_element_by_class_name(SEARCH_CONTENT_CLASS).text
    print content
    result = []
    list = content.split(' ')
    for item in list:
        if item.isdigit():
            result.append(item)
    obj = {}
    obj[KEY_LINK] = url
    obj[KEY_TOTAL] = 0
    obj[KEY_CRASH] = 0
    obj[KEY_ANR] = 0
    obj[KEY_ERROR] = 0
    if len(result) == 4:
        obj[KEY_TOTAL] = result[0]
        obj[KEY_CRASH] = result[1]
        obj[KEY_ANR] = result[2]
        obj[KEY_ERROR] = result[3]
    return obj
    pass


def login():
    global g_browser
    global g_wait

    g_browser.get(LOGIN_URL)
    time.sleep(1)
    g_wait.until(EC.presence_of_all_elements_located)

    input_str = g_browser.find_element_by_id('u')
    input_str.send_keys(QQ_USER_NAME)

    input_str = g_browser.find_element_by_id('p')
    input_str.send_keys(QQ_PASSWORD)

    button = g_browser.find_element_by_id('go')
    button.click()
    time.sleep(5)

    while True:
        if (SUCCESS_URL in g_browser.current_url):
            print ("Login Successful.")
            break
        time.sleep(2)
        print ("Login Failed. Waiting manual login.")
    pass

# @return appNameList[], appIdList[]
def get_app_list():
    global g_browser
    global g_wait

    htmlElement = None
    names = None
    while True:
        htmlElement = g_browser.execute_script(ROOT_ELEMENT)
        if htmlElement is not None:
            names = htmlElement.find_elements_by_class_name(APP_NAME_CLASS)
            if len(names) > 0:
                time.sleep(2)
                break
        time.sleep(1)

    names = htmlElement.find_elements_by_class_name(APP_NAME_CLASS)
    ids = htmlElement.find_elements_by_class_name(APP_ID_CLASS)

    appNameList = []
    appIdList = []
    for name in names:
        name = name.text
        appNameList.append(name)
        print name
    for id in ids:
        id = id.get_attribute('href')
        id = id[id.rindex('/') + 1: len(id)]
        appIdList.append(id)
        print id
    return appNameList, appIdList
    pass

def test():
    global g_browser
    g_browser.get("https://www.baidu.com/")
    print "https OK"

def main():
    global g_browser
    global g_wait
    startTime = time.time()
    chrome_options = chrome.options.Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--remote-debugging-port=9222')
    # chrome_options.binary_location = r'C:\Users\hldh214\AppData\Local\Google\Chrome\Application\chrome.exe'

    g_browser = webdriver.Chrome(chrome_options=chrome_options)
    g_wait = WebDriverWait(g_browser, 10) # wait for at most 10s

    print "## step1. login ##"
    login()

    print "## step2. get app list ##"
    appNameList, appIdList = get_app_list()

    print "## step3. get app crash data ##"

    dataList = []
    for i in range(len(appNameList)):
        print "name:"+appNameList[i]
        appId = appIdList[i]

        result = []
        searchNotHandleUrl = GET_SEARCH_URL(appId, "", "0")
        result1 = search(searchNotHandleUrl)
        result1[KEY_NAME] = appNameList[i]
        result1[KEY_LINK] = GET_SEARCH_URL(appId, "")
        result.append(result1)

        searchLast1DayUrl = GET_SEARCH_URL(appId, "last_1_day")
        result2 = search(searchLast1DayUrl)
        result2[KEY_NAME] = appNameList[i]
        result2[KEY_LINK] = GET_SEARCH_URL(appId, "")
        result.append(result2)
        dataList.append(result)
    print dataList

    print "## step4. send email. ##"
    print "mail to:" + str(model.getRecievers())
    mailer.sendEmail(model.getRecievers(), model.getSubject(), model.generateMailHtmlText(dataList))

    print "## Time Cost: " + model.getPassTime(startTime)

    print "## finally. quit browser ##"
    g_browser.quit()



    # print "=============="
    # innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    # print innerHTML

    # browser.execute_script("function showAlert() { alert('success'); }; showAlert()");
    # browser.execute_script("console.log(typeof(pt_logout));");

# Main #
main()


