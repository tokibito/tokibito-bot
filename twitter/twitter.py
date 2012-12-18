# coding: utf-8
import tweepy


class OAuthHandler(tweepy.OAuthHandler):
    pass


class API(tweepy.API):
    pass


def get_oauth_handler(consumer_key, consumer_secret, access_token, access_token_secret):
    """OAuthハンドラを取得する関数
    """
    # OAuthのハンドラを生成
    handler = OAuthHandler(consumer_key, consumer_secret)
    # ハンドラにアクセストークンを設定
    handler.set_access_token(access_token, access_token_secret)
    return handler


def get_api_with_handler(handler):
    """TwitterAPIを取得する関数
    """
    return API(handler)
