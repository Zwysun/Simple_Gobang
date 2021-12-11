#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name: GomokuAI_animo
Author: Zwy
"""

import player.animo2.Global as Global
import re


def cal_score_v1(color, i, j):
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
	# print 'bia_right:' + str(len(bia_right))
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
	# print 'bia_left:' + str(len(bia_left))
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
			if not result or not result.span()[0] <= pos <= result.span()[1]:  #pos要固定
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
					# print result.span()
					search_flag = True
					break
		if search_flag:
			break
	return score + Global.board_scores[i-1][j-1]

def cal_score_v2(color, i, j):
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
