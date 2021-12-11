from player.animo2.GomokuAI_animo import get_next_pos
import player.animo2.Global as Global
import random
import numpy as np
import logic.judge as jd
import draw.table as tb

class Animo():
    def __init__(self, table):
        self.playerjudger = None
        self.table_2d = None
        self.color = None
        self.anticolor = None

        self.color_dict = {'White': 1, 'Black': -1, 'Blank': 0}
        self.t1 = None
        # AI

    def update_table_info(self):
        for i in range(len(self.table_2d)):
            for j in range(len(self.table_2d[0])):
                if self.table_2d[i][j] == 1:
                    Global.flag[i][j] = 1
                    Global.white[i][j] = 1
                elif self.table_2d[i][j] == -1:
                    Global.flag[i][j] = 1
                    Global.black[i][j] = 1
        return

    def xiazi(self, playerjudger, color, step):
        # if step == 0:

        self.playerjudger = playerjudger
        self.color = color
        self.table_2d = np.transpose(playerjudger.table_2d[1:16, 1:16])
        self.update_table_info()

        if self.color == 'Black':
            is_neg = False
        else:
            is_neg = True

        if step != 0:
            machine_pos = get_next_pos(is_neg)
        else:
            machine_pos = [random.randint(6, 9), random.randint(6, 9)]

        if not machine_pos:
            valid_index = [(i, j) for i in range(len(self.table_2d)) for j in range(len(self.table_2d[0])) if
                           self.table_2d[i][j] == 0]
            if len(valid_index) == 0:
                print('No Valid Pos!!!')
                return
            random_index = random.randint(0, len(valid_index))
            machine_pos = valid_index[random_index]
        # print(self.color)
        if self.color == 'Black':
            # # config and initialization
            # table_row = 16  # 1 ~ 15 is valid
            # table_col = 16  # 0 , 16 is invalid
            # grid_size = 40
            #
            # tmp_table = tb.Table(table_row=table_row, table_col=table_col, grid_size=grid_size)
            # tmp_table.table_2d[machine_pos[0]+1][machine_pos[1]+1] = -1
            # tmp_judger = jd.Judge(tmp_table)
            self.playerjudger.table_2d[machine_pos[1]+1][machine_pos[0]+1] = -1
            if (not self.playerjudger.check_forbidden((machine_pos[0]+1, machine_pos[1]+1), self.color, False)):
                print('forbidden')
                Global.flag[machine_pos[0]][machine_pos[1]] = 1
                new_machine_pos = get_next_pos(is_neg)
                Global.flag[machine_pos[0]][machine_pos[1]] = 0
                machine_pos = new_machine_pos
            self.playerjudger.table_2d[machine_pos[1] + 1][machine_pos[0] + 1] = 0

            print('Animo!', machine_pos)
        return machine_pos[1]+1, machine_pos[0]+1
