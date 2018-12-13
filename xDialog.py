# -*- coding: utf-8 -*-
import json
import time
from threading import Thread

import requests
import wx
import wx.animate

import global_variable as gb_v
from function import get_safe_code


class Login_app(Thread):
    def __init__(self, username, in_psw):
        Thread.__init__(self)
        self._username = username
        self._in_psw = in_psw
        self.start()

    def run(self):
        try:
            gb_v.TUNNEL_L2I.append(u'正在连接服务器...')
            username, in_psw = self._username, self._in_psw
            gb_v.USERNAME = username
            r = requests.post('https://nickyang.info/login?username=' + username + '&password='+in_psw)
            gb_v.TUNNEL_L2I.append(u'获取验证信息...')
            dic = json.loads(r.text)
            if dic['states'] == 'ID_error':
                gb_v.TUNNEL_L2I.append('ID')
                # wx.MessageBox(u'用户名不存在！', u'选课助手', style=wx.ICON_ERROR)
                return False

            if dic['states'] == 'PSD_error':
                gb_v.TUNNEL_L2I.append('PSD')
                # wx.MessageBox(u'密码错误！', u'选课助手', style=wx.ICON_ERROR)
                return False

            if dic['times'] == 0:
                gb_v.TUNNEL_L2I.append('times')
                # wx.MessageBox(u'剩余次数为 0 ！', u'选课助手', style=wx.ICON_ERROR)
                return False

            student_number = dic['student_number']
            times = dic['times']

            gb_v.TUNNEL_L2I.append(u'连接选课网站...')
            if not get_safe_code():
                wx.MessageBox(u'选课网验证码获取失败, 请检查网络。', u'选课助手', style=wx.ICON_ERROR)

            gb_v.TUNNEL_L2I.append((student_number, times))
            return None

        except:
            gb_v.TUNNEL_L2I.append('net')
            # wx.MessageBox(u'网络链接失败！', u'选课助手', style=wx.ICON_ERROR)


class InputDialog(wx.Dialog):
    def __init__(self, parent, title, func_callBack):
        wx.Dialog.__init__(self, parent, -1, title, size=(300, 200))
        self.CenterOnScreen()
        self.timer = wx.Timer(self)
        self.icon = wx.Icon(u'Ico.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.Bind(wx.EVT_TIMER, self.Timer, self.timer)
        self.func_callBack = func_callBack
        self.InitUI()  # 绘制Dialog的界面

    def InitUI(self):
        panel = wx.Panel(self)
        # font = wx.Font(14, wx.DEFAULT, wx.BOLD, wx.NORMAL, True)

        accountLabel = wx.StaticText(panel, -1, u'账号：', pos=(20, 25))
        # accountLabel.SetFont(font)

        self.accountInput = wx.TextCtrl(panel, -1, u'', pos=(80, 25), size=(180, -1), style=wx.TE_PROCESS_ENTER)
        self.accountInput.SetForegroundColour('gray')
        # self.accountInput.SetFont(font)

        passwordLabel = wx.StaticText(panel, -1, u'密码：', pos=(20, 70))
        # passwordLabel.SetFont(font)

        self.passwordInput = wx.TextCtrl(panel, -1, u'', pos=(80, 70), size=(180, -1),
                                         style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        # self.passwordInput.SetFont(font)

        self.info = wx.StaticText(panel, -1, u'', pos=(0, 105), size=(180, 20))
        self.info.SetForegroundColour('#32CC32')

        self.sureButton = wx.Button(panel, -1, u'登录', pos=(20, 130), size=(240, 30))
        self.Bind(wx.EVT_BUTTON, self.sureEvent, self.sureButton)

        self.cancleButton = wx.Button(panel, -1, u'取消', pos=(160, 130), size=(120, 30))
        # self.Bind(wx.EVT_BUTTON, self.cancleEvent, self.cancleButton)
        self.cancleButton.Show(False)

        self.Bind(wx.EVT_TEXT_ENTER, self.sureEvent, None)

    def Timer(self, evt):
        if not gb_v.TUNNEL_L2I:
            return

        result = gb_v.TUNNEL_L2I.pop(0)
        if result is 'ID':
            self.info.SetLabel('')
            self.timer.Stop()
            self.sureButton.Enable()
            self.cancleButton.Enable()
            self.accountInput.Enable()
            self.passwordInput.Enable()
            wx.MessageBox(u'用户名不存在！', u'选课助手', style=wx.ICON_ERROR)
            return

        if result is 'PSD':
            self.info.SetLabel('')
            self.timer.Stop()
            self.sureButton.Enable()
            self.cancleButton.Enable()
            self.accountInput.Enable()
            self.passwordInput.Enable()
            wx.MessageBox(u'密码错误！', u'选课助手', style=wx.ICON_ERROR)
            return

        if result is 'times':
            self.info.SetLabel('')
            self.timer.Stop()
            self.sureButton.Enable()
            self.cancleButton.Enable()
            self.accountInput.Enable()
            self.passwordInput.Enable()
            wx.MessageBox(u'剩余次数为 0 ！', u'选课助手', style=wx.ICON_ERROR)
            return

        if result is 'net':
            self.info.SetLabel('')
            self.timer.Stop()
            self.sureButton.Enable()
            self.cancleButton.Enable()
            self.accountInput.Enable()
            self.passwordInput.Enable()
            wx.MessageBox(u'网络链接失败！', u'选课助手', style=wx.ICON_ERROR)
            return

        if isinstance(result, unicode):
            self.info.SetLabel(result.center(65))
            return

        if isinstance(result, tuple):
            gb_v.USERNUMBER = result[0]
            gb_v.TIMES = result[1]
            self.func_callBack()
            self.timer.Stop()
            self.Close()

    def sureEvent(self, event):
        gb_v.USERNAME = self.accountInput.GetValue()
        gb_v.IN_PSW = self.passwordInput.GetValue()
        self.timer.Start(200)
        self.sureButton.Disable()
        self.cancleButton.Disable()
        self.accountInput.Disable()
        self.passwordInput.Disable()
        result = Login_app(gb_v.USERNAME, gb_v.IN_PSW)

    def cancleEvent(self, event):
        self.Destroy() # 销毁隐藏Dialog

if __name__ == '__main__':
    t = time.time()
    print Login_app('NickYang', '123456')
    print time.time() - t
