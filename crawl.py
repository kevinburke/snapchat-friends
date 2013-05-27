import random
import time
from Queue import Queue
from threading import Thread

from lxml import etree
import requests

import db

BASE_URL = 'http://www.snapchat.com'
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/23 Safari/536.5',
    'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
]
SEEDS = open('seeds').read().splitlines()
QUEUE = Queue()
STOP = False

def worker():
    while not STOP:
        username = QUEUE.get()
        get(username)
        QUEUE.task_done()


def _fetch(username):
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    resp = requests.get("{}/{}".format(BASE_URL, username), headers=headers)
    return resp.text


def _write_err(text):
    with open('parse.err', 'w') as f:
        f.write(text)
        f.write("\n\n")


def _get_friends(text):
    """ this is not the most robust function in the world """
    def _find_friends(child):
        link = child.find('.//a')
        return link.text

    try:
        html = etree.HTML(text)
        friends_div = html.find('.//div[@id="panel3"]')
        return [_find_friends(child) for child in friends_div.iterchildren()]
    except:
        _write_err(text)
        return []


def _get_score(text):
    try:
        html = etree.HTML(text)
        score_div = html.find('.//div[@id="score"]')
        # format is HISCORE&nbsp;3428
        parts = score_div.text.split(u'\xa0')
        return int(parts[1])
    except:
        _write_err(text)
        return 0




def _store(user_id, friend_id, index):
    db.add(user_id, friend_id, index)


def _already_indexed(username):
    first = db.exists(username)
    if first:
        return first.id
    return None


def _queue(username):
    QUEUE.put(username)


def get(username):
    """ Return a list of who this person follows"""
    print username
    text = _fetch(username)
    friends = _get_friends(text)
    score = _get_score(text)
    user_id = db.create_user(username, score)
    for index, friend in enumerate(friends):
        record = _already_indexed(friend)
        if not record:
            record = db.create_user(friend)
            _queue(friend)
        _store(user_id, record, index + 1)


def _add_seeds():
    users = db.find_queued_users()
    for user in users:
        QUEUE.put(user.username)


if __name__ == "__main__":
    count = 0
    while len(SEEDS):
        seed = SEEDS.pop()
        count += 1
        QUEUE.put(seed)
    _add_seeds()

    for i in range(10):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    try:
        time.sleep(200)
    except KeyboardInterrupt:
        print "interrupted"
        STOP = True

