一则短信猝不及防，tplink的自带免费域名的dns居然停了

- 第一个想到的是使用openwrt软路由替换，作为主路由实现ddns与端口映射

理解一下ddns的原理：

动态域名的ip不固定，这时候需要将域名与ip绑定 通过域名访问，这一过程叫做dns

TPLINK的 ddns 如何实现的：访问的域名只要能和实时变动的域名对应上，就ok了

一般自己配置dns服务对应的ip是固定的，我们要做的是让dns服务器或服务商知道ip变了，要去更新一下，

这时候需要有设备告诉dns服务器，ip发生了变化，你要更新一下



我有一个群晖，在群晖上检测公网ip,当ip变了时告诉dns服务器或服务商



github:https://github.com/joshuaavalon/SynologyCloudflareDDNS

配置参考：https://diveng.xyz/article/configuring-cloudflare-dynamic-dns-on-synology-dsm/

# Synology Cloudflare DDNS Script 📜

The is a script to be used to add [Cloudflare](https://www.cloudflare.com/) as a DDNS to [Synology](https://www.synology.com/) NAS. The script used an updated API, Cloudflare API v4.

## How to use

### Access Synology via SSH

1. Login to your DSM
2. Go to Control Panel > Terminal & SNMP > Enable SSH service
3. Use your client to access Synology via SSH.
4. Use your Synology admin account to connect.

### Run commands in Synology

1. Download `cloudflareddns.sh` from this repository to `/sbin/cloudflareddns.sh`

```
wget https://raw.githubusercontent.com/joshuaavalon/SynologyCloudflareDDNS/master/cloudflareddns.sh -O /sbin/cloudflareddns.sh
```

It is not a must, you can put I whatever you want. If you put the script in other name or path, make sure you use the right path.

1. Give others execute permission

```
chmod +x /sbin/cloudflareddns.sh
```

1. Add `cloudflareddns.sh` to Synology

```
cat >> /etc.defaults/ddns_provider.conf << 'EOF'
[Cloudflare]
        modulepath=/sbin/cloudflareddns.sh
        queryurl=https://www.cloudflare.com
        website=https://www.cloudflare.com
E*.
```

`queryurl` does not matter because we are going to use our script but it is needed.

### Get Cloudflare parameters

1. Go to your domain overview page and copy your zone ID.
2. Go to your profile > **API Tokens** > **Create Token**. It should have the permissions of `Zone > DNS > Edit`. Copy the api token.

### Setup DDNS

1. Login to your DSM
2. Go to Control Panel > External Access > DDNS > Add
3. Enter the following:
   - Service provider: `Cloudflare`
   - Hostname: `www.example.com`
   - Username/Email: `<Zone ID>`
   - Password Key: `<API Token>`