# coding: utf-8
import os
import re
import base64


def get_ngword_filepath():
    """ngwordのテキストファイルを返す

    >>> len(readfile(get_ngword_filepath())) > 0
    True
    """
    return os.path.join(os.path.dirname(__file__), "ngword.txt")


def readfile(path):
    """ファイルを読んで中身を返す
    """
    with open(path) as f:
        data = f.read()
    return data


def decode(text):
    return base64.b64decode(text).decode('utf-8')


def encode(text):
    return base64.b64encode(text.encode('utf-8'))


def make_patterns(text):
    """テキストからngwordの正規表現を作る

    >>> p = make_patterns(u"ほげ\\nふが")
    >>> p.search(u"あいうえおほげかきくけこ") is not None
    True
    >>> p.search(u"ほけ") is None
    True
    >>> p.search(u"ほげあいうえおふがかきくけこ") is not None
    True
    """
    words = text.strip().splitlines()
    patterns = re.compile(ur"(%s)+" % "|".join(words))
    return patterns


def main():
    ngword_raw = readfile(get_ngword_filepath())
    print(decode(ngword_raw))

if __name__ == '__main__':
    main()
