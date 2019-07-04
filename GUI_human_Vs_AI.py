from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.font as tkFont
from Record_and_GameTree import StepRecordChessBoard
from PIL import Image, ImageTk


class CheckerBoardView(tk.Tk, object):
    # 这个类中包含了显示棋盘和棋子的方法
    def __init__(self):
        super(CheckerBoardView, self).__init__()
        # 一些状态属性
        self.gameStart = False
        self.allphoto = []
        self.count = 0

        # 调试用
        self.i = 0
        self.j = 0

        # 人机对战模式
        self.humanVsAI = True  # 人机只会用白子
        # 初始化棋盘状态
        self.step_record_chess_board = StepRecordChessBoard(1)

        # 绘制棋盘
        self.build_board()

    def endgame_result(self):
        self.gameStart = False
        # 游戏结束响应，设置为两种选择，退出游戏和重新开始

    def regret_piece(self):
        """
        悔棋函数
        前提：当且仅当玩家在决策时可使用悔棋函数，悔棋需要删除：
                list1的最后一个元素
                list2的最后一个元素
                list3的最后两个元素
                record记录中对应的两个元素
                self.allphoto中的最后两个元素
                self.count倒退两步
        :return: 
        """
        # list1的最后一个元素
        # list2的最后一个元素
        # list3的最后两个元素
        print('111111111111111111111')
        position_b = self.step_record_chess_board.list1.pop()
        position_w = self.step_record_chess_board.list2.pop()
        self.step_record_chess_board.list3.pop()
        # 删除record记录中对应的两个元素
        self.step_record_chess_board.records[position_b[0]][position_b[1]] = None
        self.step_record_chess_board.records[position_w[0]][position_w[1]] = None
        # self.allphoto中的最后两个元素
        self.board.delete(self.allphoto.pop())
        self.board.delete(self.allphoto.pop())
        # self.count倒退两步
        self.count -= 2

    def build_board(self):


        def buttonCallBack():
            # 开始游戏
            # 初始化棋盘图形对象
            self.gameStart = True
            if len(self.allphoto) > 0:

                for i in self.allphoto:
                    self.board.delete(i)
            # 按钮消失
            start_str.place_forget()
            self.allphoto.clear()

        def quitCallBack():
            # 退出游戏
            exit(0)

        # 让可用图形窗口置顶
        # self.geometry('700x900')
        self.title("五子棋--人机对战模式")
        self.resizable(width=False, height=False)
        self.board = Canvas(self.master, bg="#FFFFF0", width=630, height=650)

        # 创建棋盘划线
        for c in range(40, 610, 30):
            x0, y0, x1, y1 = c, 40, c, 580
            self.board.create_line(x0, y0, x1, y1)
        for r in range(40, 610, 30):
            x0, y0, x1, y1 = 40, r, 580, r
            self.board.create_line(x0, y0, x1, y1)

        # 创建棋盘中的辅助数字标签，标定棋盘中线的位置序号1-19
        x0 = 30
        y0 = 5
        for i in range(1, 20):
            tk.Label(self.board, text=i, bg="#FFFFF0").place(x=x0, y=y0)
            x0 += 30
        x0 = 5
        y0 = 30
        for i in range(1, 20):
            tk.Label(self.board, text=i, bg="#FFFFF0").place(x=x0, y=y0)
            y0 += 30

        # 棋盘上功能按钮
        # 开始游戏按钮
        font1 = tkFont.Font(family='微软雅黑', size=10, weight=tkFont.BOLD)
        start_str = Button(self.board, text="开始游戏", bg="white", activebackground="Gray", font=font1,
                           command=buttonCallBack)
        start_str.place(x=315, y=300, anchor='center')

        # 退出游戏按钮
        # img_open = Image.open('img_png.png')
        # img_png = ImageTk.PhotoImage(img_open)
        font2 = tkFont.Font(family='微软雅黑', size=12, weight=tkFont.BOLD)
        quit_str = Button(self.board, text="退出游戏", bg="white", activebackground="Gray", font=font2,
                          command=quitCallBack)
        quit_str.place(x=500, y=610, anchor='center')

        # 悔棋按钮
        regret_str = Button(self.board, text='悔棋', bg="white", activebackground="Gray", font=font2,
                            command=self.regret_piece)
        regret_str.place(x=300, y=610, anchor='center')

        # 禁手
        forbid_str = Button(self.board, text='禁手', bg="white", activebackground="Gray", font=font2,
                            command=quitCallBack)
        forbid_str.place(x=100, y=610, anchor='center')

        # 建立事件响应
        self.board.bind("<Button-1>", self.human)
        self.board.bind("<ButtonRelease-1>", self.AI)
        self.board.pack()

    def AI(self, event):
        if self.gameStart:
            print('电脑下棋中，鼠标缴掉')
            if self.count % 2 == 1:

                pos = self.step_record_chess_board.policy_decision()
                # 调试用
                #pos = [self.i, self.j]
                #self.i += 1
                #self.j += 1

                self.step_record_chess_board.insert_record(pos[0], pos[1])  # 在棋盘中插入该棋子
                self.step_record_chess_board.insert_position_list(0, pos)

                # 棋盘坐标转换
                y = pos[1] * 30 + 40
                x = pos[0] * 30 + 40
                self.allphoto.append(self.board.create_oval(x - 14, y - 14, x + 14, y + 14, fill="White"))

                result = self.step_record_chess_board.check_victory()  # 判断是否胜利
                if result == 0:
                    # 结束情况选择：1、继续游戏 2、退出游戏
                    # tk.messagebox.showinfo('提示', 'AI获胜！').place(240, 550)
                    ask_result = tk.messagebox.askyesno(title='提示', message='AI胜利！\n再来一盘？')
                    if ask_result:
                        self.destroy()
                    else:
                        exit(0)

                else:
                    pass
                self.count += 1

    def human(self, event):
        # 读取鼠标坐标，event_x为横坐标，event_y为纵坐标
        if self.gameStart:
            mouse_x = event.x
            mouse_y = event.y
            if 590 > mouse_x > 30 and 590 > mouse_y > 30:
                # 由鼠标坐标计算并四舍五入出实际的位置坐标（1,1）-（19,19）
                # 为方便计算设为（0,0）-（18,18）
                position_x = round((mouse_x - 40) / 30)
                position_y = round((mouse_y - 40) / 30)
                # 将二维位置坐标转化为一维动作，方便之后使用，总共有19*19种动作情况
                # 即对应动作值action范围为0-360
                action = position_x + 19 * position_y

                # 棋盘坐标转换
                y = (action // 19) * 30 + 40
                x = (action % 19) * 30 + 40

                if self.step_record_chess_board.has_record(position_x, position_y) == 0:
                    self.step_record_chess_board.insert_record(position_x, position_y)  # 在棋盘中插入该棋子
                    self.step_record_chess_board.insert_position_list(1, (position_x, position_y))
                    self.allphoto.append(self.board.create_oval(x - 14, y - 14, x + 14, y + 14, fill="Black"))
                    # self.board.delete(self.allphoto.pop())
                    self.count += 1

                result = self.step_record_chess_board.check_victory()  # 判断是否胜利

                if result == 1:
                    # 解除鼠标左键绑定
                    self.unbind('<Button-1>')
                    # tk.messagebox.showinfo('提示', '黑棋获胜！').place(240, 550)
                    ask_result = tk.messagebox.askyesno(title='提示', message='玩家胜利！\n再来一盘？')
                    if ask_result:
                        self.destroy()
                    else:
                        exit(0)

                else:
                    pass

    def AI_vs_human(self, event):
        if self.gameStart:
            print('11111111111111111111111')
            if self.count % 2 == 1:
                pos = self.step_record_chess_board.policy_decision()
                if pos in self.step_record_chess_board.list3:
                    message = tk.Text( "不可用的位置" + str(pos[0]) + "," + str(pos[1])).place(200, 200)
                    message.pack()
                self.step_record_chess_board.insert_record(pos[0], pos[1])  # 在棋盘中插入该棋子
                self.step_record_chess_board.insert_position_list(0, (pos[0], pos[1]))

                # 棋盘坐标转换
                y = pos[1] * 30 + 40
                x = pos[0] * 30 + 40
                self.board.create_oval(x - 14, y - 14, x + 14, y + 14, fill="White")

                result = self.step_record_chess_board.check_victory()  # 判断是否胜利
                if result == 0:
                    tk.messagebox.showinfo('提示', 'AI获胜！').place(240, 550)
                    self.endgame_result()

                else:
                    pass
                self.count += 1

            else:
                # 读取鼠标坐标，event_x为横坐标，event_y为纵坐标
                mouse_x = event.x
                mouse_y = event.y
                if 590 > mouse_x > 30 and 590 > mouse_y > 30:
                    # 由鼠标坐标计算并四舍五入出实际的位置坐标（1,1）-（19,19）
                    # 为方便计算设为（0,0）-（18,18）
                    position_x = round((mouse_x - 40) / 30)
                    position_y = round((mouse_y - 40) / 30)
                    # 将二维位置坐标转化为一维动作，方便之后使用，总共有19*19种动作情况
                    # 即对应动作值action范围为0-360
                    action = position_x + 19 * position_y

                    # 棋盘坐标转换
                    y = (action // 19) * 30 + 40
                    x = (action % 19) * 30 + 40

                    if self.step_record_chess_board.has_record(position_x, position_y) == 0:
                        self.step_record_chess_board.insert_record(position_x, position_y)  # 在棋盘中插入该棋子
                        self.step_record_chess_board.insert_position_list(1, (position_x, position_y))
                        self.board.create_oval(x - 14, y - 14, x + 14, y + 14, fill="Black")

                    result = self.step_record_chess_board.check_victory()  # 判断是否胜利

                    if result == 1:
                        # 解除鼠标左键绑定
                        self.unbind('<Button-1>')
                        tk.messagebox.showinfo('提示', '黑棋获胜！').place(240, 550)
                        self.endgame_result()

                    else:
                        pass

                    self.count += 1

    def render(self):
        self.update()

# 调试用
def main():
    while 1:
        view = CheckerBoardView()
        view.mainloop()

if __name__ == "__main__":
    main()