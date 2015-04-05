import os
import praw
import threading
import time
import tweepy

def basicThread():
	global looping
	looping = True
	while True:
		i = input()
		if i == 'exit':
			looping = False
			print("Loop will close on next iteration.")
		else:
			print("1:", i)

t1 = threading.Thread(target=basicThread)
t1.daemon = True
t1.start()

version = '1.0.0'

print('Initializing NAME v%s'%version)

'''
CONFIGURATION
'''

USERAGEN = '''App: Reddit to Twitter # user agent
				Version: %s
				Description: Formats posts from /r/SUBREDDIT and tweets them on @TWITTER
				Known Issues: None'''%version


USERNAME = '' # account username
PASSWORD = '' # account password
SUBREDDT = '' # subreddit
CONSUMERKEY = ''
CONSUMERSECRET = ''
ACCESSTOKEN = ''
ACCESSSECRET = ''
LOOP_DEL = 900 # seconds
DIR = '' # Directory to save

'''
/CONFIGURATION
'''

os.chdir(DIR)

def signIn(username,password,useragent):
	import praw
	import re
	r = praw.Reddit(user_agent=re.compile(r'\t+').sub('',useragent))
	r.login(username,password)
	return r

def doneList():
	with open('done.txt') as f:
		donelist = f.readlines()
	donelist = [x.strip('\n') for x in donelist]
	return donelist
	
def doneListWrite(content):
	with open('done.txt', 'a') as f:
		f.write(content)
		
def unreadMessages(messages):
	arr = []
	for x in messages:
		arr.append(x.author.name + '_:_' + x.subject + '_:_' + x.body)
		x.mark_as_read()
	handleMessages(arr)

def handleMessages(arr):
	for x in arr:
		split = x.split('_:_')
		if split[2] != 'remove':
			r.send_message(split[0], split[1], 'I am a bot, this cannot respond correctly.')
		else:
			print('%s wishes to be removed from the mailing list'%split[0])
			r.send_message(split[0], 'Removal Confirmed', 'You have been removed from the list. To be re-added, please contact /u/Spedwards')
			avoidListWrite(split[0])

def avoidList():
	with open('avoid.txt') as f:
		avoidlist = f.readlines()
	avoidlist = [x.strip('\n') for x in avoidlist]
	return avoidlist

def avoidListWrite(name):
	with open('avoid.txt', 'a') as f:
		f.write('%s\n'%name)

def tweetOut(content, api):
	try:
		s = api.update_status(status=content)
		return s
	except:
		print('Error: %s'%content)

message_footer = "\n\n---\n^(I am a bot. If you do not want to receive any of these message, please [)[^(click this link and press send)](http://www.reddit.com/message/compose/?to=%s&subject=Removal&message=remove)^(].)"%USERNAME

auth = tweepy.OAuthHandler(CONSUMERKEY, CONSUMERSECRET)
auth.set_access_token(ACCESSTOKEN, ACCESSSECRET)
api = tweepy.API(auth)

r = signIn(USERNAME, PASSWORD, USERAGEN)

subreddit = r.get_subreddit(SUBREDDT)
while looping:
	for submission in subreddit.get_new(limit=10):
		unreadMessages(r.get_unread())
		avoid = avoidList()
		already_done = doneList()
		sub_id = submission.id
		if submission.id not in already_done:
			sub_title = submission.title
			sub_body = submission.selftext
			sub_author = submission.author
			shortlink = submission.short_link
			foot = "\n" + shortlink
			if (len(sub_title) + len(foot)) >= 130:
				sub_title = sub_title[:(137-len(foot))]
			head = sub_title + "\n"
			if sub_body != '':
				if len(sub_body) >= 139:
					length = 140 - (len(head) + len(foot)) - 4
					body = sub_body[:length] + "..."
				else:
					length = 140 - (len(head) + len(foot)) - 1
					body = sub_body[:length]
			else:
				body = ''
			
			tweet = head + foot
			status = tweetOut(tweet, api)
			if type(status) != type(None):
				status_url = 'https://twitter.com/' + status.author.screen_name + '/status/' + status.id_str
				
				print('\nPost, "' + sub_title + '", by ' + sub_author.name + ' has been tweeted.\n' + status_url + '\n')
				
				if sub_author not in avoid:
					r.send_message(sub_author.name, 'Post Tweeted', 'Your post, "' + sub_title + '", has been tweeted.\n\n' + status_url + message_footer)
			
			already_done.append(sub_id)
			doneListWrite('%s\n'%sub_id)
	time.sleep(LOOP_DEL)
