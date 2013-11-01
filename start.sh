#!/bin/sh

if [ "$(whoami)" != "root" ]; then
	echo "Run this script as root please"
	exit 1
fi

cd /home/nas/git/e2m

echo "Killing uWSGI instances.."
pkill uwsgi 2> /dev/null
sleep 1

echo "Starting uWSGI.."
uwsgi --socket 127.0.0.1:4242 --master -w e2m:app --processes 4 --threads 2 --die-on-term --daemonize /dev/null && echo "Successfully started uWSGI"

# It's probably not necessary to restart nginx,
# but we do it anyway
#echo "Restarting nginx.."
#service nginx restart && echo "Successfully restarted nginx" && echo "IndexConsole should now be up and running"
