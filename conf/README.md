supervisor must be placed in /etc/init.d/  \
supervisord.conf must be placed in /etc/supervisor/ \
dht22.conf must be placed in /etc/supervisor/conf.d/ 

then run 

sudo chmod +x /etc/init.d/supervisord \
sudo update-rc.d supervisord defaults 

see: https://serverfault.com/questions/96499/how-to-automatically-start-supervisord-on-linux-ubuntu 

