# crawler-google-scholar ![](spider.png)

this repo presents an automatic way of downloading statistics of a set of researchers or professors from the google scholar.
giving as input a list of [name surname] of researchers it retrieves data from google scholar such as {# of publications, h-index, i10-index and others}

the project scholarly (https://pypi.org/project/scholarly/) probably allows me to do the same I wanted
to find out a bit more regarding http requests and its implications.

get_stats_serial.py is waiting until each task(load webpage of researcher X) is completed, and only after that proceeds with the new author (Y).
this simple approach comes with the expense of time complexity O(N), meaning as long as the amount of researcher is 'little' it won't require too much time.

This problem has a bottleneck in the speed which is the network, crawling the web is time expensive and the amount of request accepted by servers is limited and has to be respected.

A method to avoid the system staying idle while the web server responds is to allow multple tasks to run simultaneously.

get_stats_coroutine.py wants to exploit this strategy.

A proper timing sleep function must be setted inside each file in order to avoid rejection by the server.
if we are requesting informations too fast, the server will answer always with an [Error 429 Too Many Requests].

the serial script has been tested to query at a speed of 0,7 researcher per second
the coroutine script has been tested to query at a speed of 0.05 researcher per second

## Use
the input information must be an .xlsx file with two columns [surname, name]
- Run **get_stats_coroutine.py**
- output **stats.txt**

Recommended script for downloading stats : **get_stats_coroutine.py**


Recommended script for downloading profile images : **get_picts.py**



*image with the courtesy of icons8.com*


## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

**[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2021 © Francesco Vigni