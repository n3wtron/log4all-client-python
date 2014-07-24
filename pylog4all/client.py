import time

__author__ = 'Igor Maculan <n3wtron@gmail.com>'
import logging
import urllib
import json
import urllib2

log = logging.getLogger('log4all.client')


class Log4allClient(object):
    def __init__(self, host, proxy={}):
        self.host = host
        self.proxy = urllib2.ProxyHandler(proxy)
        urllib2.install_opener(urllib2.build_opener(self.proxy))

    def add_log(self, application, level, message, stack=None):
        data = json.dumps(dict(application=application, level=level, log=message, stack=stack))
        req = urllib2.Request(self.host + "/api/logs/add", data, {'Content-Type': 'application/json'})
        res = urllib2.urlopen(req)
        result = json.loads(res.read())
        return result['result'], result['message']

    def search_log(self, query, since, to, page=0, result_per_page=10, full=False):
        params = urllib.urlencode({
            'query': query,
            'dtSince': int(time.mktime(since.timetuple())),
            'dtTo': int(time.mktime(to.timetuple())),
            'page': page,
            'result_per_page': result_per_page,
            'full': full
        })
        url = self.host + "/api/logs/search?" + params
        log.info('calling ' + url)
        res = urllib2.urlopen(url)
        return json.load(res)

    def tail_log(self, query, since, full=False):
        params = urllib.urlencode({
            'query': query,
            'dtSince': int(time.mktime(since.timetuple())),
            'full': full
        })
        url = self.host + "/api/logs/tail?" + params
        log.debug('calling ' + url)
        res = urllib2.urlopen(url)
        return json.load(res)
