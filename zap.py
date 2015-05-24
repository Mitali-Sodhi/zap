#!/usr/bin/python

import sys
import os
import sqlite3


def start():
    if os.path.isfile("/tmp/zap.db"):
        print "Your Zap list already intialized. Use 'zap add' to add new tasks"
    else:
        conn = sqlite3.connect("/tmp/zap.db")
        conn.execute('''CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, tag TEXT NOT NULL, priority TEXT NOT NULL, added_on TIMESTAMP);''')
        conn.close()
        print "Zap list initialized Successfully. Use 'zap add' to add new tasks"


def add():
    raise NotImplementedError


def show():
    raise NotImplementedError


def done():
    raise NotImplementedError


def clean():
    raise NotImplementedError


if __name__ == '__main__':
    usage = '''\nUsage: zap start/add/show/done/clean <params> \n'''

    if len(sys.argv) < 2:
        print usage
        sys.exit(0)

    if sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "add":
        add(sys.argv)
    elif sys.argv[1] == "show":
        show()
    elif sys.argv[1] == "done":
        done(sys.argv)
    elif sys.argv[1] == "clean":
        clean()
    else:
        print "Illegal Parameters"
        print usage
        sys.exit(0)
