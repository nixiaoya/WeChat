#!/bin/env bash

hostname=`hostname`
date=`date +"%Y-%m-%d %H:%M:%S"`
uptime_since=$(date -d "`awk -F. '{print $1}' /proc/uptime` second ago" +"%Y-%m-%d %H:%M:%S")
users=`uptime | cut -d ',' -f 2`
cpu_load=`uptime | awk -F 'average:' '{print $NF}'`
total_mem=`free -m |awk 'NR==2{print $2}'`
used_mem=`free -m |awk 'NR==2{print $3}'`
free_mem=`free -m |awk 'NR==2{print $4}'`
disk_status=`df -lh | grep ^/`

echo "Hostname=${hostname};" 
echo "Cpu load=${cpu_load};"
echo "Memory(MB)=total-${total_mem}, used-${used_mem}, free-${free_mem};"
echo "Disk=${disk_status};"
echo "Users=${users};"
echo "Online since=${uptime_since};"
