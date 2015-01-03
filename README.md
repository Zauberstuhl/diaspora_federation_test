This is a really rough diaspora federation test!  
You need at least two pods. The script will create a post  
on pod A and try to reach it via pod B.

The script can handle multiple diaspora pod's. Just add more to the `config.ini`


Dependencies
------------

`sudo pip install configparser htmltemplate cherrypy`

`cd diaspy && sudo python setup.py install`

Setup
-----

`cp config.ini.example config.ini`

Adjust the configuration parameters.  
Create the aspect name configured in `config.ini` in every account!

Run it
------

`python test.py example.org`

The test script will also save the results to a sqlite database.  
You can run the start script for displaying the results nicly:

`python start.py`


Example
-------

If you check the following text for keywords like `Post found!` or `Post not found!`  
you can easily create a Nagios check or something similar.

    Starting with sechat.org > diasp.org
    [sechat.org] duplicate record, user already exists in aspect: 400
    [diasp.org] duplicate record, user already exists in aspect: 400
    [sechat.org] Create post..
    Wait 45 seconds to synchronize..
    [diasp.org] Fetch stream..
    [diasp.org] Search stream for new post..
    Post found!
    Starting with diasp.org > sechat.org
    [diasp.org] duplicate record, user already exists in aspect: 400
    [sechat.org] duplicate record, user already exists in aspect: 400
    [diasp.org] Create post..
    Wait 45 seconds to synchronize..
    [sechat.org] Fetch stream..
    [sechat.org] Search stream for new post..
    'ascii' codec can't encode character u'\xe4' in position 66: ordinal not in range(128)
    Post found!
