#encoding=utf-8
#!/usr/bin/env python
__author__ = 'huangqingwei'

import sys
from pymongo import Connection
from django.conf import settings
import logging
from shard_redis import ShardJedis
import time

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

class MongoDAO(object):
    @staticmethod
    def newFromDjango():
        return MongoDAO(settings.MONGO_DATABASE)

    def __init__(self, config):
        self.config = config
        self.config['DBURL'] = 'mongodb://%s:%s/%s' % (self.config['HOST'], self.config['PORT'], self.config['NAME'])
        if self.config['USER']:
            self.config['DBURL'] = 'mongodb://%s:%s@%s:%s/%s' % (self.config['USER'], self.config['PASSWORD'],
                                                                 self.config['HOST'], self.config['PORT'],
                                                                 self.config['NAME'])

    def connect(self):
        conn = Connection(self.config['DBURL'])
        self.db = conn[self.config['NAME']]
        return self

    def getCollection(self, coll):
        self.coll = self.db[coll]
        return self.coll


class collection_dao(object):
    def __init__(self, conf):
        mongo = MongoDAO(conf).connect()
        self.mongo = mongo.getCollection('collection_name')

    def load_data(self):
        result_list = []
        for item in self.mongo.find({}, {"_id": 0}):
            result_list.append(item)
        logger.debug("finished to load mongo data, size:%d" % len(result_list))
        return result_list


#将dict序列化成redis中存放的格式
def serialize_dict(detail):
    result = "{\"id\":null,"
    for k, v in detail.iteritems():
        if type(v) is int:
            result += ("\"%s\":" % k) + ("%s" % v)
        else:
            result += ("\"%s\":" % k) + ("\"%s\"" % v)
        result += ","
    result = result[:len(result)-1]
    result += "}"
    return result


# convert isoDate 2012-11-26T07:45:16.632000 to integer 1353887116632
def isoToTimeStamp(iso_date):
    date_str = str(iso_date)
    date_head = date_str.split(".")[0]
    date_tail = date_str.split(".")[1] if len(date_str.split(".")) > 1 else 0
    time_stamp = int(time.mktime(time.strptime(date_head, "%Y-%m-%d %H:%M:%S"))) * 1000 + int(date_tail)/1000
    return time_stamp


#刷新feedback缓存
def refresh_redis(redis_servers, data_list):
    refresh_cnt = 0
    total_cnt = len(data_list)
    redis_client = ShardJedis(redis_servers)
    key_prefix = "_feedback_notify"
    for item in data_list:
        token = item['token']
        pkg = item['pkg']
        if not token or not pkg:
            continue
        key = "%s##%s##%s" % (key_prefix, token, pkg)
        if 'lastAccessTime' in item:
            item["lastAccessTime"] = isoToTimeStamp(item['lastAccessTime'])
        if 'modifiedTime' in item:
            item["modifiedTime"] = isoToTimeStamp(item['modifiedTime'])
        item["token"] = token
        item["pkg"] = pkg
        value = serialize_dict(item)
        redis_client.set(key, value)
        refresh_cnt += 1
        print ("refresh process : %d%%(%d/%d)\r" % (int(100.0*refresh_cnt/total_cnt), refresh_cnt, total_cnt)),
    print


if __name__ == "__main__":
    mongoConf = {'NAME': '', 'USER': '', 'PASSWORD': '', 'HOST': '127.0.0.1', 'PORT': '29017'}
    redisConf = ['127.0.0.1:6379', '127.0.0.1:6378']

    dao = collection_dao(mongoConf)
    data_list = dao.load_data()
    refresh_redis(redisConf, data_list)