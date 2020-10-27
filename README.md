# Introduction

This project is written using Python3 and tested on macOS environment. It is highly recommended to run this on linux/MacOS environment.

Flask is used as the web framework for the server and MongoDB is used for the database. 

# Installation
`MongoDB` needs to be installed first before running the server. The installation guide can be found [here](https://docs.mongodb.com/manual/administration/install-community/)

To run the server, launch a `terminal` and execute the following command. 
```
$ python3 server.py
```
You may be required to install some python modules that are used to run this script eg. pymongo, flask. You can use the python package manager `pip3 install <missing package>` to install the modules.

The server runs on `port:8082` and mongodb runs on `port:27017` by default.

# Testing
Unit tests are located under `tests` folder and can be executed by running `./runtests.sh`. Ensure that the **server is running before executing the testcases.**
