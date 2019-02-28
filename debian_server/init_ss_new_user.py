# !/usr/bin/python
# -*- encoding:utf-8 -*-
import commands

YES = ("Y", "y", "YES", "yes")


def init_ss_port():
    res = raw_input("Init new port of shadowsocks for your server ? (Y/N)")
    if res not in YES:
        return False
    while True:
        name = raw_input("Please input your user name:")
        pwd = raw_input("Please input your user pwd:")
        port = raw_input("Please input your user port:")
        commands.getoutput("docker run -e PASSWORD=%s "
                           "-p%s:8388 -p%s:8388/udp --restart=always "
                           "--name %s -d shadowsocks/shadowsocks-libev" % (pwd, port, port, name))
        res = raw_input("Init other new user ? (Y/N)")
        if res not in YES:
            break
    return True


if __name__ == '__main__':
    init_ss_port()
