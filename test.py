#! /usr/bin/python

import sys
import os.path
import diaspy
import sqlite3

from time import sleep
from random import randint
from lib import config

c = config.Config().load()

def sendAndVerifyPost(pod1, pod2):
    print("Starting with " + pod1 + " > " + pod2)
    foundPost = False
    local = diaspy.connection.Connection(
            pod = c[pod1]['scheme'] + '://' + pod1,
            username = c[pod1]['username'],
            password = c[pod1]['password'])
    remote = diaspy.connection.Connection(
            pod = c[pod2]['scheme'] + '://' + pod2,
            username = c[pod2]['username'],
            password = c[pod2]['password'])

    local.login()
    remote.login()

    localAspect = diaspy.models.Aspect(local, name = c['global']['aspect'])
    localUser = diaspy.people.User(local,
            handle = c[pod2]['username'] + "@" + pod2,
            fetch='data')
    try:
        localAspect.addUser(localUser['id'])
    except diaspy.errors.AspectError as e:
        print("[" + pod1 + "] " + str(e))
        if '500' in str(e):
            sys.exit(2)

    remoteAspect = diaspy.models.Aspect(remote, name = c['global']['aspect'])
    remoteUser = diaspy.people.User(remote,
            handle = c[pod1]['username'] + "@" + pod1,
            fetch='data')
    try:
        remoteAspect.addUser(remoteUser['id'])
    except diaspy.errors.AspectError as e:
        print("[" + pod2 + "] " + str(e))
        if '500' in str(e):
            sys.exit(2)

    seed = str(randint(100, 999))
    localStream = diaspy.streams.Stream(local)
    print("[" + pod1 + "] Create post..")
    localPost = localStream.post(text="ping " + seed, aspect_ids=str(localAspect.id))

    print("Wait " + c['global']['timeout'] + " seconds to synchronize..")
    sleep(int(c['global']['timeout']))

    print("[" + pod2 + "] Fetch stream..")
    remoteStream = diaspy.streams.Stream(remote)

    print("[" + pod2 + "] Search stream for new post..")
    for post in remoteStream:
        try:
            if "ping " + seed in str(post): # and str(post.author(key='id')) == str(localUser['id']):
                foundPost = True
                break
        except UnicodeEncodeError as e:
            print(e)

    if foundPost:
        print("Post found!")
    else:
        print("Post not found!")

    with sqlite3.connect(c['global']['database_path']) as con:
        rowid = 0 # initialize
        cursor = con.cursor()
        cursor.execute("SELECT ROWID FROM pod WHERE podName LIKE '" + pod1 + "'")
        data = cursor.fetchone()
        if data is None:
            cursor.execute("INSERT INTO pod VALUES ('" + pod1 + "', CURRENT_TIMESTAMP)")
            rowid = cursor.lastrowid
        else:
            rowid = int(data[0])

        con.execute("INSERT INTO federation VALUES (?, ?, ?, ?)",
                [rowid, pod1, pod2, foundPost])

    localPost.delete()
    local.logout()
    remote.logout()

with sqlite3.connect(c['global']['database_path']) as con:
    plainSQL = open(c['global']['database_scheme']).read()
    con.executescript(plainSQL)

for localPod in c.sections():
    if localPod == "global": continue
    for remotePod in c.sections():
        if remotePod == localPod or remotePod == "global":
            continue

        try: sendAndVerifyPost(localPod, remotePod)
        except diaspy.errors.StreamError as e:
            print(e)
