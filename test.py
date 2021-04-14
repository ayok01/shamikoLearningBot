#! /usr/bin/env python
# -*- coding: utf-8 -*-
from mastodon import Mastodon

#mstdn = Mastodon(client_id="client_id.txt",api_base_url="https://machikadon.online");
#mstdn.log_in(username="arakakiyutaro.0204@gmail.com",password="",to_file="access_token.txt");

#url = 'https://machikadon.online'
#cid_file = 'client_id.txt'
#token_file = 'access_token.txt'
#
#mstdn = Mastodon(client_id=cid_file ,access_token=token_file ,api_base_url=url)
#
#mastodon = Mastodon(
#    client_id=cid_file,
#    access_token=token_file,
#    api_base_url=url
#)
#
#mastodon.status_post("zlzz",visibility='unlisted') #ここを変える


#アプリケーションの登録
#Mastodon.create_app(client_name = "MyApp",            #アプリケーション名
#                    api_base_url= "https://machikadon.online", #アクセス先
#                    to_file = "client_id.txt")       #client idとclient secretの出力先

mastodon = Mastodon(client_id="client_id.txt",       #client idとclient secretを出力したファイル
                    api_base_url="https://machikadon.online")  #アクセス先

#ユーザー認証
mastodon.log_in(username="arakakiyutaro.0204@gmail.com",    #登録したメールアドレス
                password="Wacom0204@",            #設定したパスワード
                to_file="access_token.txt")  #アクセストークン出力先