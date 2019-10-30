# Stats_from_google_scholar

in this repo I implemented an automatic way of downloading defined statistics of a set of researchers
although the project scholarly (https://pypi.org/project/scholarly/) probably allows me to do the same I wanted
to find out a bit more regarding http requests and its implications.

get_stats_serial.py is waiting until each task(load webpage) is completed, and only after that proceeds with the new author.
this is a really straight forward was of dealing with this problem but has complexity O(N) this means that more authors I have
and more time I need.

This problem has a bottleneck in the speed which is the network, crawling the web is time expensive.

A method to avoid the system staying idle while the web server respond is to allow multple tasks to run simultaneously.

get_stats_parallel.py wants to exploit this strategy.


A proper timing sleep function must be setted inside each file in order to avoid rejection by the server.
if we are requesting informations too fast the server will answer always with an [Error 429 Too Many Requests].

the serial script is able to query at a speed of 0,7 researcher per second

the parallel script is currently not running, from a local machine pov should be able to outperform the previous example, but the server limit threshold must be respected.

# Recommended script for stats : get_stats_coroutine.py
# Recommended script for picts : get_picts.py
