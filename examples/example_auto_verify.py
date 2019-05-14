# -*- coding: utf-8 -*-


# EXPERIMENTAL
# EXPERIMENTAL
# EXPERIMENTAL


import traceback
import mohmal_api as mohmal_api


m = mohmal_api.mohmal_api()
print m.create_random_mail()						# print the email address created randomly

while True:
	raw_input ("...")								# wait for user to press enter
	msg_lst = m.get_messages_list()					# get the messages list
	print msg_lst									# print the messages list array
	if (len(msg_lst) > 0):							# if array is empty auto_verify
		try: 
			print m.auto_verify_link()				# auto_verification is made making a request to all the url in the first message
			break

		except Exception, e:
			traceback.print_exc(e)
	else:											# else print an error
		print "messages list is empty"