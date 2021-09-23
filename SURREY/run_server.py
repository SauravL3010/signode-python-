import sched, time
from server import server

import pymongo
from pymongo import MongoClient


cluster  = MongoClient("mongodb://127.0.0.1:27017/")

############## CLUSTER ######################
db = cluster["signode"]

############## COLLECTIONS(S) ######################
collection = db["surrey"]
collection_via = db["via"]
collection_vars = db["vars"]


s = sched.scheduler(time.time, time.sleep)

# Refresh Rate
sec = 5


def run_server(sc, sec):
    server(collection, collection_via, collection_vars)
    s.enter(sec, 1, run_server, (sc, sec))

s.enter(5, 1, run_server, (s, sec))
s.run()