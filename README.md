# crawler-google-scholar ![](spider.png)

This repo presents an automatic way of downloading statistics of a set of researchers or professors from the google scholar.
giving as input a list of [name surname] of researchers it retrieves data from google scholar such as {# of publications, h-index, i10-index and others}

The project scholarly (https://pypi.org/project/scholarly/) allows to do something similar in a (way more structured way) but I wanted to find out a bit more regarding http requests and its implications.
Crawling the web is time expensive and the amount of request accepted by servers is limited and has to be respected!
A method to avoid the system staying idle while the web server responds is to allow multple tasks to run simultaneously.
The scripts here presented shows different ways of getting the same set of information.

## The scripts

`get_stats_serial.py` waits until each task(load webpage of researcher X) is completed, and only after that proceeds with the new author (Y). This simple approach comes with the expense of time complexity O(N), meaning as long as the amount of researcher is 'little' it won't require too much time.

`get_stats_coroutine.py` does not wait for researcher X to be downloaded and requests right away the next ones.

A proper timing sleep function must be setted inside each file in order to avoid rejection by the server. If we are requesting informations too fast, the server will answer always with an [Error 429 Too Many Requests].

### Performances
| Script      | Downloaded info per second |
| ----------- | ----------- |
| `get_stats_serial.py`      | 0.7       |
| `get_stats_coroutine.py`   | 0.05        |

## Use
The input information must be an .xlsx file with two columns [surname, name]
- Run **get_stats_coroutine.py**
- output **stats.txt**

Recommended script for downloading stats : **get_stats_coroutine.py**

Recommended script for downloading profile images : **get_picts.py**

*image with the courtesy of icons8.com*

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

**[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2023 © Francesco Vigni
