��ȡ��������IP��curl ifconfig.me

��¼ftp������
lftp ftp://username:password@host:port

#����ɾ��
./redis-cli -h 127.0.0.1 -n 1 keys 'oh:1:payment:7d742f3be61c4c8a84f6fd05928c7d014d4bed9e:*'|awk '{cmd="./redis-cli -h 127.0.0.1 -n 1 del \"" $0 "\""; system(cmd);}'
#����ˢ��(setex�﷨��setex key, expireTime, value)
cat ~/datas | awk '{cmd="./redis-cli -h 127.0.0.1 -p 6379 -n 1 setex "$0" 60 4"; system(cmd);}'