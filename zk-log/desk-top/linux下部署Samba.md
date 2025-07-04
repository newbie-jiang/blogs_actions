要在Ubuntu上设置服务，使得Windows用户可以通过`\\IP`地址访问共享文件夹，您需要使用Samba服务。Samba是一个免费的软件，提供了符合SMB/CIFS协议的文件和打印服务，使得Linux和Windows系统之间的文件共享成为可能。以下是如何在Ubuntu上安装和配置Samba服务，以及如何创建一个共享文件夹，使Windows用户能够通过`\\IP`地址访问它的步骤。

### 安装Samba

1. 打开Ubuntu终端。

2. 更新包列表：

   ```
   sudo apt update
   ```

3. 安装Samba：

   ```
   sudo apt install samba
   ```

### 配置共享文件夹

1. 创建一个新的文件夹来共享，或选择一个现有的文件夹。例如，创建一个名为`shared`的文件夹：

   ```
   mkdir ~/shared
   ```

2. 分配适当的权限给这个文件夹，确保其他用户可以访问：

   ```
   chmod 777 ~/shared
   ```

   **注意**：这里使用的`777`权限很宽松，允许所有用户读写执行。根据您的安全需求，您可能需要使用更严格的权限。

3. 编辑Samba配置文件以添加共享文件夹的配置。首先，备份原始配置文件：

   ```
   sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.backup
   ```

4. 使用文本编辑器打开配置文件：

   ```
   sudo nano /etc/samba/smb.conf
   ```

5. 在文件末尾添加以下内容，以配置共享：

   ```
   [SharedFolder]
   path = /home/username/shared
   read only = no
   browsable = yes
   ```

   将`/home/username/shared`替换为您的共享文件夹的实际路径。

6. 保存文件并退出编辑器。

### 添加Samba用户

1. 创建一个Samba用户。这个用户需要对应一个系统用户，所以如果您还没有为要共享的目录创建一个系统用户，现在就创建一个。然后，为这个用户创建一个Samba密码：

   ```
   sudo smbpasswd -a username
   ```

   将`username`替换为您的用户名。系统会提示您输入并确认密码。

2. 启动Samba服务并设置为开机启动：

   ```
   sudo systemctl restart smbd
   sudo systemctl enable smbd
   ```







在windows下在命令窗口使用以下命令访问     其中SharedFolder是所要共享的文件夹

```
\\192.168.8.41\SharedFolder   
```

![image-20240307210818376](https://newbie-typora.oss-cn-shenzhen.aliyuncs.com/zhongke/image-20240307210818376.png)

如果添加其他文件夹则在 /etc/samba/smb.conf 最后添加其他文件夹

如创建共享文件夹名为software  ，需要共享的路径为/home/username/software

```
[SharedFolder]
path = /home/username/software
read only = no
browsable = yes
```



访问\\192.168.8.41 可看到所有文件夹

