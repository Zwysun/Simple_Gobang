# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDialog
from UI_game_begin import Ui_gamebegin
import GUI_human_Vs_AI  #import CheckerBoardView
import GUI_human


class MyMain(QDialog, Ui_gamebegin):

    def __init__(self):
        super(MyMain, self).__init__()
        self.setupUi(self)

        self.AI.clicked.connect(self.begin_ai)
        self.human.clicked.connect(self.begin_human)

    # 启动人机对战
    def begin_ai(self):
        vs_ai = GUI_human_Vs_AI.CheckerBoardView()
        self.accept()    # 隐藏启动界面
        vs_ai.mainloop()
        
    # 启动局域网对战
    def begin_human(self):
        vs_human = GUI_human.CheckerBoardView()
        self.accept()
        vs_human.mainloop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    begin = MyMain()
    begin.show()
    sys.exit(app.exec_())