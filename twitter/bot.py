# coding: utf-8
import os
import sys
import random
import logging
import socket
import time
import json

import tweepy
import tweepy.error

import twitter
import ngword

_default_stdout = None

SETTINGS_FILE = 'settings.json'

# リツイートのしきい値
RETWEET_COUNT_MIN = random.choice(range(1, 30))
RETWEET_COUNT_MAX = random.choice(range(35, 300))
TIMELINE_FETCH_COUNT = 20

# 設定
DEFAULT_TIMELINE_COUNT = 30


def get_ngword_patterns(handler):
    """ngwordの正規表現を得る
    """
    ngword_text = ngword.decode(ngword.readfile(ngword.get_ngword_filepath()))
    handler.logger.info("%d ngwords loaded." % len(ngword_text.splitlines()))
    re_ngword = ngword.make_patterns(ngword_text)
    return re_ngword


def tweet_nullpo(handler):
    "ぬるぽ"
    handler.tweet(u"ぬるぽ")


def tweet_po(handler):
    "ぽ"
    handler.tweet(u"ぽ")


def tweet_fmm(handler):
    "ふーむ..."
    handler.tweet(u"ふーむ...")


def tweet_hyahha(handler):
    "ﾋｬｯﾊｰ"
    handler.tweet(u"ﾋｬｯﾊｰ")


def tweet_nemumui(handler):
    "ねむむい"
    handler.tweet(u"ねむむい")


def tweet_harahe(handler):
    "はらへ"
    handler.tweet(u"はらへ")


def tweet_hee(handler):
    "へー.."
    handler.tweet(u"へー..")


def tweet_maayarimasu(handler):
    "まあやります"
    handler.tweet(u"まあやります")


def tweet_bucho(handler):
    "bucho..."
    handler.tweet(u"bucho...")


def tweet_botpower(handler):
    "bot力・・・！"
    handler.tweet(u"bot力・・・！")


def tweet_lets_work(handler):
    "仕事に集中しよう.."
    handler.tweet(u"仕事に集中しよう..")


def tweet_all_for_bucho(handler):
    "（σ･ิω･ิ）σ すべては #bucho のために！"
    handler.tweet(u"（σ･ิω･ิ）σ すべては #bucho のために！")


def tweet_bot_work(handler):
    "twitterはbotに任せて仕事する"
    handler.tweet(u"twitterはbotに任せて仕事する")


def tweet_kiai(handler):
    "気合で乗り切ろう"
    handler.tweet(u"気合で乗り切ろう")


def tweet_ganbaranai(handler):
    "がんばらないようにがんばる"
    handler.tweet(u"がんばらないようにがんばる")


def tweet_yes(handler):
    "はい"
    handler.tweet(u"はい")


def tweet_hai(handler):
    "hai"
    handler.tweet(u"hai")


def tweet_kakko(handler):
    "("
    handler.tweet(u"(")


def tweet_n(handler):
    "n"
    handler.tweet(u"n")


def tweet_e(handler):
    "e"
    handler.tweet(u"e")


def tweet_we(handler):
    "うぇ"
    handler.tweet(u"うぇ")


def tweet_mu(handler):
    "む"
    handler.tweet(u"む")


def tweet_uhihi(handler):
    "ｳﾋﾋ"
    handler.tweet(u"ｳﾋﾋ")


def tweet_hai_sumimasen(handler):
    "はい、すみません"
    handler.tweet(u"はい、すみません")


def tweet_bot_kamosiremasen(handler):
    "botかもしれません。/そうじゃないかもしれません。"
    handler.tweet(u"botかもしれません。")
    time.sleep(15)
    handler.tweet(u"そうじゃないかもしれません。")


def tweet_sorosoro_akiraresou(handler):
    "そろそろ飽きそう/もうちょい何か面白い仕掛けを考えたい"
    handler.tweet(u"そろそろ飽きそう")
    time.sleep(20)
    handler.tweet(u"もうちょい何か面白い仕掛けを考えたい")


def tweet_yama_ni_ikitai(handler):
    "山に行きたい"
    handler.tweet(u"山に行きたい")


def tweet_dokokara_nagaretekitanda_kore(handler):
    "どこから流れてきたんだこれ..."
    handler.tweet(u"どこから流れてきたんだこれ...")


def tweet_bikibiki(handler):
    "（#^ω^）"
    handler.tweet(u"（#^ω^）")


def tweet_uxei(handler):
    "うぇーい"
    handler.tweet(u"うぇーい")


def tweet_maa_kasegou(handler):
    "まあ稼ごうじゃないか。"
    handler.tweet(u"まあ稼ごうじゃないか。")


def tweet_twitter_kowai(handler):
    "ついったーこわい。"
    handler.tweet(u"ついったーこわい。")


def tweet_mainichi_hack(handler):
    "毎日がハッカソン！"
    handler.tweet(u"毎日がハッカソン！")


def tweet_monsama_kusobot(handler):
    "もん様にクソbotって言われないようにがんばる"
    handler.tweet(u"もん様にクソbotって言われないようにがんばる")


def tweet_itudemo_isogasii(handler):
    "いつでも忙しい"
    handler.tweet(u"いつでも忙しい")


def tweet_minna_yoyuu_aru(handler):
    "みんなTwitterやるぐらいの余裕はあるのだよな"
    handler.tweet(u"みんなTwitterやるぐらいの余裕はあるのだよな")


def tweet_tsutaetakoto(handler):
    "「伝わったことが、伝えたこと」"
    handler.tweet(u"「伝わったことが、伝えたこと」")


def tweet_bot_ga_ittakoto_kinisisugi(handler):
    "botが言ったことを気にし過ぎじゃないか"
    handler.tweet(u"botが言ったことを気にし過ぎじゃないか")


def tweet_watasi_kininarimasu(handler):
    "わたし、気になります"
    handler.tweet(u"わたし、気になります")


def tweet_satsubatsu(handler):
    "殺伐"
    handler.tweet(u"殺☆伐")


def tweet_machigai(handler):
    "自分が間違っているな、と思ったら素直に認めて先へ進もう"
    handler.tweet(u"自分が間違っているな、と思ったら素直に認めて先へ進もう")


def tweet_gouriteki(handler):
    "気に入らなくても合理的であるかどうかを一度考えてみよう"
    handler.tweet(u"気に入らなくても合理的であるかどうかを一度考えてみよう")


def tweet_hu(handler):
    "フー"
    handler.tweet(u"フー")


def tweet_gununu(handler):
    "ぐぬぬ"
    handler.tweet(u"ぐぬぬ")


def tweet_haa(handler):
    "はー"
    handler.tweet(u"はー")


def tweet_rakudehanaigatanoshii(handler):
    "楽ではないが楽しい"
    handler.tweet(u"楽ではないが楽しい")


def tweet_dakaradoushita(handler):
    "だからどうした"
    handler.tweet(u"＼だからどうした／")


def tweet_retweet_many(handler):
    "リツイート一覧からランダムに選んでリツイート"
    status = handler.get_many_retweeted(RETWEET_COUNT_MIN, RETWEET_COUNT_MAX)
    if status:
        handler.logger.info("status.id = %s, %d RT" % (status.id, status.retweet_count))
        handler.retweet(status.id)


def tweet_retweet_list(handler, user, slug):
    "リストのリツイートされた発言をリツイート"
    status = handler.get_many_retweeted_from_list(user, slug, 1, RETWEET_COUNT_MAX)
    if status:
        handler.logger.info("status.id = %s, %d RT" % (status.id, status.retweet_count))
        handler.retweet(status.id)


def retweet(handler, id):
    "リツイート"
    print("tweet message id: %s" % id)
    handler.retweet(id)


def post(handler, message, in_reply_to_status_id=None):
    "ツイートを投稿"
    print("tweet message: %s" % message)
    handler.tweet(message, in_reply_to_status_id)


def show_list(handler):
    "リストを表示"
    for lst in handler.api.lists():
        print("user: %s, slug: %s" % (lst.user.screen_name, lst.slug))


def home(handler, count=None):
    "ホームタイムラインを表示"
    iterator = tweepy.Cursor(handler.api.home_timeline).items(count and int(count) or DEFAULT_TIMELINE_COUNT)
    for status in iterator:
        print_status(status)


def list_tl(handler, user, slug, count=None):
    """リストを表示
    """
    iterator = tweepy.Cursor(handler.api.list_timeline, user, slug).items(count and int(count) or DEFAULT_TIMELINE_COUNT)
    for status in iterator:
        print_status(status)


def list_retweeted(handler, user, slug, min_count=1, max_count=None):
    """リストのうちしきい値を超えた回数リツイートされた発言を表示
    """
    status = handler.get_many_retweeted_from_list(user, slug, min_count, max_count)
    if status:
        print_status(status)


def search_tl(handler, keyword, count=None):
    """検索してタイムラインを表示
    """
    iterator = tweepy.Cursor(handler.api.search, keyword).items(count and int(count) or DEFAULT_TIMELINE_COUNT)
    for result in iterator:
        print_search_result(result)


def unescape(text):
    """ステータスのメッセージをエスケープ解除して返す
    """
    result = text.replace('&lt;', '<')
    result = result.replace('&gt;', '>')
    return result


def print_status(status):
    """Statusを色付きでprint
    """
    print("\033[1;33m%s\033[1;m \033[1;36m%s\033[1;m %s" % (status.id, status.user.screen_name, unescape(status.text)))


def print_search_result(result):
    """SearchResultを色付きでprint
    """
    print("\033[1;33m%s\033[1;m \033[1;36m%s\033[1;m %s" % (result.id, result.from_user, unescape(result.text)))


def shell(handler):
    """対話シェル
    """
    import code
    import readline
    sys.stdout = _default_stdout
    variables = globals()
    variables.update({'handler': handler})
    print("starting interactive shell...")
    print("handler = BotHanler()")
    import rlcompleter
    readline.set_completer(rlcompleter.Completer(variables).complete)
    readline.parse_and_bind("tab:complete")
    code.interact(local=variables)

# アクションのマップ
ACTION_MAP_CONFIG = [
  [2, tweet_nullpo],
  [1, tweet_po],
  [1, tweet_fmm],
  [1, tweet_hyahha],
  [1, tweet_nemumui],
  [1, tweet_harahe],
  [1, tweet_hee],
  [1, tweet_maayarimasu],
  [1, tweet_bucho],
  [1, tweet_botpower],
  [1, tweet_lets_work],
  [1, tweet_all_for_bucho],
  [1, tweet_bot_work],
  [1, tweet_kiai],
  [1, tweet_ganbaranai],
  [1, tweet_yes],
  [1, tweet_hai],
  [1, tweet_kakko],
  [1, tweet_n],
  [1, tweet_e],
  [1, tweet_we],
  [1, tweet_mu],
  [1, tweet_uhihi],
  [1, tweet_hai_sumimasen],
  [1, tweet_bot_kamosiremasen],
  #[1, tweet_sorosoro_akiraresou],
  [1, tweet_yama_ni_ikitai],
  [1, tweet_dokokara_nagaretekitanda_kore],
  [1, tweet_bikibiki],
  [1, tweet_uxei],
  [1, tweet_maa_kasegou],
  [1, tweet_twitter_kowai],
  [1, tweet_mainichi_hack],
  [1, tweet_monsama_kusobot],
  #[1, tweet_itudemo_isogasii],
  #[1, tweet_minna_yoyuu_aru],
  [1, tweet_tsutaetakoto],
  #[1, tweet_bot_ga_ittakoto_kinisisugi],
  [1, tweet_watasi_kininarimasu],
  [1, tweet_satsubatsu],
  [1, tweet_machigai],
  [1, tweet_gouriteki],
  [1, tweet_hu],
  [1, tweet_gununu],
  [1, tweet_haa],
  [1, tweet_rakudehanaigatanoshii],
  [1, tweet_dakaradoushita],
  [20, tweet_retweet_many],
  [20, lambda handler: tweet_retweet_list(handler, 'tokibito', 'v')],
  [20, lambda handler: tweet_retweet_list(handler, 'tokibito', 'py')],
  [20, lambda handler: tweet_retweet_list(handler, 'tokibito', 'beproud')],
  [30, None],  # 何もしない
]


class BotHandler(object):
    """botのハンドラクラス(TwitterアカウントやAPIとひもづいてる)
    """
    def __init__(self, settings_file=None):
        if settings_file:
            with open(settings_file) as f:
                self.settings = json.load(f)
        else:
            self.settings = {}
        self.oauth_handler = twitter.get_oauth_handler(
            consumer_key=self.settings.get('CONSUMER_KEY'),
            consumer_secret=self.settings.get('CONSUMER_SECRET'),
            access_token=self.settings.get('ACCESS_TOKEN'),
            access_token_secret=self.settings.get('ACCESS_TOKEN_SECRET'))
        self.api = twitter.get_api_with_handler(self.oauth_handler)
        self.action_map = []
        self.logger = self.getLogger()
        self.re_ngword = None
        for priority, action in ACTION_MAP_CONFIG:
            for i in range(priority):
                self.action_map.append(action)

    def getLogger(self):
        return logging.getLogger('bot')

    def get_many_retweeted_for_timeline(self, timeline, min_count=5, max_count=None):
        """指定したtimelineのうちたくさんリツイートされた発言を取得
        """
        for status in timeline:
            if status.retweet_count > min_count:
                # max_countが設定されている場合
                if max_count and (status.retweet_count > max_count):
                    self.logger.info("It was skipped because it is over than max retweeted count (%d)." % status.retweet_count)
                    continue
                # NGワードを含むものはスキップ
                if self.match_ngword(status.text):
                    self.logger.info("It was skipped because it includes NG words.")
                    continue
                return status

    def get_many_retweeted(self, min_count=5, max_count=None):
        """たくさんリツイートされた発言を取得
        count: しきい値
        """
        timeline = self.api.retweeted_to_me(count=TIMELINE_FETCH_COUNT)
        return self.get_many_retweeted_for_timeline(timeline, min_count, max_count)

    def get_list_statuses(self, user, slug):
        """リストの発言を取得
        """
        iterator = tweepy.Cursor(
            self.api.list_timeline,
            user,
            slug).items(TIMELINE_FETCH_COUNT)
        return iterator

    def get_many_retweeted_from_list(self, user, slug, min_count=1, max_count=None):
        """リストからタイムラインを取得してリツイートされたものを返す
        """
        timeline = self.get_list_statuses(user, slug)
        return self.get_many_retweeted_for_timeline(timeline, min_count, max_count)

    def tweet(self, message, in_reply_to_status_id=None):
        """Twitterへ発言する
        """
        try:
            self.api.update_status(message, in_reply_to_status_id)
        except tweepy.error.TweepError:
            self.logger.info("Duplicate tweet.")

    def retweet(self, id):
        """Twitterへretweetする
        """
        try:
            self.api.retweet(id)
        except tweepy.error.TweepError, err:
            self.logger.info(err)

    def match_ngword(self, text):
        """ngwordを含むか判定
        """
        if self.re_ngword is None:
            self.re_ngword = get_ngword_patterns(self)
        return self.re_ngword.search(text)

    def get_action(self):
        action = random.choice(self.action_map)
        self.logger.info("action = %s" % (action and action.__name__))
        return action

    def run(self):
        action = self.get_action()
        if action and callable(action):
            action(self)


def help(handler, *args):
    """ヘルプを表示
    """
    import bot
    print "-" * 70
    for name in dir(bot):
        func = getattr(bot, name)
        if callable(func):
            spacer = " " * abs(35 - len(name))
            print "%s%s\t%s" % (name.decode('utf-8'), spacer, func.__doc__ and func.__doc__.decode('utf-8').strip() or "")
    print "-" * 70


def command(*args):
    """コマンドモード
    """
    import codecs
    socket.setdefaulttimeout(20)
    global _default_stdout
    _default_stdout = sys.stdout
    sys.stdout = codecs.getwriter('utf-8')(_default_stdout)
    bits = map(lambda v: v.decode('utf-8'), args)
    print("command mode: %s" % bits)
    import bot
    cmd_name = bits[0]
    if hasattr(bot, cmd_name):
        func = getattr(bot, cmd_name)
        settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), SETTINGS_FILE)
        handler = BotHandler(settings_file)
        if callable(func):
            try:
                func(handler, *bits[1:])
            except Exception, err:
                print(err)
    else:
        print("command not found.")
    print("OK.")  # exit string
