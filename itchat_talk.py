# -*- encoding:utf-8 -*-
"""
Wechat auto reply movies info in real-time mode by crawling douban website

(1)
    * sender could select the movie type according to popup movie type list
    * receiver will response with fist 10 movies listed in douban in three sequence mode(hot, time, commend)
(2)
    * sender could select the movie from the movies searched from above operation
    * receiver will response with the specific info of selected movies
"""
import itchat
import douban_crawl
import re
from xlrd import open_workbook
from os import path

# load info of movies from given file
def load_xls(path, links):
	wb = open_workbook(path)
	for s in wb.sheets():
		for row in range(s.nrows):
			links[s.cell(row, 0).value] = s.cell(row,1).value

links = {}

@itchat.msg_register(itchat.content.TEXT, itchat.content.PICTURE)
def simple_reply(msg):
	global movie_info_all
	# 接受用户任意包含“电影”的字样，跳转到指定页面等待
	if u'电影' in msg['Text']:
	    douban_object.browser_hotopen()
	    douban_object.cvt_cmd_to_ctgy_url(msg['Text'])
	    movie_category_option = ' '.join(douban_crawl.movie_category)
	    itchat.send_msg('----请选择一种类型----\n' + movie_category_option, msg['FromUserName'])
	else:
		find_info = False
		# 接受用户的电影类型输入，并执行概况信息爬取，然后反馈给用户
		for category in douban_crawl.movie_category:
			if category in msg['Text']:
				find_info = True
				itchat.send_msg('正在查找' + category + '电影...', msg['FromUserName'])
				del douban_crawl.command_cache[:]
				douban_crawl.command_cache.append(category)
				 # 进行概况信息爬取，并将所有排列列表扩展到一起
				movie_info_all = douban_object.browser_action_general_info(category)
				itchat.send_msg('----按热度排序----\n' + '\n' + '\n'.join(douban_crawl.movie_info_hot), msg['FromUserName'])
				itchat.send_msg('----按时间排序----\n' + '\n' + '\n'.join(douban_crawl.movie_info_time), msg['FromUserName'])
				itchat.send_msg('----按评论排序----\n' + '\n' + '\n'.join(douban_crawl.movie_info_comment), msg['FromUserName'])
		# 接受用户的电影名的选择，并进行指定电影的详细字段爬取，然后返回给用户
		if not find_info:
			search_num = 0
			for x in movie_info_all:
				# Get movie_name from format "10.电影名：9.7分"
				movie_name = re.match(r'^\d*\.(\w+):', x)
				if movie_name:
					movie_name = movie_name.group(1)
				else:
					continue
				if movie_name in msg['Text']:
					itchat.send_msg('正在查找' + movie_name + '...', msg['FromUserName'])
					loc = movie_info_all.index(x)
					if 0 <= loc < 10:
						search_num = 1
					elif 10 <= loc < 20:
						search_num = 2
					else:
						search_num = 3
					url_result = douban_object.browser_action_detail_info(search_num, movie_name)
					html_result = douban_object.download_detail_info_html(url_result)
					douban_object.parse_detail_info(html_result)
					movie_link = ""
					for x in links.keys():
						if movie_name in x or x in movie_name:
							movie_link = links[x]
					douban_crawl.movie_detail_info.append("豆瓣链接： " + url_result)
					douban_crawl.movie_detail_info.append("百度云资源： " + movie_link)
					itchat.send_msg('\n\n'.join(douban_crawl.movie_detail_info), msg['FromUserName'])
					break


if __name__ == '__main__':
	movie_dir = path.join(path.dirname(__file__), 'movies.xlsx')
	load_xls(movie_dir, links)
	# for x in links:
		# print(x + ' ' + links[x])
	itchat.auto_login(hotReload=True)
	douban_object = douban_crawl.DoubanSpider()
	movie_info_all = []
	itchat.run()


