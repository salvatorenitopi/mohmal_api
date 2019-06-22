# Mohmal API

### Short Description
This is an UNOFFICIAL class that automates the interaction with the disposable mail service [Mohmal](https://www.mohmal.com/).

### Installation
mohmal_api requires [python](https://www.python.org/) v2+ to run.
To make it work you need to install the [requests](https://2.python-requests.org/en/master/) package.
```sh
$ pip install requests --user
```

### Quickstart
To implement this class in your script you just need to import it as follows:
```python
# -*- coding: utf-8 -*-

import mohmal_api as mohmal_api

obj = mohmal_api.mohmal_api()
```
Then you can use the instance as shown in the examples/ folder.


### UPDATE
A class for [Tempmail](https://temp-mail.org/) has been added. It works similarly, to implement it in your script you just need to import it as follows:
```python
# -*- coding: utf-8 -*-

import tempmail_api as tempmail_api

obj = tempmail_api.tempmail_api()
```
Then you can use the instance as shown in the examples/ folder (just change mohmal_api in tempmail_api).

### DISCLAIMER
This class was created to simplify the creation and management of a disposable mail address in a python script, please do not abuse it. Author assume no liability and are not responsible for any misuse or damage caused by this program.
