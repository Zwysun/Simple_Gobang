#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name: GomokuAI_animo
Author: Zwy
"""

import player.animo2.Cal_all_score as Cal_all_score
import player.animo2.Global as Global
import copy

# used for testing
test = [[0 for i in range(15)] for j in range(15)]
a = [[0 for i in range(15)] for j in range(15)]
b = [[0 for i in range(15)] for j in range(15)]
best_b_sums = -1
best_w_sums = -1
best_b = []
best_w = []
black_used_pos = []
white_used_pos = []
max_b_score = -1000
max_w_score = -1000
best_b_pos = []
best_w_pos = []
best_pos = []
search_range = []
origin_color = ''
test_pos = []

def get_next_pos(mod):
	global search_range, best_pos
	search_range = shrink_range()
	try:
		if mod:
			best_pos = machine_thinking_twice(mod)
		else:
			best_pos = machine_thinking(mod)
	except Exception as e:
		print(e)
		return False
	return best_pos

def alpha_beta(color, depth, alpha, beta):
	global test_pos, origin_color, rblack_used_pos, white_used_pos, max_score, best_pos, black_used_pos, white_used_pos, search_range, max_b_score, max_w_score, best_b_pos, best_w_pos
	if origin_color == '':
		origin_color = color
	if depth <= 0:
		if color == 'black':
			ii = black_used_pos[-1][0]
			jj = black_used_pos[-1][1]
			score = Cal_all_score.cal_score_v1('black', ii, jj)
			# max_scores = -5
			# for i in range(15):
			# 	for j in range(15):
			# 		if Global_variables.black[i][j] == 1:
			# 			score = Calcu_every_step_score.cal_score('black', i, j)
			# 			if score > max_scores:
			# 				max_scores = score
				# print 'score：' + str(score)
				# if score > max_b_score:
				# 	max_b_score = score
					# bug 修复
					# best_b_pos = (ii, jj)
					# print best_b_pos
			# return max_b_score
		else:
			ii = white_used_pos[-1][0]
			jj = white_used_pos[-1][1]
			score = Cal_all_score.cal_score_v1('white', ii, jj)
		return score
	for i in range(15):
		for j in range(15):
			# print i,j
			# for k in search_range:
			# 	print k
			# for k in flag:
			# 	print k
			if Global.flag[i][j] == 0 and search_range[i][j] == 1:
				Global.flag[i][j] = 1
				# print i,j
				search_range[i][j] = 0
				if color == 'black':
					# 修复bug * 4 => long time
					Global.black[i][j] = 1
					black_used_pos.append((i, j))
				else:
					Global.white[i][j] = 1
					white_used_pos.append((i, j))
				if color == 'black':
					new_color = 'white'
				else:
					new_color = 'black'
				val = - alpha_beta(new_color, depth-1, -beta, - alpha)
				Global.flag[i][j] = 0
				search_range[i][j] = 1
				if color == 'black':
					black_used_pos.remove((i, j))
					Global.black[i][j] = 0
				else:
					white_used_pos.remove((i, j))
					Global.white[i][j] = 0
				if val >= beta:
					# print 'beta:' + str(beta)
					return beta
				if val > alpha:
					# print alpha
					# 修复bug =》 fatal 233
					if color == origin_color and depth == 4:
						# print origin_color
						# print val
						# print best_pos
						best_pos = (i, j)
					alpha = val
	return alpha

# 寻找'半径'为1的闭包
def shrink_range():
	cover_range = [[0 for i in range(15)] for j in range(15)]
	for i in range(15):
		for j in range(15):
			if Global.flag[i][j] == 1:
				for k in range(3):
					# bug修复
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

# if __name__ == '__main__':
# 	# alpha_beta_test('black', 6, -1000000, 1000000)
# 	# for i in best_b:
# 	# 	print i
# 	# for j in best_w:
# 	# 	print j
# 	search_range = shrink_range()
# 	print alpha_beta('black', 3, -1000000, 1000000)


# 比alpha-beta效果好太多，2017-12-7 11:16 用贪心思想再权衡各参数
def machine_thinking(is_neg):
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
				white_score = Cal_all_score.cal_score_v2('white', i, j)

				Global.white[i][j] = 0
				Global.black[i][j] = 1
				black_score = Cal_all_score.cal_score_v2('black', i, j)

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
def machine_thinking_twice(is_neg):
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
				white_score = Cal_all_score.cal_score_v2('white', i, j)
				Global.white[i][j] = 0
				Global.black[i][j] = 1

				black_score = Cal_all_score.cal_score_v2('black', i, j)
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
	first_sums, first_best = twice_search(first_best, second_best, is_neg)
	second_sums, second_best = twice_search(second_best, first_best, is_neg)
	if first_sums < second_sums:
		first_best = second_best
	# print(first_sums, second_sums)
	return first_best


def twice_search(first_best, second_best, is_neg):
	global search_range
	(w_11, w_12) = first_best
	one_score = Cal_all_score.cal_score_v2('white', w_11, w_12)
	Global.white[w_11][w_12] = 1
	Global.flag[w_11][w_12] = 1

	search_range = shrink_range()
	(b_11, b_12) = machine_thinking(is_neg)
	one_b_score = Cal_all_score.cal_score_v2('black', b_11, b_12)
	Global.black[b_11][b_12] = 1
	Global.flag[b_11][b_12] = 1

	search_range = shrink_range()
	(w_21, w_22) = machine_thinking(is_neg)
	two_score = Cal_all_score.cal_score_v2('white', w_21, w_22)
	Global.white[w_21][w_22] = 1
	Global.flag[w_21][w_22] = 1

	search_range = shrink_range()
	(b_21, b_22) = machine_thinking(is_neg)
	two_b_score = Cal_all_score.cal_score_v2('black', b_21, b_22)

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