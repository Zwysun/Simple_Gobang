"""
Name: MiddleWare_Aimo
Author: Zwy
"""


from player.animo.alpha_beta_ai import Gomoku
import random
import numpy as np

class Animo():
    def __init__(self, table, search_depth = 3):
        self.playerjudger = None
        self.table_2d = None
        self.color = None
        self.anticolor = None

        self.search_depth = search_depth

        self.color_dict = {'White': 1, 'Black': -1, 'Blank': 0}
        self.my_color_dict = {'White': 2, 'Black': 1, 'Blank': 0}
        self.t1 = None
        # AI
        self.ai = None

    def update_table_info(self):
        for i in range(len(self.table_2d)):
            for j in range(len(self.table_2d[0])):
                # 白棋
                if self.table_2d[i][j] == 1:
                    self.ai.g_map[i][j] = 2
                # 黑棋
                elif self.table_2d[i][j] == -1:
                    self.ai.g_map[i][j] = 1
        return

    def xiazi(self, playerjudger, color, step):
        # if step == 0:

        self.playerjudger = playerjudger
        self.color = color
        self.table_2d = playerjudger.table_2d[1:16, 1:16]

        self.ai = Gomoku(self.search_depth)
        self.update_table_info()
            

        is_player_first = (self.color == 'White')
        self.ai.cur_step = step
        # print(is_player_first)
        try:
            machine_pos = self.ai.ai_play_1step(is_player_first)
        except Exception as e:
            print(e)

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
            self.playerjudger.table_2d[machine_pos[0]+1][machine_pos[1]+1] = -1
            if (not self.playerjudger.check_forbidden((machine_pos[1]+1, machine_pos[0]+1), self.color, False)):
                print('forbidden')
                self.ai.g_map[machine_pos[0]][machine_pos[1]] = 1
                new_machine_pos = self.ai.ai_play_1step(is_player_first)
                self.ai.g_map[machine_pos[0]][machine_pos[1]] = 0
                machine_pos = new_machine_pos

            self.playerjudger.table_2d[machine_pos[0] + 1][machine_pos[1] + 1] = 0
            # print('Animo!', machine_pos)

        return machine_pos[0]+1, machine_pos[1]+1

