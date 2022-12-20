# -*- coding: utf-8 -*-
"""
@Software: PyCharm
@File    :  PlayImg.py
@Time    : 2022/4/18 13:16
@Author  :  Void
"""
import os
import threading
import time

import cv2

import PyQt5
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QGraphicsPixmapItem, QGraphicsScene, QApplication, QGridLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from MyFigure import MyFigure
from UI.PlayImg_ui import Ui_MainWindow


class PlayImg(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PlayImg, self).__init__(parent)
        self.setupUi(self)

        self.btn_open.clicked.connect(self.open_imgs)
        self.btn_play.clicked.connect(self.play)
        # self.btn_stop.clicked.connect(self.stop)
        self.btn_jump.clicked.connect(self.jump)
        self.btn_ApplyFPS.clicked.connect(self.apply_fps)

        self.PlayFps = 0
        self.PlayTime = 0
        self.ImgWidth = 0
        self.ImgLength = 0
        self.ImgList = []
        self.ImgBasePath = ""
        self.IsImportImgs = 0
        self.ImgPath = ""
        self.ImgIndex = 0

        self.item = 0
        self.scene = 0
        self.size = (0, 0)

        self.IsPause = 1

        self.gridlayout = None
        self.F = None

    def open_imgs(self):
        try:
            self.IsPause = 1
            self.btn_play.setText("播放")
            self.ImgIndex = 0
            self.ImgBasePath = self.lineEdit_path.text()
            self.ImgList = os.listdir(self.ImgBasePath)
            print(self.ImgList)
            # 使用相对路径
            self.ImgPath = self.ImgBasePath + '/' + self.ImgList[self.ImgIndex]
            self.PlayFps = int(self.lineEdit_fps.text())
            self.PlayTime = 1 / self.PlayFps

            # 在Qt上显示self.F
            self.F = MyFigure(ImgPath=self.ImgPath)
            self.gridlayout = QGridLayout(self.label_img)
            self.gridlayout.addWidget(self.F)
            # 适应窗口大小
            # showImage = QPixmap(self.ImgPath).scaled(self.label_img.width(), self.label_img.height())
            # self.label_img.setPixmap(showImage)

            QMessageBox.information(self, "Success!", "图片已导入，请点击“播放”开始播放图片！")
            self.label_ImgName.setText(self.ImgList[self.ImgIndex])
            self.qid.setText(str(self.ImgIndex) + "/" + str(len(self.ImgList)))
            self.IsImportImgs = 1

        except Exception as e:
            print(e)
            QMessageBox.information(self, "Error!", "未找到图片，或图片路径错误！")

    def play(self):
        if self.IsImportImgs == 1:
            if self.IsPause == 1:
                self.IsPause = 0
                # self.update_img()
                update_img_thread = threading.Thread(target=self.update_img).start()
                self.btn_play.setText("暂停")
            else:
                self.IsPause = 1
                self.btn_play.setText("播放")
        else:
            QMessageBox.information(self, "Error!", "您还未导入图片！")

    # def stop(self):
    #     if self.IsImportImgs == 1:
    #         self.IsPause = 1
    #
    #     else:
    #         QMessageBox.information(self, "Error!", "您还未导入图片！")

    def update_img(self):
        while self.ImgIndex < len(self.ImgList) and self.IsPause == 0:
            self.ImgPath = self.ImgBasePath + '/' + self.ImgList[self.ImgIndex]
            # print(self.ImgPath)

            # 更新图片
            # self.F.fig.clf()
            self.F = MyFigure(ImgPath=self.ImgPath)
            print(self.F)

            self.gridlayout = None
            self.gridlayout = QGridLayout(self.label_img)
            self.gridlayout.addWidget(self.F)
            # print(self.gridlayout)
            # F_update_imgs_thread = threading.Thread(target=self.F.upgrade_imgs, args=(self.ImgPath,)).start()
            # self.F.upgrade_imgs(self.ImgPath)
            # # self.F = MyFigure(ImgPath=self.ImgPath)
            # # self.gridlayout = None
            # self.gridlayout = QGridLayout(self.label_img)
            # self.gridlayout.addWidget(self.F)

            # showImage = QPixmap(self.ImgPath).scaled(self.label_img.width(), self.label_img.height())  # 适应窗口大小
            # self.label_img.setPixmap(showImage)

            # img = cv2.imread(self.ImgPath)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # img = cv2.resize(img, self.size, interpolation=cv2.INTER_CUBIC)
            # frame = QImage(img, self.ImgWidth, self.ImgLength, QImage.Format_RGB888)
            # pix = QPixmap.fromImage(frame)
            # self.label_img.setPixmap(pix)

            self.label_ImgName.setText(self.ImgList[self.ImgIndex])
            self.qid.setText(str(self.ImgIndex + 1) + "/" + str(len(self.ImgList)))
            self.ImgIndex += 1
            time.sleep(self.PlayTime)  # 设置图片显示间隔时间
            # QApplication.processEvents()

    def jump(self):
        if self.IsImportImgs == 1:
            self.IsPause = 1
            self.btn_play.setText("播放")
            JumpIndex = int(self.lineEdit_jump.text())
            if 0 < JumpIndex <= len(self.ImgList):
                self.ImgIndex = JumpIndex - 1
                self.ImgPath = self.ImgBasePath + '/' + self.ImgList[self.ImgIndex]
                showImage = QPixmap(self.ImgPath).scaled(self.label_img.width(), self.label_img.height())  # 适应窗口大小
                self.label_img.setPixmap(showImage)
                self.label_ImgName.setText(self.ImgList[self.ImgIndex])
                self.qid.setText(str(self.ImgIndex + 1) + "/" + str(len(self.ImgList)))

            else:
                QMessageBox.information(self, "Error!", "无效的跳转")
        else:
            QMessageBox.information(self, "Error!", "您还未导入图片！")

    def apply_fps(self):
        try:
            self.PlayFps = int(self.lineEdit_fps.text())
            self.PlayTime = 1 / self.PlayFps
        except:
            QMessageBox.information(self, "Error!", "无效的帧率！")
