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


def add(params):
    if len(sys.argv) < 3:
        print "Enter item to be added in your Zap list, followed by optional tag and priority"
        sys.exit(0)
    conn = sqlite3.connect("/tmp/zap.db")

    task_name = params[2]
    tag = "NA"
    priority = "normal"

    if len(sys.argv) == 4:
        option1 = params[3].split(':')
        if len(option1) < 2:
            print "Give options seperated by :"
            sys.exit(0)
        elif option1[0] == "tag":
            tag = option1[1]
        elif option1[0] == "priority":
            priority = option1[1]
        else:
            print "Enter either tag or priority as options"
            sys.exit(0)
    elif len(sys.argv) == 5:
        option1 = params[3].split(':')
        option2 = params[4].split(':')
        if len(option1) < 2 or len(option2) < 2:
            print "Give options seperated by :"
            sys.exit(0)
        if option1[0] == "tag":
            tag = option1[1]
        else:
            print "Enter either tag or priority as options"
            sys.exit(0)
        if option2[0] == "priority":
            priority = option2[1]
        else:
            print "Enter either tag or priority as options"
            sys.exit(0)
    elif len(sys.argv) > 5:
        print "Illegal Parameters"
        sys.exit(0)
    query_string = "INSERT INTO tasks (task,tag,priority,added_on) VALUES ('%s', '%s', '%s', CURRENT_TIMESTAMP);"%(task_name,tag,priority)
    conn.execute(query_string)
    print task_name, "added successfully to your Zap list :)"
    conn.commit()
    conn.close()



def show(params):
    if len(params) > 2:
        print "Illegal Parameters"
        sys.exit(0)
    else:
        conn = sqlite3.connect("/tmp/zap.db")
        cursor = conn.execute("SELECT * FROM tasks")
        for row in cursor:
            print "------------------------------------------------------------------------------"
            print row[0],"\t",row[1],"\t",row[2],"\t",row[3],"\t",row[4],"\n"
        conn.close()



def done(params):
    if len(params) == 2 or len(params) > 3:
        print "Illegal Parameters"
        sys.exit(0)
    else:
        params = params[2]
        params = params.split(',')
        conn = sqlite3.connect("/tmp/zap.db")
        for item in params:
            query_string = "DELETE from tasks where ID=%s"%int(item)
            cursor = conn.execute("DELETE from tasks where ID='%s'"%item)
            conn.commit()


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
        show(sys.argv)
    elif sys.argv[1] == "done":
        done(sys.argv)
    elif sys.argv[1] == "clean":
        clean()
    else:
        print "Illegal Parameters"
        print usage
        sys.exit(0)
