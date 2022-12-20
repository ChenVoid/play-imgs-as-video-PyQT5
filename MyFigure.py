# -*- coding: utf-8 -*-
"""
@Software: PyCharm
@File    :  MyFigure.py
@Time    : 2022/4/21 17:30
@Author  :  Void
"""
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MyFigure(FigureCanvas):
    def __init__(self, ImgPath):
        # 插入背景图片
        # self.ImgPath = r"D:\Projects\PycharmProjects\Matplotlib-demo\pic\11.jpg"
        self.img = plt.imread(ImgPath)
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.imshow(self.img)
        # self.fig, self.axes = plt.subplots()
        # self.axes.imshow(self.img, extent=[0, 571, 0, 361])
        # self.axes.imshow(self.img)
        print(ImgPath)

        # 此句必不可少，否则不能显示图形
        super(MyFigure, self).__init__(self.fig)
        # plt.close(self.fig)

    def upgrade_imgs(self, ImgPath):
        # self.fig = None
        # self.axes = None
        # self.fig.clf()
        # draw_final()
        self.img = plt.imread(ImgPath)
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111)
        # self.fig, self.axes = plt.subplots()
        self.axes.imshow(self.img)
        super(MyFigure, self).__init__(self.fig)
        print(ImgPath)