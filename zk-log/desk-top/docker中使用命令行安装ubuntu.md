
在 Docker 中安装 Ubuntu 实际上意味着从 Docker Hub 上拉取一个 Ubuntu 镜像并运行一个基于该镜像的容器。下面是如何做到这一点的步骤：

### 步骤 1: 拉取 Ubuntu 镜像

首先，你需要拉取一个 Ubuntu 镜像到你的系统。你可以选择特定的版本（如 `ubuntu:20.04`），或者如果你不指定版本，使用 `ubuntu:latest` 来拉取最新的官方 Ubuntu 镜像。打开你的终端或命令行界面，然后运行以下命令：

```
docker pull ubuntu:latest
```

这个命令会从 Docker Hub 拉取最新的 Ubuntu 镜像。如果你想要一个特定版本的 Ubuntu，只需将 `latest` 替换为你想要的版本号，例如 `20.04`。

### 步骤 2: 运行 Ubuntu 容器

拉取镜像后，你可以运行一个基于该镜像的容器。使用以下命令来运行一个交互式的容器，其中 `-it` 参数允许你交互式地使用容器内的 shell：

```
docker run -it --name ubuntu_container ubuntu:latest /bin/bash
```

这里的命令解析如下：

- `docker run` 命令用于创建并启动一个新的容器。
- `-it` 参数使容器在交互模式下运行，并分配一个伪终端。
- `--name ubuntu_container` 给容器指定一个名字（`ubuntu_container`），这样你就可以轻松地引用它。
- `ubuntu:latest` 指定使用哪个镜像来创建容器。这应该与你之前拉取的镜像标签匹配。
- `/bin/bash` 指定启动容器时要运行的命令。在这个例子中，它会启动 bash shell，允许你直接在容器中输入命令。

运行上述命令后，你将进入 Ubuntu 容器的 bash 环境中，可以在其中执行 Ubuntu 命令。当你完成操作并想退出容器时，只需输入 `exit` 命令或使用 `Ctrl+D` 快捷键。

### 额外提示

- **列出所有运行的容器**：如果你想看到当前所有正在运行的容器，可以使用 `docker ps` 命令。
- **停止容器**：要停止正在运行的容器，可以使用 `docker stop <容器名或ID>` 命令。
- **重新进入容器**：如果你的容器已经运行，但你想再次进入其 bash 环境，可以使用 `docker exec -it <容器名或ID> /bin/bash` 命令。

通过这些步骤，你就可以在 Docker 中轻松运行和管理 Ubuntu 容器了。



### 退出 Ubuntu 容器

如果你想退出容器的命令行界面，可以使用 `exit` 命令或按下 `Ctrl+D`。这会结束当前的 shell 会话，但容器本身会停止运行。要再次进入该容器的交互式命令行，可以使用：

```shell
docker start my_ubuntu_container
docker attach my_ubuntu_container
```



我需要使用ssh工具来连接到我的ubuntu需要如何做



要通过 SSH 连接到你在 Docker 容器中运行的 Ubuntu 系统，你需要执行几个步骤来设置环境。这些步骤包括在 Docker 容器中安装 SSH 服务、配置 SSH 服务、以及通过 Docker 端口映射来暴露 SSH 端口。下面是详细的步骤：

### 步骤 1: 创建一个带有 SSH 服务的 Ubuntu 容器

首先，你需要创建一个新的 Dockerfile 来构建一个包含 SSH 服务的 Ubuntu 容器镜像。

1. **创建 Dockerfile**：在一个空目录中创建一个文件命名为 `Dockerfile`，然后输入以下内容：

```
# 使用官方 Ubuntu 基础镜像
FROM ubuntu:latest

# 安装 SSH 服务
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:yourpassword' | chpasswd

# 更改 SSH 配置以允许 root 登录
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# 容器启动时运行 SSH 服务
CMD ["/usr/sbin/sshd", "-D"]
```

1. **构建 Docker 镜像**：在 Dockerfile 所在目录运行以下命令来构建你的镜像：

```
docker build -t ubuntu_ssh .
```

这会创建一个标签为 `ubuntu_ssh` 的新 Docker 镜像。

### 步骤 2: 运行带有 SSH 服务的 Ubuntu 容器

使用以下命令运行你刚刚创建的带有 SSH 服务的容器，并映射端口以便通过 SSH 连接：

```
docker run -d -p 2222:22 --name ubuntu_ssh_container ubuntu_ssh
```

这里 `-d` 参数使容器在后台运行，`-p 2222:22` 将容器的 22 端口（SSH 默认端口）映射到宿主机的 2222 端口。你可以选择使用其他宿主机端口，只需调整命令中的 `2222` 即可。

### 步骤 3: 通过 SSH 连接到容器

现在，你可以使用 SSH 客户端连接到运行 SSH 服务的 Docker 容器了：

```
ssh root@localhost -p 2222
```

当系统提示你输入密码时，使用你在 Dockerfile 中设置的密码（示例中为 `yourpassword`）。



使用ssh工具连接一致  用户名root 密码yourpassword