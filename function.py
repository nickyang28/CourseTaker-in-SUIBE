# -*- coding:utf-8 -*-
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from PIL import Image
import threading
import global_variable as gb_v
import warnings

warnings.filterwarnings('ignore')
import time
import DaPy as dp
from bs4 import BeautifulSoup as bs

dp.io.encode('utf-8')

url = "http://xk.suibe.edu.cn/xsxk/login.xk"


def get_safe_code():
    driver = WebDriver(executable_path='./phantomjs')
    driver.get(url)
    driver.maximize_window()
    driver.save_screenshot('test.png')
    gb_v.DRIVER = driver
    imgelement = driver.find_element_by_xpath('//*[@id="safecode"]')  # 定位验证码
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    rangle = (left, top, right, bottom)  # 写成我们需要截取的位置坐标
    i = Image.open("test.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('test.png')  # 保存我们接下来的验证码图片 进行打码
    '''
    pattern = re.compile(r'[0-9]{13}')
    result = pattern.findall(driver.page_source)
    Verifycodeurl = "http://xk.suibe.edu.cn/xsxk/servlet/ImageServlet?d=" + result[0]
    selenium_cookies = driver.get_cookies()
    JSESSIONID = selenium_cookies[0]['value']
    cookie = ''.join(['JSESSIONID=', JSESSIONID]).encode('ascii')
    headers = dict(Cookie=cookie)
    print Verifycodeurl
    pic = requests.get(Verifycodeurl, headers=headers)
    with open('test.png', 'wb') as f:
        f.write(pic.content)
    '''
    return True


def get_safe_code_again():
    driver = gb_v.DRIVER
    imgelement = driver.find_element_by_xpath('//*[@id="safecode"]')  # 定位验证码
    imgelement.click()
    time.sleep(0.5)
    driver.save_screenshot('test.png')
    location = imgelement.location  # 获取验证码x,y轴坐标
    size = imgelement.size  # 获取验证码的长宽
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    rangle = (left, top, right, bottom)  # 写成我们需要截取的位置坐标
    i = Image.open("test.png")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save('test.png')  # 保存我们接下来的验证码图片 进行打码
    return True


class xk_assistant(threading.Thread):
    def __init__(self, codes):
        threading.Thread.__init__(self)
        self.codes = codes
        self.driver = gb_v.DRIVER
        self.start()

    def run(self):
        try:
            data = self.login()
            if not data:
                gb_v.TUNNEL_F2D.append(False)
                return
            tj_codes, tyk_codes, qxg_codes, xgxkx_codes = self.code_classification(self.codes)
            # print tj_codes, tyk_codes, qxg_codes, xgxkx_codes
            self.recommend_xk(tj_codes)
            self.physical_xk(tyk_codes)
            self.public_xk(qxg_codes)
            self.interdisciplinary_xk(xgxkx_codes)
            useful_total = [code[-11:] for code in tj_codes] + [code[-11:] for code in tyk_codes] + [code[-11:] for code in
                                                                                               qxg_codes] + [code[-11:] for code in
                                                                                               xgxkx_codes]
            not_found_codes = list(set(self.codes) - set(useful_total))
            for code in not_found_codes:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code, u'请检查选课序号！'))
            gb_v.TUNNEL_F2D.append(None)
            gb_v.DRIVER.close()
            gb_v.DRIVER = None
        except Exception, e:
            print e
            gb_v.TUNNEL_F2D.append(False)

    def login(self):
        name_input = self.driver.find_element_by_id('username')  # 找到用户名的框框
        pass_input = self.driver.find_element_by_id('password')  # 找到输入密码的框框
        verify_input = self.driver.find_element_by_id('verifyCode')
        login_button = self.driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td[2]/input[1]')
        name_input.clear()
        name_input.send_keys(gb_v.USERNUMBER)  # 填写用户名
        pass_input.clear()
        pass_input.send_keys(gb_v.PASSWORD)  # 填写密码
        verify_input.clear()
        verify_input.send_keys(gb_v.VERIFYCODE)
        login_button.click()
        time.sleep(1)
        if u'贸易谈判学院' in self.driver.page_source:
            print 'Login Success'
            selenium_cookies = self.driver.get_cookies()  # 把selenium获取的cookies保存到变量，备用。
            '''
            pattern = re.compile(r'loadFaxklcs\(.[\d]{5}')
            result = pattern.findall(self.driver.page_source)
            global pyfaid
            pyfaid = result[-1][-5:]
            '''
            self.driver.find_element_by_xpath('//*[@id="mainFun"]/li[3]/a').click()
            JSESSIONID = selenium_cookies[0]['value']
            cookie = ''.join(['JSESSIONID=', JSESSIONID]).encode('ascii')
            gb_v.HEADERS['Cookie'] = cookie
            return True
        return False

    def recommend_xk(self, tj_codes=[]):
        for code in tj_codes:
            info = {'method': 'handleTjxk',
                    'jxbid': code,
                    'glJxbid': '',
                    'xyjc': ''}
            '''
            check = requests.get(
                'http://xk.suibe.edu.cn/xsxk/xkjs.xk?pyfaid=%s&jxqdm=2&data-frameid=main&data-timer=2000&data-proxy=proxy.xk' % pyfaid,
                headers=gb_v.HEADERS)
            '''
            r = requests.get('http://xk.suibe.edu.cn/xsxk/xkOper.xk', headers=gb_v.HEADERS, params=info)
            if 'false' not in r.text:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11:],
                                                      u'选课成功！'))
            else:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11:],
                                                      r.text.split('"')[5]))

    def physical_xk(self, tyk_codes=[]):
        for code in tyk_codes:
            info = {'method': 'handleTykxk',
                    'jxbid': code,
                    'glJxbid': '',
                    'xyjc': ''}

            r = requests.get('http://xk.suibe.edu.cn/xsxk/xkOper.xk', headers=gb_v.HEADERS, params=info)
            if 'false' not in r.text:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11],
                                                      u'选课成功！'))
            else:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11],
                                                      r.text.split('"')[5]))

    def public_xk(self, qxg_codes=[]):
        for code in qxg_codes:
            info = {'method': 'handleQxgxk',
                    'jxbid': code,
                    'glJxbid': '',
                    'xyjc': ''}
            r = requests.get('http://xk.suibe.edu.cn/xsxk/xkOper.xk', headers=gb_v.HEADERS, params=info)
            if 'false' not in r.text:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11:],
                                                      u'选课成功！'))
            else:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11:],
                                                      r.text.split('"')[5]))

    def interdisciplinary_xk(self, xgxkx_codes=[]):
        for code in xgxkx_codes:
            info = {'method': 'handleQxgxk',
                    'jxbid': code,
                    'glJxbid': '',
                    'xyjc': ''}

            r = requests.get('http://xk.suibe.edu.cn/xsxk/xkOper.xk', headers=gb_v.HEADERS, params=info)
            if 'false' not in r.text:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11:],
                                                      u'选课成功！'))
            else:
                gb_v.TUNNEL_F2D.append(gb_v.code_info(code[-11:],
                                                      r.text.split('"')[5]))

    def get_course_no(self, course_no, html_text):
        soup = bs(html_text, 'lxml')
        # course_no = ['107.124.201', '107.125.204', '107.126.201']
        useful_no = []
        all_no = []
        for x in soup.find_all(type="text/javascript"):
            if 'var jxbid = ' in str(x.string).strip():
                all_no.append(str(x.string).strip().split('var jxbid = ')[1].split(';')[0].strip('\''))

        for course in course_no:
            for no in all_no:
                if course in no[-11:]:
                    useful_no.append(all_no[all_no.index(no)])
                    break
        return set(useful_no)

    def code_classification(self, codes=[]):
        '''
        check = requests.get(
            'http://xk.suibe.edu.cn/xsxk/xkjs.xk?pyfaid=%s&jxqdm=2&data-frameid=main&data-timer=2000&data-proxy=proxy.xk' % pyfaid,
            headers=gb_v.HEADERS)
        '''
        '''
        tj_web = requests.get('http://xk.suibe.edu.cn/xsxk/tjxk.xk', headers=gb_v.HEADERS).text
        tyk_web = requests.get('http://xk.suibe.edu.cn/xsxk/tykxk.xk', headers=gb_v.HEADERS).text
        qxg_web = requests.get('http://xk.suibe.edu.cn/xsxk/qxgxk.xk', headers=gb_v.HEADERS).text
        xgxkx_web = requests.get('http://xk.suibe.edu.cn/xsxk/xgxkxxk.xk', headers=gb_v.HEADERS).text
        '''
        self.driver.get('http://xk.suibe.edu.cn/xsxk/tjxk.xk')
        tj_web = self.driver.page_source
        self.driver.get('http://xk.suibe.edu.cn/xsxk/tykxk.xk')
        tyk_web = self.driver.page_source
        self.driver.get('http://xk.suibe.edu.cn/xsxk/qxgxk.xk')
        qxg_web = self.driver.page_source
        self.driver.get('http://xk.suibe.edu.cn/xsxk/xgxkxxk.xk')
        xgxkx_web = self.driver.page_source
        # print qxg_web
        tj_codes = self.get_course_no(codes, tj_web)
        tyk_codes = self.get_course_no(codes, tyk_web)
        qxg_codes = self.get_course_no(codes, qxg_web)
        xgxkx_codes = self.get_course_no(codes, xgxkx_web)
        # print qxg_codes
        self.driver.close()
        self.driver.quit()
        return tj_codes, tyk_codes, qxg_codes, xgxkx_codes


if __name__ == '__main__':
    get_safe_code()
    gb_v.USERNUMBER = ''
    gb_v.PASSWORD = ''
    gb_v.VERIFYCODE = raw_input('>>')
    codes = ['454.001.201', '402.001.201', '701.010.204', '596.001.201']
    assis = xk_assistant(codes)
    assis.join()
    print gb_v.TUNNEL_F2D
