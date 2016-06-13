#!/usr/bin/env bash

PROVISIONING_DIR='/vagrant/provisioning'

echo "** Adding Apt Mirrors **"
echo "$(echo deb mirror://mirrors.ubuntu.com/mirrors.txt wily main restricted universe multiverse | cat - /etc/apt/sources.list)" > /etc/apt/sources.list
echo "$(echo deb mirror://mirrors.ubuntu.com/mirrors.txt wily-updates main restricted universe multiverse | cat - /etc/apt/sources.list)" > /etc/apt/sources.list
echo "$(echo deb mirror://mirrors.ubuntu.com/mirrors.txt wily-backports main restricted universe multiverse | cat - /etc/apt/sources.list)" > /etc/apt/sources.list
echo "$(echo deb mirror://mirrors.ubuntu.com/mirrors.txt wily-security main restricted universe multiverse | cat - /etc/apt/sources.list)" > /etc/apt/sources.list

echo "** Disabling IPv6 **"
echo 'precedence ::ffff:0:0/96 100' >> /etc/gai.conf
echo "#disable ipv6" | tee -a /etc/sysctl.conf
echo "net.ipv6.conf.all.disable_ipv6 = 1" | tee -a /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 1" | tee -a /etc/sysctl.conf
echo "net.ipv6.conf.lo.disable_ipv6 = 1" | tee -a /etc/sysctl.conf
sysctl -p


# Upgrade System
echo "** Upgrade System **"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" -y -f dist-upgrade


echo "** Start Provisioning Script **"
$PROVISIONING_DIR/provision.sh
