# 服务器部署脚本

## debian_server

### 使用Debian服务器的脚本

以下最佳适配国外云厂商，或对梯子有需求的服务器

- init_new_server.py  初始化新的服务器,包括google带宽算法bbr、压缩解压工具(zip unzip)、网络工具(net-tools)、Docker、shadowsocks服务端
- init_ss_new_user.py  为shadowsocks添加新的端口

说明：

1、bbr算法在某些云厂商的服务器上无法使用，请安装时选择不进行安装（已知：腾讯）

2、shadowsocks每添加一个端口和密码会新开启一个docker进程来运行
