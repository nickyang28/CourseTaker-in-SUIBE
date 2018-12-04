# -*- coding:utf-8 -*-
import loginFrame
import desktop


class GuiManager():
    def __init__(self, UpdateUI, app):
        self.UpdateUI = UpdateUI
        self.app = app
        self.frameDict = {}  # 用来装载已经创建的Frame对象

    def GetFrame(self, type):
        frame = self.frameDict.get(type)
        if frame is None:
            frame = self.CreateFrame(type)
            self.frameDict[type] = frame
        return frame

    def CreateFrame(self, type):
        if type == 0:
            return loginFrame.LoginFrame(parent=None, id=-1, UpdateUI=self.UpdateUI)
        elif type == 1:
            return desktop.desktop(parent=None, id=-1, UpdateUI=self.UpdateUI)
