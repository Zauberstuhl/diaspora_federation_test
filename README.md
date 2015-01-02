This is a really rough diaspora federation test!  
You need at least two pods. The script will create a post  
on pod A and try to reach it via pod B.

Dependencies
------------

`sudo pip install configparser`

`sudo python setup.py install`

Setup
-----

`cp config.ini.example config.ini`

Adjust the configuration parameters.  
Create the aspect name configured in `config.ini` in every account!

Run it
------

`python test.pl example.org`
