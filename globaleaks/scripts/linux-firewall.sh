#/bin/sh

firewall_stop()
{
echo "Disabling GlobaLeaks Firewall... "
iptables -D INPUT -p tcp -d 127.0.0.1 --dport 8000  -s 127.0.0.1 -j ACCEPT
iptables -D INPUT -p tcp -d 127.0.0.1 --dport 8000  -j DROP
}

torrify_stop()
{
echo "Disabling GlobaLeaks Torrification..."
iptables -t nat -D OUTPUT ! -o lo -p tcp -m owner --uid-owner globaleaks -m tcp -j REDIRECT --to-ports 9040
iptables -t nat -D OUTPUT ! -o lo -p udp -m owner --uid-owner globaleaks -m udp --dport 53 -j REDIRECT --to-ports 53
iptables -t filter -D OUTPUT -p tcp -m owner --uid-owner globaleaks -m tcp --dport 9040 -j ACCEPT
iptables -t filter -D OUTPUT -p udp -m owner --uid-owner globaleaks -m udp --dport 53 -j ACCEPT
iptables -t filter -D OUTPUT ! -o lo -m owner --uid-owner globaleaks -j DROP
}


firewall_start()
{
echo "Enabling GlobaLeaks Firewall..."
# INBOUND
# Accept only connection from localhost (via Tor Hidden Service)
iptables -A INPUT -p tcp -d 127.0.0.1 --dport 8000  -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp -d 127.0.0.1 --dport 8000  -j DROP
}


torrify_start()
{
echo "Enabling GlobaLeaks Torrification..."
# OUTBOUND
# All outbound connections from GlobaLeaks goes trough Tor 
iptables -t nat -A OUTPUT ! -o lo -p tcp -m owner --uid-owner globaleaks -m tcp -j REDIRECT --to-ports 9040
iptables -t nat -A OUTPUT ! -o lo -p udp -m owner --uid-owner globaleaks -m udp --dport 53 -j REDIRECT --to-ports 53
iptables -t filter -A OUTPUT -p tcp -m owner --uid-owner globaleaks -m tcp --dport 9040 -j ACCEPT
iptables -t filter -A OUTPUT -p udp -m owner --uid-owner globaleaks -m udp --dport 53 -j ACCEPT
iptables -t filter -A OUTPUT ! -o lo -m owner --uid-owner globaleaks -j DROP
}
