# -*- coding: utf-8 -*-


import traceback
import mohmal_api as mohmal_api


proxy_ip = "127.0.0.1"
proxy_port = "8080"

proxyDict = { 
	"http"  : str(proxy_ip) + ":" + str(proxy_port), 
	"https" : str(proxy_ip) + ":" + str(proxy_port), 
	"ftp"   : str(proxy_ip) + ":" + str(proxy_port)
	}

m = mohmal_api.mohmal_api(proxyDict)
print m.create_random_mail()						# print the email address created randomly

while True:
	raw_input ("...")								# wait for user to press enter
	msg_lst = m.get_messages_list()					# get the messages list
	print msg_lst									# print the messages list array
	if (len(msg_lst) > 0):							# if array is empty print the first message
		try: 
			print m.get_message(msg_lst[0])
			break

		except Exception, e:
			traceback.print_exc(e)
	else:											# else print an error
		print "messages list is empty"