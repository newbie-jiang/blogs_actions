



```
sudo -i
sudo docker pull gitlab/gitlab-ce:latest

docker run -d \
  --hostname gitlab.your-domain.com \
  -p 2080:80 \
  -p 20443:443 \
  -p 2022:22 \
  --name gitlab \
  --restart always \
  -v /srv/gitlab/config:/etc/gitlab \
  -v /srv/gitlab/logs:/var/log/gitlab \
  -v /srv/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest
  
  

```

查看密码

登录账户root

```
docker exec gitlab cat /etc/gitlab/initial_root_password
```



设置中文：

1. 登录 GitLab 后，右上角点击头像 → **Settings**
2. 左侧选 **Preferences**
3. 在 **Language** 下拉里选 **简体中文 (Chinese)**
4. 滚动到页面底部，点击 **Save changes**

这样该用户的所有界面都会变成中文，且对每个用户都独立，别人不受影响。****
