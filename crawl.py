import random

from lxml import etree
import requests

BASE_URL = 'http://www.snapchat.com'
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.25 (KHTML, like Gecko) Version/6.0 Safari/536.25',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/23 Safari/536.5',
    'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
]
SEEDS = open('seeds').read().splitlines()


def _fetch(username):
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    r = requests.get("{}/{}".format(BASE_URL, username), headers=headers)
    r.raise_for_status()
    return r.text


def _parse(text):
    """ this is not the most robust function in the world """
    def _find_friends(child):
        link = child.find('.//a')
        return link.text

    html = etree.HTML(text)
    friends_div = html.find('.//div[@id="panel3"]')
    return [_find_friends(child) for child in friends_div.iterchildren()]


def _store(username, index):
    print username
    print index


def _already_indexed(username):
    return True


def _queue(username):
    pass


def get(username):
    """ Return a list of who this person follows"""
    text = _fetch(username)
    friends = _parse(text)
    for index, friend in enumerate(friends):
        _store(friend, index)
        if not _already_indexed(friend):
            _queue(friend)

if __name__ == "__main__":
    for seed in SEEDS:
        get(seed)
