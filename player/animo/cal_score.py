# -*- coding: utf-8 -*-
"""
Name: Cal_Score
Author: Zwy
"""

import re

class Global():
	black = [[0 for a in range(15)] for b in range(15)]
	white = [[0 for a in range(15)] for b in range(15)]
	flag = [[0 for a in range(15)] for b in range(15)]
	# 100000
	pattern_5 = [re.compile(r'11111')]
	# 10000 把011112移到下面
	pattern_alive_4 = [re.compile(r'011110')]
	# 8000 去除重复模式
	pattern_to_4 = [re.compile(r'11011'), re.compile(r'011112'), re.compile(r'10111'), re.compile(r'201111')]
	# 5000 双活三原本是01110 但此处应该再加边缘2个0 长度尽量长限制足够大就不会误判
	pattern_double_alive_3 = [re.compile(r'0011100'), re.compile(r'2011100')]
	# 1000
	pattern_alive_sleep_3 = [re.compile(r'0011102')]
	# 500
	pattern_alive_3 = [re.compile(r'010110')]
	# 200 加了边缘两个0的限制,新增‘001102’,'001012
	pattern_double_alive_2 = [re.compile(r'001100'), re.compile(r'001102'), re.compile(r'001012')]
	# 100
	pattern_sleep_3 = [re.compile(r'001112'), re.compile(r'010112'), re.compile(r'011012')
	, re.compile(r'10011'), re.compile(r'10101'), re.compile(r'2011102')]
	# 35 加了两个，无对方棋在边缘的活二
	pattern_alive_sleep_2 = [re.compile(r'0010100'), re.compile(r'00100100')]
	# 15
	pattern_alive_2 = [re.compile(r'201010'), re.compile(r'2010010'),  re.compile(r'20100102'),  re.compile(r'2010102')]
	# 3 加了两个,要保证不陷入死4，即起码还有5个空位
	pattern_sleep_2 = [re.compile(r'000112'), re.compile(r'001012'), re.compile(r'010012')
	, re.compile(r'10001'), re.compile(r'2010102'), re.compile(r'2011002')]
	# -5 这个可以先看一下效果,边缘一个子也会设定为 -5
	pattern_dead_4 = [re.compile(r'2\d{3}12'), re.compile(r'2\d{2}1\d{2}2')]
	# -5
	pattern_dead_3 = [re.compile(r'2\d{2}12')]
	# -5
	pattern_dead_2 = [re.compile(r'2\d12')]

	all_patterns = [pattern_5, pattern_alive_4, pattern_to_4, pattern_double_alive_3, pattern_alive_sleep_3, pattern_alive_3
	, pattern_double_alive_2, pattern_sleep_3, pattern_alive_sleep_2, pattern_alive_2, pattern_sleep_2, pattern_dead_4,
	pattern_dead_3, pattern_dead_2]

	all_scores = [100000, 10000, 8000, 5000, 1000, 200, 100, 50, 10, 5, 3, -5, -5, -5]

	board_scores = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
					[0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
					[0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
					[0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
					[0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0],
					[0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
					[0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
					[0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
					[0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
					[0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
					[0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 0],
					[0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0],
					[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

	search_range = []

def cal_score(color, i, j):
	scores = []
	first_pattern = -1
	second_pattern = -1
	p_index = -1
	# 加一个初边界处理
	pos_row = '2'
	pos_col = '2'
	bia_right = '2'
	bia_left = '2'
	for ii in range(15):
		if Global.black[i][ii] == 1:
			if color == 'black':
				pos_row += '1'
			else:
				pos_row += '2'
		elif Global.white[i][ii] == 1:
			if color == 'black':
				pos_row += '2'
			else:
				pos_row += '1'
		else:
			pos_row += '0'
	pos_row += '2'
	for ii in range(15):
		if Global.black[ii][j] == 1:
			if color == 'black':
				pos_col += '1'
			else:
				pos_col += '2'
		elif Global.white[ii][j] == 1:
			if color == 'black':
				pos_col += '2'
			else:
				pos_col += '1'
		else:
			pos_col += '0'
	pos_col += '2'
	# 要保存两个斜线上组成的字符串中原下棋点的位置
	bia_left_pos = -1
	bia_right_pos = -1
	bia_left_pos_rev = -1
	bia_right_pos_rev = -1
	# 按列数递增遍历，与按行数递增遍历一样的效果
	for ii in range(max(0, i-j), min(i+(14 - j) + 1, 15)):
		if bia_right_pos == -1 and ii == i:
			bia_right_pos = ii - max(0, i-j)
			# print 'bia_right_pos: ' + str(bia_right_pos)
			bia_right_pos_rev = min(i+(14 - j), 15) - 1 - bia_right_pos
		if Global.black[ii][ii + j - i] == 1:
			if color == 'black':
				bia_right += '1'
			else:
				bia_right += '2'
		elif Global.white[ii][ii + j - i] == 1:
			if color == 'black':
				bia_right += '2'
			else:
				bia_right += '1'
		else:
			bia_right += '0'
	# 加一个末边界处理
	bia_right += '2'
	# print 'bia_right:' + bia_right
	for ii in range(max(0, i-(14 - j)), min(i + j + 1, 15)):
		if bia_left_pos == -1 and ii == i:
			bia_left_pos = ii - max(0, i-(14 - j))
			# print 'bia_left_pos: ' + str(bia_left_pos)
			bia_left_pos_rev = min(i + j + 1, 15) - 1 - bia_left_pos
		if Global.black[ii][j - (ii - i)] == 1:
			if color == 'black':
				bia_left += '1'
			else:
				bia_left += '2'
		elif Global.white[ii][j - (ii - i)] == 1:
			if color == 'black':
				bia_left += '2'
			else:
				bia_left += '1'
		else:
			bia_left += '0'
	bia_left += '2'
	# print 'bia_left:' + bia_left
	search_flag = False
	# pos_col = pos_col[max(0, j-6):min(j+6, 15)]
	rev_col = pos_col[::-1]
	# pos_row = pos_row[max(0, i-6):min(i+6, 15)]
	rev_row = pos_row[::-1]
	rev_bia_left = bia_left[::-1]
	rev_bia_right = bia_right[::-1]
	score = 0
	# 加了末边界处理后要统一将下标都加1
	i += 1
	j += 1
	bia_left_pos += 1
	bia_right_pos += 1
	bia_left_pos_rev += 1
	bia_right_pos_rev += 1
	for patterns in Global.all_patterns:
		for p in patterns:
			result = re.search(p, pos_col)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_col)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, pos_row)
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_row)
			if result:
				search_range = result.span()
				if (search_range[0] <= i <= search_range[1]) or (search_range[0] <= j <= search_range[1]):
					score = Global.all_scores[Global.all_patterns.index(patterns)]
					first_pattern = Global.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					# print result.span()
					search_flag = True
					break
			# 处理两种斜线上的情况
			pos = -1
			if not result or not ((result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, bia_left)
				if result:
					pos = bia_left_pos
					# print 'test:' + str(result.span())
					# print 'pos:' + str(pos)
			if not result or not result.span()[0] <= pos <= result.span()[1]:  # ，pos要固定
				result = re.search(p, rev_bia_left)
				if result:
					pos = bia_left_pos_rev
					# print 'test:' + str(result.span())
					# print 'pos:' + str(pos)
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, bia_right)
				if result:
					pos = bia_right_pos
					# print 'test:' + str(result.span())
					# print 'pos:' + str(pos)
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, rev_bia_right)
				if result:
					pos = bia_right_pos_rev
					# print 'test:' + str(result.span())
					# print 'pos:' + str(pos)
			if result:
				search_range = result.span()
				if search_range[0] <= pos <= search_range[1]:
					score = Global.all_scores[Global.all_patterns.index(patterns)]
					first_pattern = Global.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					# print result.span()
					search_flag = True
					break
		if search_flag:
			break
	search_flag = False
	for patterns in Global.all_patterns[first_pattern:]:
		for p in patterns:
			if patterns == Global.all_patterns[first_pattern]:
				if patterns.index(p) <= p_index:
					continue
			result = re.search(p, pos_col)
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_col)
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, pos_row)
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, rev_row)
			if result:
				search_range = result.span()
				if (search_range[0] <= i <= search_range[1]) or (search_range[0] <= j <= search_range[1]):
					score = Global.all_scores[Global.all_patterns.index(patterns)]
					first_pattern = Global.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					# print result.span()
					search_flag = True
					break
			# 处理两种斜线上的情况
			pos = -1
			if not result or not (
				(result.span()[0] <= i <= result.span()[1]) or (result.span()[0] <= j <= result.span()[1])):
				result = re.search(p, bia_left)
				if result:
					pos = bia_left_pos
				# print 'test:' + str(result.span())
				# print 'pos:' + str(pos)
			if not result or not result.span()[0] <= pos <= result.span()[1]:  # ，pos要固定
				result = re.search(p, rev_bia_left)
				if result:
					pos = bia_left_pos_rev
				# print 'test:' + str(result.span())
				# print 'pos:' + str(pos)
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, bia_right)
				if result:
					pos = bia_right_pos
				# print 'test:' + str(result.span())
				# print 'pos:' + str(pos)
			if not result or not result.span()[0] <= pos <= result.span()[1]:
				result = re.search(p, rev_bia_right)
				if result:
					pos = bia_right_pos_rev
				# print 'test:' + str(result.span())
				# print 'pos:' + str(pos)
			if result:
				search_range = result.span()
				# print search_range
				if search_range[0] <= pos <= search_range[1]:
					score = Global.all_scores[Global.all_patterns.index(patterns)]
					first_pattern = Global.all_patterns.index(patterns)
					scores.append(score)
					p_index = patterns.index(p)
					# print result.span()
					search_flag = True
					break
		if search_flag:
			break
	# i-1
	# print 'origin: ' + str(Global_variables.board_scores[i - 1][j - 1]) + ' point: ' + str('%d,%d' % (i-1, j-1))
	# print 'score: ' + str(score)
	# print scores
	if len(scores) == 2:
		score = sum(scores)
	elif len(scores) != 0:
		score = max(scores)
	# print sum(scores) + Global_variables.board_scores[i-1][j-1]
	return score + Global.board_scores[i-1][j-1]
