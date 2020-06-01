import praw
import re
from secrets import *

rx = "(\[([^\(\)]*)\])\(https?:\/\/((www|old|np|i|beta|m|pay|ssl|new|alpha)\.)?(reddit\.com)\/r\/(\S*)\)"
rxUrl = "https?:\/\/((www|old|np|i|beta|m|pay|ssl|new|alpha)\.)?(reddit\.com)\/r\/(\S*)"

reddit = praw.Reddit(client_id=cId,
    client_secret=cSecret,
    password=pw,
    user_agent=uAgent,
    username=user)

srd = reddit.subreddit("subredditdrama")


for submission in srd.stream.submissions():
    print(submission.title)
    comment=""
    if submission.is_self:

        #Scan for all links and post
        links = re.findall(rx, submission.selftext)
        for link in links:
            urlText = (link[1][:30] + "...") if len(link[1]) > 30 else link[1]
            #print("Text: " + urlText + "Link: " + link[5])
            comment+= urlText + " - [removeddit](https://removeddit.com/r/" + link[5] + "]\n"
    else:
        urlText = (submission.title[:30] + "...") if len(submission.title) > 30 else submission.title
        #Replace link with removeddit and comment
        url = re.search(rxUrl, submission.url)
        if(url != None):
            #print("LINKPOST: https://removeddit.com/r/" + url[4])
            comment += urlText + " - [removeddit](https://removeddit.com/r/" + url[4] + "]\n"

    print(comment)
    submission.reply(comment)