import random
import time

import gevent
import gevent.monkey
gevent.monkey.patch_all(httplib=True)
from gevent.pool import Pool
from lxml import etree
import grequests

import db

BASE_URL = 'http://www.snapchat.com'
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/23 Safari/536.5',
    'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
]
SEEDS = open('seeds').read().splitlines()
POOL = Pool(10)


def _callback(r):
    print dir(r)
    _parse_text(r.text)

def _fetch(username):
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    return grequests.get("{}/{}".format(BASE_URL, username), headers=headers,
                         callback=_callback)


def _get_friends(text):
    """ this is not the most robust function in the world """
    def _find_friends(child):
        link = child.find('.//a')
        return link.text

    html = etree.HTML(text)
    friends_div = html.find('.//div[@id="panel3"]')
    return [_find_friends(child) for child in friends_div.iterchildren()]


def _get_score(text):
    html = etree.HTML(text)
    score_div = html.find('.//div[@id="score"]')
    # format is HISCORE&nbsp;3428
    parts = score_div.text.split(u'\xa0')
    return int(parts[1])


def _store(user_id, friend_id, index):
    db.add(user_id, friend_id, index)


def _already_indexed(username):
    first = db.exists(username)
    if first:
        return first.id
    return None


def _queue(username):
    SEEDS.append(username)


def _parse_text(text):
    print text
    friends = _get_friends(text)
    score = _get_score(text)
    user_id = db.create_user(username, score)
    for index, friend in enumerate(friends):
        record = _already_indexed(friend)
        if not record:
            record = db.create_user(friend)
            _queue(friend)
        _store(user_id, record, index + 1)


def get(username):
    """ Return a list of who this person follows"""
    print username
    r = _fetch(username)
    grequests.map([r])

if __name__ == "__main__":
    count = 0
    while len(SEEDS):
        POOL.wait_available()
        seed = SEEDS.pop()
        count += 1
        POOL.spawn(get, seed)
        POOL.join()
