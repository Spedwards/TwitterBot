# TwitterBot
A Reddit/Twitter bot posting everything from a subreddit to Twitter
Requires Python 3+

# Installation
To install TwitterBot, you first have to install `praw` and `tweepy`.

## Variables to Change
There are 9 variables to change along with 4 other bits of text.

First of all, your account username and password need to be changed on lines 36 and 37.  
Next is the Subreddit you want the bot to operate it. This is the next line down.

The next four variables are your Twitter app Consumer Key, Consumer Secret Key, Access Token and Access Secret Token. Don't share these with anyone.

The loop delay should be left at 900 unless you have an active subreddit. 900 seconds is 15 minutes.

`DIR` is the directory the donelist and avoidance lists will be saved.

---
In the user agent string, change what subreddit you are using and where the tweets are being posted from.

On line 83, add your main account's username to the end of the message.

## Save files
In the directory you saved above, you need to create 2 files. `avoid.txt` and `done.txt`. Avoid will be a list of all names who do not want to receive further messages from the bot. Done is a list of all posts already tweeted out.

# Running
You are now free to run the bot! Note that the account your bot runs on will need some link karma. I suggest visiting /r/FreeKarma

# Closing
After running the bot, if you want to close it, do not just close out of the window. Instead, type `exit` into the window and let it close on it's own.
