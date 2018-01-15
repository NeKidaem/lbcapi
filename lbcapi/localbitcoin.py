# -*- coding: utf-8 -*-
__author__ = 'Marco Borges'
__version__ = '0.0.2'

from .api import hmac, Connection

class Payment(object):
	def __init__(self, code, name, currencies=None):
		self.code = code
		self.name = name
		self.currencies = currencies or list()
	
	def __contains__(self, code):
		return code in self.currencies
	
	def __str__(self):
		return self.code


class Currency(object):
	def __init__(self, code, name, altcoin=False):
		self.code = code
		self.name = name
		self.altcoin = altcoin
	
	def __str__(self):
		return self.code

class LocalBitcoin(object):
	"""LocalBitcoins API Integration"""
	
	def __init__(self, hmac_key='', hmac_secret=''):
		
		if hmac_key and hmac_secret:
			self.conn = hmac(hmac_key, hmac_secret)
			self.auth = True
		else:
			self.conn = Connection()
			self.conn.server = 'https://localbitcoins.com'
			self.auth = False
		self.cc = []
		self.pm = []
		self.curr = []
		
	def active(self):
		ac = self.conn.call('GET', '/api/dashboard/').json()
		return ac['data']['contact_list']
	
	def ads(self):
		if not self.auth: raise Exception('Method need Authentication!')
		ads = self.conn.call('GET', '/api/ads/').json()
		#TODO: review
		return ads
	
	def canceled(self):
		ac = self.conn.call('GET', '/api/dashboard/canceled/').json()
		return ac['data']['contact_list']

	def closed(self):
		ac = self.conn.call('GET', '/api/dashboard/closed/').json()
		return ac['data']['contact_list']
		
	def country_codes(self):
		"""Returns a list of valid and recognized countrycodes for LocalBitcoins."""
		if len(self.cc) == 0:
			cc = self.conn.call('GET', '/api/countrycodes/').json()
			self.cc = cc['data']['cc_list']
		return self.cc
	
	def currencies(self):
		if len(self.curr) == 0:
			curr = self.conn.call('GET', '/api/currencies/').json()
			for k, v in curr['data']['currencies'].items():
				c = Currency(k, v['name'], v['altcoin'])
				self.curr.append(c)
		return [k.code for k in self.curr]
	
	def fees(self):
		"""Returns deposit and outgoing fees."""
		dat = self.conn.call('GET', '/api/fees/').json()
		deposit = float(dat['data']['deposit_fee'])
		outgoing = float(dat['data']['outgoing_fee'])
		return (deposit, outgoing)
	
	def payment_methods(self, country_code=''):
		"""Returns a list of valid payment methods. Also contains name and code for payment methods,
		and possible limitations in currencies and bank name choices. You can filtered by countrycodes."""
		if len(self.pm) == 0:
			pm = self.conn.call('GET', '/api/payment_methods/').json()
			for k, v in pm['data']['methods'].items():
				p = Payment(v['code'], v['name'], v['currencies'])
				self.pm.append(p)
		if len(country_code) > 0 and country_code in self.country_codes():
			pm = self.conn.call('GET', '/api/payment_methods/?countrycode=%s' % country_code).json()
			m = list()
			for k, v in pm['data']['methods'].items():
				m.append(v['code'])
			return m
		return [k.code for k in self.pm]
	
	def sell_online(self, payment_method=None, currency=None, country_code=None):
		if payment_method == None and currency == None and country_code == None:
			sell_list = list()
			sell = self.conn.call('GET', '/sell-bitcoins-online/.json', all_pages=True).json()
			
	
	def wallet(self):
		"""Returns wallet balance and sendable BTC values."""
		dat = self.conn.call('GET', '/api/wallet/').json()
		balance = float(dat['data']['total']['balance'])
		sendable = float(dat['data']['total']['sendable'])
		return (balance, sendable)
	
	def wallet_detail(self):
		"""Returns dict with wallet datailed info."""
		dat = self.conn.call('GET', '/api/wallet/').json()
		return dat['data']
