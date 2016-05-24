#!/usr/bin/python

#CS544 - Computer Networks
#Group 8
#BGP Protocol
#Team Members: Brian Quinn, TJ Rhodes, Ryan Mann, Marc Thomson

#Module name: message_handler
#Description: exposes a verify_message function for verifying message version and client id
import message

class MessageHandler(object):

	def __init__(self, version):
		self.version = version
		#will hold a pair of client_id's for a given game
		self.client_id_pairs = []
	
	def verify_message(self, message):

		valid_version = True
		valid_client_id = True

		if message.version != self.version:
			valid_version = False
		elif message.client_id != 0:
			found = False
			for (cid_1, cid_2) in self.client_id_pairs:
				if message.client_id == cid_1 or message.client_id == cid_2:
					found = True
					break

			valid_client_id = found

		return valid_version and valid_client_id


