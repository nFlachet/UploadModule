#!/bin/sh
# chkconfig: 123456 90 10
# Tornado Server for ecodistrict uploader
#
workdir=/home/cstb/ecodistrict/FileHandlerService/

start() {
    cd $workdir
    /usr/bin/python /home/cstb/ecodistrict/FileHandlerService/UploadForm.py &
    echo "Server started."
}

stop() {
    pid=`ps -ef | grep '[p]ython /home/cstb/ecodistrict/FileHandlerService/UploadForm.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: /etc/init.d/ecodistrict {start|stop|restart}"
    exit 1
esac
exit 0