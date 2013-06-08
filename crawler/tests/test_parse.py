import os

from nose.tools import assert_equal

import crawl

current_dir = os.path.join(os.path.dirname(__file__))
def test_friends():
    html = open('{}/test.html'.format(current_dir)).read()
    friends = crawl._get_friends(html)
    assert_equal(['turtleshelley', 'maxine', 'regulareng'], friends)

def test_score():
    html = open('{}/test.html'.format(current_dir)).read()
    score = crawl._get_score(html)
    assert_equal(32428, score)
