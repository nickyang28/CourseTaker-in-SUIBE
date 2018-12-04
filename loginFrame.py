# coding=utf-8
import wx
import wx.lib.buttons as wxButton

from utils import load_image
import xDialog
import register


class LoginFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, style=wx.CAPTION|wx.CLOSE_BOX|wx.STAY_ON_TOP, UpdateUI=None):
        wx.Frame.__init__(self, parent, id, title=u'选课助手', size=(400, 600))
        self.CenterOnScreen()
        self.UpdateUI = UpdateUI
        self.InitUI()  # 绘制UI界面
        self.SetMaxSize((400, 600))
        self.SetMinSize((400, 600))

    def InitUI(self):
        self.icon = wx.Icon(u'Ico.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        panel = wx.Panel(self)
        self.holder = wx.BoxSizer(wx.VERTICAL)
        self.logo_sys = wx.EmptyImage(10, 10)
        imag = wx.Image(u'logo_sys.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.logo = wxButton.GenBitmapButton(panel, -1, imag,
                                             style=wx.BORDER_NONE, size=(366, 366))
        self.logo_title = wx.StaticText(panel, -1, u'欢迎使用选课助手！', pos=(120, 210))
        self.logo_title.SetForegroundColour('#0a74f7')
        self.logo_title.SetFont(wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.button_Login = wxButton.GenButton(panel, -1, u'登录', pos=(40, 270), size=(200, 40))#, style=wx.BORDER_MASK)
        self.button_Reg = wxButton.GenButton(panel, -1, u'注册', pos=(40, 270), size=(200, 40))#, style=wx.BORDER_MASK)

        self.Bind(wx.EVT_BUTTON, self.loginSys, self.button_Login)
        self.Bind(wx.EVT_BUTTON, self.Reg, self.button_Reg)

        self.holder.Add(self.logo, 0, wx.ALL | wx.CENTER, 10)
        self.holder.Add(self.logo_title, 0, wx.ALL | wx.CENTER, 10)
        self.holder.Add(self.button_Login, 0, wx.ALL | wx.CENTER, 10)
        self.holder.Add(self.button_Reg, 0, wx.ALL | wx.CENTER, 10)

        panel.SetSizer(self.holder)

    def loginSys(self, event):
        dlg = xDialog.InputDialog(self, u'登录系统', self.loginFunction)
        dlg.ShowModal()

    def loginFunction(self):
        self.UpdateUI(1)  # 更新UI-Frame

    def do_nothing(self):
        self.button_Reg.Disable()


    def Reg(self, event):
        dlg = register.register(self, u'用户注册', self.do_nothing)
        dlg.ShowModal()
