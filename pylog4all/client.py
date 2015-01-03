import time

__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import logging
import urllib
import json
import urllib2

_log = logging.getLogger('log4all.client')


class Log4allClientException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Log4allClient(object):
    def __init__(self, host, proxy={}):
        self.host = host
        self.proxy = urllib2.ProxyHandler(proxy)
        urllib2.install_opener(urllib2.build_opener(self.proxy))

    def add_log(self, application, level, message, stack=None):
        data = json.dumps(dict(application=application, level=level, message=message, stack=stack))
        req = urllib2.Request(self.host + "/api/logs/add", data, {'Content-Type': 'application/json'})
        res = urllib2.urlopen(req)
        result = json.loads(res.read())
        return result['success'], result['message']

    def search_log(self, query, since, to, page=0, result_per_page=10, full=False):
        params = {
            'query': query,
            'dt_since': int(time.mktime(since.timetuple()))*1000,
            'dt_to': int(time.mktime(to.timetuple()))*1000,
            'page': page,
            'max_result': result_per_page,
        }
        req = urllib2.Request(self.host + "/api/logs/search", json.dumps(params), {'Content-Type': 'application/json'})
        res = urllib2.urlopen(req)
        json_res = json.load(res)
        if not json_res['success']:
            raise Log4allClientException(json_res['message'])
        else:
            logs = json_res['result']
            if full:
                for log in logs:
                    if log.get('stack_sha') is not None:
                        stack_res = json.load(urllib2.urlopen(self.host+"/api/stack?sha="+log['stack_sha']))
                        log['stack'] = stack_res['stacktrace']
            return logs

    def tail_log(self, query, since, full=False):
        params = urllib.urlencode({
            'query': query,
            'dt_since': int(time.mktime(since.timetuple()))
        })
        req = urllib2.Request(self.host + "/api/logs/tail", json.dumps(params), {'Content-Type': 'application/json'})
        res = urllib2.urlopen(req)
        return json.load(res)
