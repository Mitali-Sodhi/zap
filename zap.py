#!/usr/bin/python

import sys
import os
import sqlite3
from colorama import Fore
from prettytable import PrettyTable


def start():
    if os.path.isfile("/tmp/zap.db"):
        print "Your Zap list already intialized. Use 'zap add' to add new tasks"
    else:
        conn = sqlite3.connect("/tmp/zap.db")
        conn.execute('''CREATE TABLE tasks (id INTEGER PRIMARY KEY , task TEXT NOT NULL, tag TEXT NOT NULL, priority TEXT NOT NULL, added_on TIMESTAMP);''')
        conn.close()
        print "Zap list initialized successfully! Use 'zap add' to add new tasks"


def add(params):
    if len(sys.argv) < 3:
        print "Enter item to be added in your Zap list, followed by optional tag and priority"
        sys.exit(0)

    if os.path.isfile("/tmp/zap.db"):
        conn = sqlite3.connect("/tmp/zap.db")
    else:
        print "Your Zap list is not initialized. Use 'zap start' to get started"
        sys.exit(0)

    task_name = params[2]
    tag = "NA"
    priority = "normal"

    if len(params) == 4:
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
    elif len(params) == 5:
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
        print usage
        sys.exit(0)

    query_string = "INSERT INTO tasks (task,tag,priority,added_on) VALUES ('%s', '%s', '%s', CURRENT_TIMESTAMP);" % (task_name, tag, priority)
    conn.execute(query_string)
    print task_name, "added successfully to your Zap list :)"
    conn.commit()
    conn.close()


def show(params):
    if len(params) > 2:
        print "Wrong Parameters"
        print usage
        sys.exit(0)
    else:
        conn = sqlite3.connect("/tmp/zap.db")
        cursor = conn.execute("SELECT * FROM tasks")
        data = cursor.fetchall()
        if len(data) == 0:
            print "Your Zap list is empty. Add a new list by zap add <task> <tag> <priority>"
        else:
            output_table = PrettyTable()
            output_table.field_names = ["#", "Task", "Tag", "Priority", "Added On"]
            for row in data:
                if row[3] == "high":
                    output_table.add_row([row[0], row[1], row[2], (Fore.RED + row[3]), row[4]])
                elif row[3] == "normal":
                    output_table.add_row([row[0], row[1], row[2], (Fore.YELLOW + row[3]), row[4]])
                elif row[3] == "low":
                    output_table.add_row([row[0], row[1], row[2], (Fore.GREEN + row[3]), row[4]])
            print output_table
        conn.close()


def done(params):
    if len(params) == 2 or len(params) > 3:
        print "Wrong Parameters"
        print usage
        sys.exit(0)
    else:
        params = params[2]
        params = params.split(',')
        conn = sqlite3.connect("/tmp/zap.db")
        for item in params:
            if item.isdigit():
                query_string = "DELETE from tasks where ID=%s" % int(item)
                conn.execute(query_string)
                conn.execute("DELETE from sqlite_sequence where name='tasks'")
                conn.commit()
                print item, "successfully deleted from your Zap list"
            else:
                query_string = "DELETE from tasks where task='%s'" % item
                conn.execute(query_string)
                conn.execute("DELETE from sqlite_sequence where name='tasks'")
                conn.commit()
                print item, "successfully deleted from your Zap list"
        conn.close()


def clean(params):
    if len(params) > 2:
        print "Wrong Parameters."
        print usage
        sys.exit(0)
    else:
        confirmation = raw_input("Are you sure (y/n)?\t")
        if confirmation.lower().startswith("y"):
            conn = sqlite3.connect("/tmp/zap.db")
            conn.execute("DELETE from tasks")
            conn.execute("DELETE from sqlite_sequence where name='tasks'")
            conn.commit()
            conn.close()
            print "Cleaned up your Zap list! Use 'zap add' to add new tasks"


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
        clean(sys.argv)
    else:
        print "Illegal Parameters"
        print usage
        sys.exit(0)
