# -*- coding: utf-8 -*-
"""
Name: Greedy_AI
Author: Zwy
"""

from player.animo.cal_score import cal_score
from player.animo.cal_score import Global
import copy

class Gomoku2():
	def __init__(self):
		pass

	def ai_play_1step(self, mod):
		global search_range, best_pos
		search_range = self.shrink_range()
		try:
			if not mod:
				best_pos = self.greedy_thinking_twice(mod)
			else:
				best_pos = self.greedy_thinking(mod)
		except Exception as e:
			print(e)
			return False
		return best_pos

	# 寻找'半径'为1的闭包
	def shrink_range(self):
		cover_range = [[0 for i in range(15)] for j in range(15)]
		for i in range(15):
			for j in range(15):
				if Global.flag[i][j] == 1:
					for k in range(3):
						cover_range[max(0, i - 1)][min(14, j - 1 + k)] = 1
						cover_range[max(0, i)][min(14, j - 1 + k)] = 1
						cover_range[min(14, i + 1)][min(14, j - 1 + k)] = 1
		cnt = 0
		for i in range(15):
			for j in range(15):
				if Global.flag[i][j] == 1:
					cover_range[i][j] = 0
				if cover_range[i][j] == 1:
					cnt += 1
		# print 'cover_range_size：%d' % cnt
		return cover_range

	# 用贪心思想再权衡各参数
	def greedy_thinking(self, is_neg):
		global search_range
		black_max_score = -5
		white_max_score = -5
		w_best_pos = ''
		b_best_pos = ''
		for i in range(15):
			for j in range(15):
				if Global.flag[i][j] == 0 and search_range[i][j] == 1:
					Global.flag[i][j] = 1
					search_range[i][j] = 0
					Global.white[i][j] = 1
					white_score = cal_score('white', i, j)

					Global.white[i][j] = 0
					Global.black[i][j] = 1
					black_score = cal_score('black', i, j)

					Global.black[i][j] = 0
					Global.flag[i][j] = 0
					if black_score > black_max_score:
						black_max_score = black_score
						b_best_pos = (i, j)
					if white_score > white_max_score:
						white_max_score = white_score
						w_best_pos = (i, j)
		# 防守型
		if is_neg and white_max_score >= 10000 and black_max_score <= white_max_score:
			return w_best_pos
		if is_neg and black_max_score >= 1000:
			return b_best_pos
		if white_max_score > black_max_score or white_max_score >= 100000:
			return w_best_pos
		else:
			return b_best_pos


	# 进攻性尝试
	def greedy_thinking_twice(self, is_neg):
		global search_range
		black_max_score = -5
		white_max_score = -5
		w_best_pos = ''
		b_best_pos = ''
		for i in range(15):
			for j in range(15):
				if Global.flag[i][j] == 0 and search_range[i][j] == 1:
					Global.flag[i][j] = 1
					search_range[i][j] = 0
					Global.white[i][j] = 1
					white_score = cal_score('white', i, j)
					Global.white[i][j] = 0
					Global.black[i][j] = 1

					black_score = cal_score('black', i, j)
					Global.black[i][j] = 0
					Global.flag[i][j] = 0
					if black_score > black_max_score:
						black_max_score = black_score
						b_best_pos = (i, j)
						# print black_max_score
						# print b_best_pos
					if white_score > white_max_score:
						white_max_score = white_score
						w_best_pos = (i, j)
						# print white_max_score
						# print w_best_pos
		if white_max_score >= 100000:
			return w_best_pos
		if black_max_score >= 8000:
			return b_best_pos
		if white_max_score > black_max_score:
			first_best = w_best_pos
			second_best = b_best_pos
		else:
			first_best = b_best_pos
			second_best = w_best_pos
		first_sums, first_best = self.twice_search(first_best, second_best, is_neg)
		second_sums, second_best = self.twice_search(second_best, first_best, is_neg)
		if first_sums < second_sums:
			first_best = second_best
		# print(first_sums, second_sums)
		return first_best


	def twice_search(self, first_best, second_best, is_neg):
		global search_range
		(w_11, w_12) = first_best
		one_score = cal_score('white', w_11, w_12)
		Global.white[w_11][w_12] = 1
		Global.flag[w_11][w_12] = 1

		search_range = self.shrink_range()
		(b_11, b_12) = self.greedy_thinking(is_neg)
		one_b_score = cal_score('black', b_11, b_12)
		Global.black[b_11][b_12] = 1
		Global.flag[b_11][b_12] = 1

		search_range = self.shrink_range()
		(w_21, w_22) = self.greedy_thinking(is_neg)
		two_score = cal_score('white', w_21, w_22)
		Global.white[w_21][w_22] = 1
		Global.flag[w_21][w_22] = 1

		search_range = self.shrink_range()
		(b_21, b_22) = self.greedy_thinking(is_neg)
		two_b_score = cal_score('black', b_21, b_22)

		# Recover
		Global.white[w_11][w_12] = Global.white[w_21][w_22] = 0
		Global.flag[w_11][w_12] = Global.flag[w_21][w_22] = 0
		Global.black[b_11][b_12] = 0
		Global.flag[b_11][b_12] = 0

		w_sums = one_score + two_score
		b_sums = one_b_score + two_b_score
		if w_sums >= b_sums:
			return w_sums, first_best
		else:
			return b_sums, second_best