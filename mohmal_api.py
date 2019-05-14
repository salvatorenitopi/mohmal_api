# -*- coding: utf-8 -*-


import re
import time
import requests
import random


class mohmal_api:
	def __init__ (self, proxy=None):
		self.session = requests.Session()
		self.proxy = proxy
		self.mail = None

		self.headers = {
			'Connection': 'keep-alive',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Google Chrome Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
			'DNT': '1',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
			'Accept-Language': 'en-US,en;q=0.5',
		}
		self.session.headers.update(self.headers)


	def get_domain_list (self):
		domains = self.session.get("https://www.mohmal.com/en", proxies=self.proxy, allow_redirects=True)
		domains_match=re.compile('<option value="(.+?)"').findall(domains.text)
		return domains_match


	def create_mail (self, name, domain):
		post_data = { "name":name , "domain":domain}
		create = self.session.post("https://www.mohmal.com/en/create", data=post_data, proxies=self.proxy, allow_redirects=True)
		verify = create.text.find(name+"@"+domain)
		if (verify != -1):
			self.mail = name+"@"+domain
			return name+"@"+domain
		else:
			return -1	# Can not create mail


	def create_random_mail (self):
		lst = self.get_domain_list()
		if (len(lst) > 0):
			return self.create_mail(''.join(random.choice('0123456789qwertyuiopasdfghjklzxcvbnm') for i in range(10)), lst[0])
		else:
			return -1	# Can not create mail


	def get_messages_list (self):
		inbox = self.session.get("https://www.mohmal.com/en/inbox", proxies=self.proxy, allow_redirects=True)
		messages_match=re.compile('<tr data-msg-id="(.+?)"').findall(inbox.text)
		return messages_match


	def get_message (self, msg_id):
		msg = self.session.get("https://www.mohmal.com/en/message/" + str(msg_id), proxies=self.proxy, allow_redirects=True)
		return msg.text


	# EXPERIMENTAL
	def auto_verify_link (self):
		msg_lst = self.get_messages_list()

		if (len(msg_lst) < 1): 
			return -1	# No message received yet

		else:
			msg = self.get_message(msg_lst[0])
			urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)
			
			allok = True

			for u in urls:
				try:
					requests.get(u, headers=self.headers)
				except:
					allok = False

			return -2 if (allok == False) else 0

