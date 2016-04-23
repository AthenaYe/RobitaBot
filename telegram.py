#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
import requests
import config
import json
import jieba
import dispatcher
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Telegram():

    token = ''
    url = ''
    offset=0

    def __init__(self, token, url):
        self.token = token
        self.url = url
        self.coordinator = dispatcher.Dispatcher()
        return

    def recv_msg(self):
        print self.url + self.token + '/getUpdates?offset='+str(self.offset)
        while True:
            res = requests.post(self.url + self.token + '/getUpdates?offset='+str(self.offset), timeout=500)
            # if res.status_code == 200:
            #     print res.text
            #     print 'msg received!'
            if res is None:
                continue

            try:
                res = json.loads(res.text)
            except:
                print("Failed to parse json: %s" % res.text)
                continue

            if len(res['result']) == 0:
                continue

            print res
            print 'msg received!'

            for update in res["result"]:
                self.offset = update["update_id"] + 1
                jmsg = update["message"]
                msg = self.parse_jmsg(jmsg)
                self.send_msg(msg)
        return

    def send_msg(self, msg):
        content = msg['content']
        ret_msg = self.coordinator.dispatch(content)
        data = {
            'chat_id': msg['chat_id'],
            'text': ret_msg,
            'parse_mode': 'HTML',
        }
        print self.url + self.token + '/sendMessage?chat_id='+str(msg['chat_id']) + '&text='+ret_msg
        requests.post(self.url + self.token + '/sendMessage?chat_id='+str(msg['chat_id']) + '&text='+ret_msg)
        return

    def parse_jmsg(self, jmsg):
        msg_id = jmsg["message_id"]
        from_info = jmsg["from"]
        user_id, username = from_info["id"], from_info.get("username", "")
        chat_id = jmsg["chat"]["id"]
        ts = jmsg["date"]
        content = ''

        if "text" in jmsg:
            content = jmsg["text"]

        return {'msg_id':msg_id, 'user_id':user_id,
                'username':username, 'chat_id':chat_id,
                'content':content, 'date':ts}

if __name__ == '__main__':
    tele = Telegram(config.dict['token'], config.dict['telegram_url'])
    tele.recv_msg()

# vim: ts=4 sw=4 sts=4 expandtab
