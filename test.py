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

for remotePod in config.sections():
    if remotePod == localPod:
        continue

    local = diaspy.connection.Connection(
            pod = config[localPod]['scheme'] + '://' + localPod,
            username = config[localPod]['username'],
            password = config[localPod]['password'])
    remote = diaspy.connection.Connection(
            pod = config[remotePod]['scheme'] + '://' + remotePod,
            username = config[remotePod]['username'],
            password = config[remotePod]['password'])

    local.login()
    remote.login()

    localAspect = diaspy.models.Aspect(local, name='Testing')
    localUser = diaspy.people.User(local,
            handle = config[remotePod]['username'] + "@" + remotePod,
            fetch='data')
    try:
        localAspect.addUser(localUser['id'])
    except diaspy.errors.AspectError as e:
        print(e)
        if '500' in str(e):
            sys.exit(2)

    remoteAspect = diaspy.models.Aspect(remote, name='Testing')
    remoteUser = diaspy.people.User(remote,
            handle = config[localPod]['username'] + "@" + localPod,
            fetch='data')
    try:
        remoteAspect.addUser(remoteUser['id'])
    except diaspy.errors.AspectError as e:
        print(e)
        if '500' in str(e):
            sys.exit(2)

    seed = str(randint(100, 999))

    remoteStream = diaspy.streams.Stream(remote)
    remotePost = remoteStream.post(text="ping " + seed, aspect_ids=str(remoteAspect.id))

    localStream = diaspy.streams.Stream(local)
    localPost = localStream.post(text="ping " + seed, aspect_ids=str(localAspect.id))

    sleep(15)

    remoteStream.update()
    localStream.update()

    print("Search remoteStream")
    for post in remoteStream:
        if "ping " + seed in str(post) and post.author(key='id') == remoteUser['id']:
            print("Found ping in remoteStream")
            break

    print("Search localStream")
    for post in localStream:
        if "ping " + seed in str(post) and post.author(key='id') == localUser['id']:
            print("Found ping in localStream")
            break

    localPost.delete()
    remotePost.delete()
    local.logout()
    remote.logout()
