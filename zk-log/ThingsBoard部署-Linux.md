

本次安装环境ubuntu22

### 1. 环境准备

确保你的系统已经安装以下必要工具：

- **JDK 11**
   安装 OpenJDK 11：

  ```
  sudo apt update
  sudo apt install openjdk-11-jdk
  ```

  验证安装：

  ```
  java -version
  ```

- **Maven**
   安装 Maven：

  ```
  sudo apt install maven
  ```

  验证安装：

  ```
  mvn -v
  ```

- **Git**
   安装 Git：

  ```
  sudo apt install git
  ```

- **数据库**
   ThingsBoard 默认支持 PostgreSQL（或 Cassandra），以 PostgreSQL 为例：

  ```
  sudo apt install postgresql postgresql-contrib
  ```

  安装后根据需要配置数据库（创建数据库、设置用户及密码）。

  默认配置文件路径/etc/thingsboard/conf/thingsboard.yml

![image-20250324155939173](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20250324155939173.png)

```
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'postgres';
\q
sudo systemctl restart postgresql
```

```
sudo -u postgres psql
CREATE DATABASE thingsboard;
\q
```



下载ThingsBoard安装包：

目前最新的版本是  https://github.com/thingsboard/thingsboard/releases/tag/v3.9.1

下载deb安装包并上传至ubuntu

- 使用 dpkg 命令安装下载好的包：

```
sudo dpkg -i thingsboard-3.9.1.deb
```

- 安装时如遇到依赖问题执行以下命令

```
sudo apt --fix-broken install
```

## 初始化数据库并加载 Demo 数据

ThingsBoard 提供了安装脚本，用于初始化数据库架构并加载示例数据。执行以下命令：

```
sudo /usr/share/thingsboard/bin/install/install.sh --loadDemo
```

![image-20250324160659728](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20250324160659728.png)



## 4. 启动 ThingsBoard 服务

启动 ThingsBoard 后端服务：

```
sudo service thingsboard start
```

可使用以下命令检查服务状态：

```
sudo service thingsboard status
```

------

## 5. 访问并体验 Demo

打开浏览器，访问：

```
http://localhost:8080
```

默认登录账号为：

- **用户名**：sysadmin@thingsboard.org
- **密码**：sysadmin

登录后，将进入 ThingsBoard 的管理界面，体验设备管理、数据可视化、规则引擎等 demo 功能。





![image-20250324160934234](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20250324160934234.png)

![image-20250324161513771](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20250324161513771.png)