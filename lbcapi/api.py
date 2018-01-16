import hashlib
import hmac as hmac_lib
import requests
import time
try:
	# Python 3.x
	from urllib.parse import urlparse, parse_qs
except ImportError:
	# Python 2.7
	from urlparse import urlparse, parse_qs


def oauth2(access_token, client_id, client_secret=None, refresh_token=None, server='https://localbitcoins.com'):
	conn = Connection()
	conn._set_oauth2(server, client_id, client_secret, access_token, refresh_token)
	return conn


def hmac(hmac_key, hmac_secret, server='https://localbitcoins.com'):
	conn = Connection()
	conn._set_hmac(server, hmac_key, hmac_secret)
	return conn


class Connection():

	def __init__(self):
		self.server = None
		self.__last_response = dict()

		# OAuth2 stuff
		self.client_id = None
		self.client_secret = None
		self.access_token = None
		self.refresh_token = None
		self.expiry_seconds = None

		# HMAC stuff
		self.hmac_key = None
		self.hmac_secret = None

	def call(self, method, url, params=None, stream=False, files=None, retry=10, all_pages=False):
		method = method.upper()
		if method not in ['GET', 'POST']:
			raise Exception(u'Invalid method {}!'.format(method))

		if method == 'GET' and files:
			raise Exception(u'You cannot send files with GET method!')

		# If URL is absolute, then convert it
		if url.startswith(self.server):
			url = url[len(self.server):]

		# If OAuth2
		if self.access_token:

			# Refresh session, if possible
			if self.refresh_token and self.client_id and self.client_secret:
				refresh_params = {
					'refresh_token': self.refresh_token,
					'grant_type': 'refresh_token',
					'client_id': self.client_id,
					'client_secret': self.client_secret,
				}
				r = requests.post(self.server + '/oauth2/access_token/', data=refresh_params)
				self.access_token = r.json()['access_token']
				self.refresh_token = r.json()['refresh_token']
				self.expiry_seconds = int(r.json()['expires_in'])

			headers = {
				'Authorization-Extra': 'Bearer ' + self.access_token,
			}

			if method == 'GET':
				self.__last_response = requests.get(self.server + url, params=params, headers=headers, stream=stream)
			else:
				self.__last_response = requests.post(self.server + url, data=params, headers=headers, stream=stream, files=files)

		# If HMAC
		else:
			session = requests.Session()
			# Loop, so retrying is possible if nonce fails
			while retry > 0:

				# .encode('ascii') ensures a bytestring on Python 2.7 and 3.x
				nonce = str(int(time.time() * 1000)).encode('ascii')

				# Prepare request based on method.
				if method == 'POST':
					api_request = requests.Request('POST', self.server + url, data=params, files=files).prepare()
					params_encoded = api_request.body

				# GET method
				else:
					api_request = requests.Request('GET', self.server + url, params=params).prepare()
					params_encoded = urlparse(api_request.url).query

				# Calculate signature
				# .encode('ascii') ensures a bytestring on Python 2.7 and 3.x
				if self.hmac_key:
					message = nonce + self.hmac_key + url.encode('ascii')
					if params_encoded:
						message += str(params_encoded).encode('ascii')
					signature = hmac_lib.new(self.hmac_secret, msg=message, digestmod=hashlib.sha256).hexdigest().upper()

					# Store signature and other stuff to headers
					api_request.headers['Apiauth-Key'] = self.hmac_key
					api_request.headers['Apiauth-Nonce'] = nonce
					api_request.headers['Apiauth-Signature'] = signature

				# Send request
				self.__last_response = session.send(api_request, stream=stream)

				# If HMAC Nonce is already used, then wait a little and try again
				try:
					response_json = self.__last_response.json()
					if response_json.get('error', {}).get('error_code') == '42':
						time.sleep(0.1); continue
					if 'data' in response_json or len(response_json) > 0: break
				except: retry -= 1
		
			if all_pages:
				page_list = list()
				page_list.append(self.__last_response)
				last = self.__last_response.json()
				while 'pagination' in last:
					page = last.get('pagination', {})
					page = page.get('next', None)
					if page == None: break
					if method == 'POST': api_request = requests.Request('POST', page).prepare()
					else: api_request = requests.Request('GET', page).prepare()
					self.__last_response = session.send(api_request, stream=stream)
					page_list.append(self.__last_response)
				return page_list
			
		return self.__last_response

	def get_access_token(self):
		return self.access_token

	def get_refresh_token(self):
		return self.refresh_token

	def get_expiry_seconds(self):
		return self.expiry_seconds

	def _set_oauth2(self, server, client_id, client_secret, access_token, refresh_token):
		self.server = server
		self.client_id = client_id
		self.client_secret = client_secret
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.expiry_seconds = None
		self.hmac_key = None
		self.hmac_secret = None

	def _set_hmac(self, server, hmac_key, hmac_secret):
		self.server = server
		self.client_id = None
		self.client_secret = None
		self.access_token = None
		self.refresh_token = None
		self.expiry_seconds = None
		# .encode('ascii') ensures a bytestring on Python 2.7 and 3.x
		self.hmac_key = hmac_key.encode('ascii')
		self.hmac_secret = hmac_secret.encode('ascii')
