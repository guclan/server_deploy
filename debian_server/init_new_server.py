# !/usr/bin/python
# -*- encoding:utf-8 -*-

import commands
import sys

YES = ("Y", "y", "YES", "yes")


def setup_bbr():
    res = raw_input("Install tcp_bbr for your server ? (Y/N)")
    if res not in YES:
        return False
    k_ver = commands.getoutput('uname -r').split(".")
    if not (int(k_ver[0]) > 4 or (int(k_ver[0]) == 4 and int(k_ver[1] >= 9))):
        print("Linux Kernal Version is lower.")
        return False
    exist_bbr = commands.getoutput('lsmod |grep bbr')
    if "tcp_bbr" in exist_bbr:
        print("TCP bbr is available.")
        return False
    load_bbr = commands.getoutput('modprobe tcp_bbr')
    if load_bbr == "modprobe: FATAL: Module tcp_bbr not found.":
        print("System no module named bbr.")
        return False
    commands.getoutput('echo "tcp_bbr" >> /etc/modules-load.d/modules.conf')
    commands.getoutput('echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf')
    commands.getoutput('echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf')
    commands.getoutput('sysctl -p')
    commands.getoutput('sysctl net.ipv4.tcp_available_congestion_control')
    commands.getoutput('sysctl net.ipv4.tcp_congestion_control')
    print("BBR setup success.")
    return True


def whoami():
    user = commands.getoutput('whoami')
    if user == "root":
        return True
    else:
        print("Your permission is not ROOT.")
        return True


def setup_tools():
    commands.getoutput('apt-get update')
    commands.getoutput('apt-get -y install zip unzip vim net-tools')
    print("Tools setup success.")
    return True


def setup_docker():
    res = raw_input("Install docker for your server ? (Y/N)")
    if res not in YES:
        return False
    commands.getoutput('apt-get -y install apt-transport-https ca-certificates curl gnupg2 lsb-release software-properties-common')
    commands.getoutput('curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -')
    commands.getoutput('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"')
    commands.getoutput('apt-get update')
    commands.getoutput('apt-get -y install docker-ce')
    commands.getoutput('systemctl enable docker')
    commands.getoutput('systemctl start docker')
    print("Docker setup success.")
    return True


def setup_shadowsocks():
    res = raw_input("Install shadowsocks for your server ? (Y/N)")
    if res not in YES:
        return False
    commands.getoutput("docker pull shadowsocks/shadowsocks-libev")
    print("Shadowsocks setup success.")
    init_ss_port()
    return True


def init_ss_port():
    res = raw_input("Init new port of shadowsocks for your server ? (Y/N)")
    if res not in YES:
        return False
    while True:
        name = raw_input("Please input your user name:")
        pwd = raw_input("Please input your user pwd:")
        port = raw_input("Please input your user port:")
        try:
            if not 0 < int(port) < 65500:
                print("Port Error.")
                continue
        except:
            print("Port Error.")
            continue
        commands.getoutput("docker run -e PASSWORD=%s "
                           "-p%s:8388 -p%s:8388/udp --restart=always "
                           "--name %s -d shadowsocks/shadowsocks-libev" % (pwd, port, port, name))
        res = raw_input("Init other new user ? (Y/N)")
        if res not in YES:
            break
    return True


def main():
    if whoami():
        setup_bbr()
        setup_tools()
        setup_docker()
        setup_shadowsocks()


if __name__ == '__main__':
    main()
