from Queue import Queue, Full
import random
from threading import Thread
import time

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
QUEUE = Queue(300)
STOP = False
COUNT = 0

def _fetch(username):
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    resp = requests.get("{}/{}".format(BASE_URL, username), headers=headers)
    if resp.status_code == 404:
        return None
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
    except Exception as e:
        _write_err(str(e) + "\n" + text)
        return 0


def _store(session, *args):
    db.add(session, *args)


def _queue(username):
    try:
        QUEUE.put(username, timeout=0)
    except Full:
        return


def get(username, session):
    """ Return a list of who this person follows"""
    print username
    text = _fetch(username)
    if not text:
        return
    friends = _get_friends(text)
    score = _get_score(text)
    user = db.create_user(session, username, score)
    for index, friend in enumerate(friends):
        friend_record = db.exists(session, friend)
        if not friend_record:
            friend_record = db.create_user(session, friend)
            _queue(friend)
        _store(session, user.id, friend_record.id, index + 1)


def _add_seeds(session):
    users = db.find_queued_users(session, 200)
    for user in users:
        QUEUE.put(user.username)


def worker():
    global COUNT
    while not STOP:
        try:
            session = db.get_session()
            username = QUEUE.get()
            get(username, session)
            QUEUE.task_done()
        finally:
            COUNT += 1
            with open('count', 'w') as f:
                f.write(str(COUNT))
            session.close()


if __name__ == "__main__":
    count = 0

    if db.get_count() == 0:
        while len(SEEDS):
            seed = SEEDS.pop()
            count += 1
            QUEUE.put(seed)
    else:
        session = db.get_session()
        _add_seeds(session)

    for i in range(10):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    try:
        while True:
            if QUEUE.qsize() > 0:
                time.sleep(20)
            else:
                session = db.get_session()
                _add_seeds(session)

    except KeyboardInterrupt:
        print "interrupted"
        STOP = True

