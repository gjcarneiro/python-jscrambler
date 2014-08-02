#! /bin/bash
function finish {
    killall nginx
}
trap finish EXIT

CWD=`pwd`
sed "s|@ROOT@|${CWD}/staticroot|" < nginx.conf.in > nginx.conf
nginx -c `pwd`/nginx.conf
gunicorn djangoscrambler.wsgi -b 127.0.0.1:8000

