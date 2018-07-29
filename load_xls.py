#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xlrd import open_workbook

def load_xls(path, links):
	wb = open_workbook(path)
	for s in wb.sheets():
		for row in range(s.nrows):
			links[s.cell(row, 0).value] = s.cell(row,1).value

links = {}
load_xls('./movies.xlsx', links)
print(links)