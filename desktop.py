# -*- coding: utf-8 -*-
import wx
import wx.lib.buttons as buttons
from copy import deepcopy
from function import get_safe_code, xk_assistant, get_safe_code_again
import global_variable as gb_v
import requests


class desktop(wx.Frame):
    def __init__(self, parent=None, id=-1, UpdateUI=None):
        wx.Frame.__init__(self, parent, title=u'选课助手', size=(510, 620))
        self.UpdateUI = UpdateUI
        self.CenterOnScreen()
        self.InitUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def InitUI(self):
        self.icon = wx.Icon('Ico.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.SetMaxSize((510, 620))
        self.SetMinSize((510, 620))
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimerEvent, self.timer)
        self.codes = list()

        self.panel = wx.Panel(self, size=(800, 600), pos=(0, 0))
        self.panel.SetBackgroundColour('white')
        self.holder = wx.BoxSizer(wx.VERTICAL)
        self.up_holder = wx.BoxSizer(wx.HORIZONTAL)
        self.upper = wx.StaticBox(self.panel, -1, u'登入信息')
        self.upper_sizer = wx.StaticBoxSizer(self.upper, wx.VERTICAL)
        upper_L1 = wx.BoxSizer(wx.HORIZONTAL)
        upper_L2 = wx.BoxSizer(wx.HORIZONTAL)
        upper_L3 = wx.BoxSizer(wx.HORIZONTAL)
        user_text = wx.StaticText(self.panel, -1, u'    学号：')
        psd_text = wx.StaticText(self.panel, -1, u'    密码：')
        veri_text = wx.StaticText(self.panel, -1, u'验证码：')
        number = wx.TextCtrl(self.panel, -1, gb_v.USERNUMBER, size=(150, 22), style=wx.TE_READONLY)
        self.password = wx.TextCtrl(self.panel, -1, '', size=(150, 22), style=wx.TE_PASSWORD)
        self.vcode = wx.TextCtrl(self.panel, -1, '', size=(150, 22))
        imag = wx.Image('test.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.vcode_button = buttons.GenBitmapButton(self.panel, -1, imag,
                                                    style=wx.BORDER_NONE, size=(68, 22))
        self.Bind(wx.EVT_BUTTON, self.refresh_safecode, self.vcode_button)

        upper_L1.Add(user_text, 0, wx.ALL | wx.CENTER, 10)
        upper_L1.Add(number, 0, wx.ALL | wx.CENTER, 10)
        upper_L2.Add(psd_text, 0, wx.ALL | wx.CENTER, 10)
        upper_L2.Add(self.password, 0, wx.ALL | wx.CENTER, 10)
        upper_L3.Add(veri_text, 0, wx.ALL | wx.CENTER, 10)
        upper_L3.Add(self.vcode, 0, wx.ALL | wx.CENTER, 10)
        upper_L3.Add(self.vcode_button, 0, wx.ALL | wx.CENTER, 10)
        self.upper_sizer.Add(upper_L1, 0, wx.ALL | wx.LEFT, 0)
        self.upper_sizer.Add(upper_L2, 0, wx.ALL | wx.LEFT, 0)
        self.upper_sizer.Add(upper_L3, 0, wx.ALL | wx.LEFT, 0)

        self._button_xk = buttons.GenButton(self.panel, -1, u'开始选课', size=(130, 130), pos=(350, 18))
        self.up_holder.Add(self.upper_sizer, 0, wx.ALL | wx.CENTER, 10)
        self.up_holder.Add(self._button_xk, 0, wx.ALL | wx.CENTER, 10)
        self.Bind(wx.EVT_BUTTON, self.confirm, self._button_xk)

        self.lower = wx.StaticBox(self.panel, -1, u'课程信息')
        self.lower_sizer = wx.StaticBoxSizer(self.lower, wx.VERTICAL)

        lower_L1 = wx.BoxSizer(wx.HORIZONTAL)
        self.code_input = wx.TextCtrl(self.panel, -1, size=(150, 20), pos=(100, 250), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.add, None)
        self._button_add = buttons.GenButton(self.panel, -1, u'添加', pos=(220, 250), size=(75, 20))
        self._button_delete = buttons.GenButton(self.panel, -1, u'删除', pos=(300, 250), size=(75, 20))
        self.Bind(wx.EVT_BUTTON, self.add, self._button_add)
        self.Bind(wx.EVT_BUTTON, self.delete, self._button_delete)
        lower_L1.Add(self.code_input, 0, wx.ALL | wx.CENTER, 10)
        lower_L1.Add(self._button_add, 0, wx.ALL | wx.CENTER, 10)
        lower_L1.Add(self._button_delete, 0, wx.ALL | wx.CENTER, 10)

        self.codes_list = wx.ListCtrl(self.panel, -1, size=(455, 260), pos=(20, 300),
                                      style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES | wx.BORDER_SUNKEN)
        self.codes_list.InsertColumn(0, u'选课序号')
        self.codes_list.InsertColumn(1, u'状态')
        self.codes_list.SetColumnWidth(0, 150)
        self.codes_list.SetColumnWidth(1, 300)
        self.lower_sizer.Add(lower_L1, 0, wx.ALL | wx.CENTER, 5)
        self.lower_sizer.Add(self.codes_list, 0, wx.ALL | wx.CENTER, 5)

        copyright_ = wx.StaticText(self.panel, -1, u'Copyright (c) 2018 Nick Yang. All rights reserve.',
                                   pos=(120, 565))
        self.times_ = wx.StaticText(self.panel, -1, u'剩余选课次数：' + str(gb_v.TIMES) + u'次',
                               pos=(120, 565))
        self.holder.Add(self.up_holder, 0, wx.ALL | wx.LEFT, 10)
        self.holder.Add(self.lower_sizer, 0, wx.ALL | wx.CENTER, 0)
        self.holder.Add(copyright_, 0, wx.ALL | wx.CENTER, 0)
        self.holder.Add(self.times_, 0, wx.ALL | wx.CENTER, 0)
        self.panel.SetSizer(self.holder)

    def OnTimerEvent(self, evt):
        if not gb_v.TUNNEL_F2D:
            return
        result = gb_v.TUNNEL_F2D.pop(0)
        if result is False:
            wx.MessageBox(u'登陆失败：密码或验证码错误， 请刷新验证码后重试。', u'选课助手', style=wx.ICON_ERROR)
            self.password.Enable()
            self.vcode.Enable()
            self.timer.Stop()
            return

        if result is None:
            e = requests.post('https://nickyang.info/count?username=' + gb_v.USERNAME)
            gb_v.TIMES -= 1
            self.times_.SetLabel(u'剩余选课次数：' + str(gb_v.TIMES) + u'次')
            wx.MessageBox(u'选课完毕， 谢谢使用！')
            self.timer.Stop()
            return
        pos = self.codes.index(result.num)
        self.codes_list.SetStringItem(pos, 1, result.status)

        if u'选课成功' in result.status:
            self.codes_list.SetItemBackgroundColour(pos, "#cde6c7")
        elif u'请检查选课序号！' in result.status:
            self.codes_list.SetItemBackgroundColour(pos, "#f7acbc")
        else:
            self.codes_list.SetItemBackgroundColour(pos, "#fcf16e")

    def confirm(self, evt):
        if not self.codes:
            wx.MessageBox(u'请至少输入一个选课序号。', u'选课助手', style=wx.ICON_ERROR)
            return
        gb_v.PASSWORD = self.password.GetValue()
        gb_v.VERIFYCODE = self.vcode.GetValue()

        self.password.Disable()
        self.vcode.Disable()
        self._button_xk.Disable()
        self.code_input.Disable()
        self._button_add.Disable()
        self._button_delete.Disable()

        self.timer.Start(50)
        xk_assistant(deepcopy(self.codes))

    def add(self, evt):
        code = self.code_input.GetValue().strip()
        if code != '':
            self.codes.append(code)
            self.code_input.Clear()
            pos = len(self.codes) - 1
            self.codes_list.InsertStringItem(pos, code)
            self.codes_list.SetStringItem(pos, 1, u'就绪...')

    def delete(self, evt):
        if len(self.codes) == 0:
            return
        self.codes_list.DeleteItem(len(self.codes) - 1)
        self.codes.remove(self.codes[-1])

    def refresh_safecode(self, evt):
        if not get_safe_code_again():
            wx.MessageBox(u'无法获取到验证码, 请检查网络。')
            return False
        self._button_xk.Enable()
        imag = wx.Image('test.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.vcode_button.SetBitmapLabel(imag)

    def OnClose(self, evt):

        self.Close()
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        gb_v.USERNUMBER = '17068028'
        if not get_safe_code():
            wx.MessageBox(u'无法获取到验证码, 请检查网络。')
        self.frame = desktop(parent=None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


'''
454.001.201 满 
596.001.203 可选
403.006.201 已选
123.456.789 无
'''

if __name__ == '__main__':
    app = App()
    app.MainLoop()
