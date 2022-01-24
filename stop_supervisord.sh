ps -ef | grep supervisord
#You will get some pid of supervisord just like these

#root 2641 12938 0 04:52 pts/1 00:00:00 grep --color=auto supervisord

#root 29646 1 0 04:45 ? 00:00:00 /usr/bin/python /usr/local/bin/supervisord

#if you get output like that, your pid is the second one. then if you want to shut down your supervisord you can do this

#kill -s SIGTERM 29646

