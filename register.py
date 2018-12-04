# -*- coding: utf-8 -*-
import wx
import wx.lib.buttons as buttons
import global_variable as gb_v
import json
import requests


class register(wx.Dialog):
    def __init__(self, parent, title, func_callBack):
        wx.Dialog.__init__(self, parent, title=title, size=(300, 200))
        self.CenterOnScreen()
        self.InitUI()
        # self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.func_callBack = func_callBack

    def InitUI(self):
        self.icon = wx.Icon('Ico.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.SetMaxSize((300, 200))
        self.SetMinSize((300, 200))

        self.panel = wx.Panel(self, size=(300, 200), pos=(0, 0))
        self.panel.SetBackgroundColour('white')
        self.holder = wx.BoxSizer(wx.VERTICAL)

        upper_L1 = wx.BoxSizer(wx.HORIZONTAL)

        user_text = wx.StaticText(self.panel, -1, u'登陆名称：')
        self.user = wx.TextCtrl(self.panel, -1, '', size=(150, 22), style=wx.TE_PROCESS_ENTER)

        upper_L1.Add(user_text, 0, wx.ALL | wx.CENTER, 10)
        upper_L1.Add(self.user, 0, wx.ALL | wx.CENTER, 10)

        lower_L1 = wx.BoxSizer(wx.HORIZONTAL)
        lower_L2 = wx.BoxSizer(wx.HORIZONTAL)

        student_id = wx.StaticText(self.panel, -1, u'绑定学号：')
        psd_text = wx.StaticText(self.panel, -1, u'账户密码：')
        self.number = wx.TextCtrl(self.panel, -1, gb_v.USERNUMBER, size=(150, 22), style=wx.TE_PROCESS_ENTER)
        self.in_psw = wx.TextCtrl(self.panel, -1, gb_v.IN_PSW, size=(150, 22), style=wx.TE_PROCESS_ENTER)
        lower_L1.Add(student_id, 0, wx.ALL | wx.CENTER, 10)
        lower_L1.Add(self.number, 0, wx.ALL | wx.CENTER, 10)
        lower_L2.Add(psd_text, 0, wx.ALL | wx.CENTER, 10)
        lower_L2.Add(self.in_psw, 0, wx.ALL | wx.CENTER, 10)
        self._button_zc = buttons.GenButton(self.panel, -1, u'注册', size=(150, 30))
        self.Bind(wx.EVT_BUTTON, self.register, self._button_zc)
        self.Bind(wx.EVT_TEXT_ENTER, self.register, None)

        self.holder.Add(upper_L1, 0, wx.ALL | wx.CENTER, 0)
        self.holder.Add(lower_L1, 0, wx.ALL | wx.CENTER, 0)
        self.holder.Add(lower_L2, 0, wx.ALL | wx.CENTER, 0)
        self.holder.Add(self._button_zc, 0, wx.ALL | wx.CENTER, 0)

        self.panel.SetSizer(self.holder)

    def register(self, evt):
        username = self.user.GetValue()
        in_psw = self.in_psw.GetValue()
        number = self.number.GetValue()
        if username == '':
            wx.MessageBox(u'用户名不能为空！', u'用户注册', style=wx.ICON_ERROR)
            return False
        if in_psw == '':
            wx.MessageBox(u'密码不能为空！', u'用户注册', style=wx.ICON_ERROR)
            return False
        if number == '':
            wx.MessageBox(u'绑定学号不能为空！', u'用户注册', style=wx.ICON_ERROR)
            return False
        try:
            r = requests.post(
                'https://nickyang.info/register?username=' + username + '&password=' + in_psw + '&number=' + number)
        except:
            wx.MessageBox(u'网络错误！', u'用户注册', style=wx.ICON_ERROR)
            return False
        if u'重复用户名' in r.text:
            wx.MessageBox(u'用户名存在！', u'用户注册', style=wx.ICON_ERROR)
            return False
        if u'重复学号' in r.text:
            wx.MessageBox(u'此学号已经被绑定！', u'用户注册', style=wx.ICON_ERROR)
            return False
        wx.MessageBox(u'注册成功！', u'用户注册')
        self.func_callBack()
        self.Close()
        return True

    def OnClose(self, evt):
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        self.frame = register(parent=None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()
