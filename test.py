#! /usr/bin/python

import sys
import os.path
import diaspy
import configparser
from time import sleep
from random import randint

if len(sys.argv) != 2:
    print(sys.argv[0] + " <pod-you-want-to-test>")
    sys.exit(1)

if not os.path.isfile("config.ini"):
    print("Please create the 'config.ini' first!")
    sys.exit(1)

localPod = sys.argv[1]
config = configparser.ConfigParser()
config.read("config.ini")

def sendAndVerifyPost(pod1, pod2):
    print("Starting with " + pod1 + " > " + pod2)
    foundPost = False
    local = diaspy.connection.Connection(
            pod = config[pod1]['scheme'] + '://' + pod1,
            username = config[pod1]['username'],
            password = config[pod1]['password'])
    remote = diaspy.connection.Connection(
            pod = config[pod2]['scheme'] + '://' + pod2,
            username = config[pod2]['username'],
            password = config[pod2]['password'])

    local.login()
    remote.login()

    localAspect = diaspy.models.Aspect(local, name = config['global']['aspect'])
    localUser = diaspy.people.User(local,
            handle = config[pod2]['username'] + "@" + pod2,
            fetch='data')
    try:
        localAspect.addUser(localUser['id'])
    except diaspy.errors.AspectError as e:
        print("[" + pod1 + "] " + str(e))
        if '500' in str(e):
            sys.exit(2)

    remoteAspect = diaspy.models.Aspect(remote, name = config['global']['aspect'])
    remoteUser = diaspy.people.User(remote,
            handle = config[pod1]['username'] + "@" + pod1,
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

    print("Wait " + config['global']['timeout'] + " seconds to synchronize..")
    sleep(int(config['global']['timeout']))

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

    localPost.delete()
    local.logout()
    remote.logout()

for remotePod in config.sections():
    if remotePod == localPod or remotePod == "global":
        continue

    sendAndVerifyPost(localPod, remotePod)
    sendAndVerifyPost(remotePod, localPod)
