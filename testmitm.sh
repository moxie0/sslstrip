#!/bin/sh
# by Krzysztof Kotowicz <kkotowicz at gmail dot com>
if [ "$1" = "start" ]; then
   echo "Accepting port 80 packets from user UID $2"
   iptables -t nat -A OUTPUT -p tcp -m owner --uid-owner $2 -j ACCEPT
   echo "Forwarding other port 80 packets to port 10000"
   iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-port 10000

elif [ "$1" = "stop" ]; then
    echo "Flushing MITM rules"
    iptables -t nat -F
    iptables -t nat -X
else
    echo "Usage: "
    echo ""
    echo "$0 start <uid>"
    echo " MITM all port 80 connections in sslstrip run by user <uid>"
    echo ""
    echo "$0 stop"
    echo " Stop MITM"
    echo ""
fi
