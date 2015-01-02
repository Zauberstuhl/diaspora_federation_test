#! /usr/bin/python

import sys
import diaspy
from time import sleep
from random import randint

sechat = diaspy.connection.Connection(pod='https://sechat.org',
        username='user',
        password='s3cret')

zio = diaspy.connection.Connection(pod='https://diasp.org',
        username='user',
        password='secr3t')

sechat.login()
zio.login()

### pod one init

sechatAspect = diaspy.models.Aspect(sechat, name='Testing')
sechatUser = diaspy.people.User(sechat, handle='zio@diasp.org', fetch='data')

try:
    sechatAspect.addUser(sechatUser['id'])
except diaspy.errors.AspectError as e:
    print(e)
    if '500' in str(e):
        sys.exit(2)

### pod one end



### pod two init

zioAspect = diaspy.models.Aspect(zio, name='Testing')
zioUser = diaspy.people.User(zio, handle='sechat@sechat.org', fetch='data')

try:
    zioAspect.addUser(zioUser['id'])
except diaspy.errors.AspectError as e:
    print(e)
    if '500' in str(e):
        sys.exit(2)

### pod two end

seed = str(randint(100, 999))

zioStream = diaspy.streams.Stream(zio)
zioStream.post(text="ping " + seed, aspect_ids=str(zioAspect.id))

sechatStream = diaspy.streams.Stream(sechat)
sechatStream.post(text="ping " + seed, aspect_ids=str(sechatAspect.id))

sleep(10)

zioStream.update()
sechatStream.update()

print("Search zioStream")
for post in zioStream:
    if "ping " + seed in str(post) and post.author(key='id') == zioUser['id']:
        print("Found ping in zioStream")
        break

print("Search sechatStream")
for post in sechatStream:
    if "ping " + seed in str(post) and post.author(key='id') == sechatUser['id']:
        print("Found ping in sechatStream")
        break

sechat.logout()
zio.logout()
