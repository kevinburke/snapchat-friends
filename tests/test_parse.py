import os

from nose.tools import assert_equal

import crawl

current_dir = os.path.join(os.path.dirname(__file__))
def test_parse():
    html = open('{}/test.html'.format(current_dir)).read()
    friends = crawl._parse(html)
    assert_equal(['turtleshelley', 'maxine', 'regulareng'], friends)
