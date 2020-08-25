#!/usr/bin/env python3
import sys,os
import pathlib
import configparser
import urllib.request
import json
import time

def loadconf ():
    global token, webhook, webhook_dev

    cfg = configparser.ConfigParser ()
    cfg_file = os.path.dirname(__file__) + '/config.ini'
    cfg.read (cfg_file)
    token = cfg['slack']['token']
    webhook = cfg['slack']['webhook']
    return 0

class Exec_api:
    def exec (self, req):
        """
        explanation:
            exec Slack API
        Args:
            req: urllib request object
        Return:
            body: Json object (dict)

        正常に完了した場合は Responsbody(json) を返す
        失敗した場合は、エラーjson(dict) を返す
        {"ok": false, "err":{"code": $err.code, "reason": $err.reason}}
        """
        body = {"ok": False}

        try:
            with urllib.request.urlopen(req) as res:
                body = json.loads(res.read().decode('utf-8'))
        except urllib.error.HTTPError as err:
            time.sleep (61)
            try:
                with urllib.request.urlopen(req) as res:
                    body = json.loads(res.read().decode('utf-8'))
            except urllib.error.HTTPError as err:
                err_d = {'reason': str(err.reason), 'code': str(err.code)}
                body = {'ok': False, 'err':err_d}

        except urllib.error.URLError as err:
            time.sleep (11)
            try:
                with urllib.request.urlopen(req) as res:
                    body = json.loads(res.read().decode('utf-8'))
            except urllib.error.URLError as err:
                err_d = {'reason': str(err.reason)}
                res = {'ok': False, 'err':err_d}

        return body

class Api:
    def api_test (self):
        """
        # GET
        https://api.slack.com/methods/api.test
        """
        url = "https://slack.com/api/api.test"

        req = urllib.request.Request (url)
        api = Exec_api ()
        body = api.exec (req)
        return body

    def auth_test (self):
        """
        # POST
        https://api.slack.com/methods/auth.test
        """
        url = "https://slack.com/api/auth.test"
        params = {
            'token': token,
        }

        req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
        api = Exec_api ()
        body = api.exec (req)
        return body

def main ():

    loadconf ()
    print (f'{token=}')
    print (f'{webhook=}')

    api = Api ()
    print ("== api.test ==")
    res = api.api_test ()
    print (json.dumps(res, indent=4))

    print ("== auth.test ==")
    res = api.auth_test ()
    print (json.dumps(res, indent=4))

if __name__ == '__main__':
    main ()
    exit (0)
