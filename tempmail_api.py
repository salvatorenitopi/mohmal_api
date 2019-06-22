# -*- coding: utf-8 -*-


import re
import time
import requests
import random
import email


class tempmail_api:
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
		domains = self.session.get("https://temp-mail.org/en/option/change/", proxies=self.proxy, allow_redirects=True)
		domains_match=re.compile('<option value="@(.+?)">').findall(domains.text)
		return domains_match


	def create_mail (self, name, domain):
		init = self.session.get("https://temp-mail.org/en/option/change/", proxies=self.proxy, allow_redirects=True)
		csrf = self.session.cookies['csrf']
		if len(csrf) != 32:
			return -1
		
		post_data = { "csrf":csrf, "mail":name , "domain": "@" + domain }
		create = self.session.post("https://temp-mail.org/en/option/change/", data=post_data, proxies=self.proxy, allow_redirects=True)

		verify = create.text.find(name+"@"+domain)
		if (verify != -1):
			self.mail = name+"@"+domain
			return name+"@"+domain
		else:
			return -2	# Can not create mail


	def create_random_mail (self):
		create = self.session.get("https://temp-mail.org/en", proxies=self.proxy, allow_redirects=True)
		mail = re.compile('"Your Temporary Email Address" data-placement="bottom" class="emailbox-input opentip" value="([^@]+@[^@]+\.[^@]+)" readonly />').findall(create.text)
		if len(mail) == 1:
			return mail[0]
		else:
			return -1


	def get_messages_list (self):
		inbox = self.session.get("https://temp-mail.org/en/option/refresh/", proxies=self.proxy, allow_redirects=True)
		messages_match=re.compile('<a href="https://temp-mail.org/en/view/(.+?)" title=').findall(inbox.text)
		return list(dict.fromkeys(messages_match))


	def get_message (self, msg_id):
		msg = self.session.get("https://temp-mail.org/en/source/" + str(msg_id), proxies=self.proxy, allow_redirects=True)
		body = ""
		b = email.message_from_string(msg.text.encode("utf-8"))
		if b.is_multipart():
			for payload in b.get_payload():
				body += payload.get_payload()
		else:
			body = b.get_payload()

		return body


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