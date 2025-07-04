# frp配置

# frps下载配置参考

https://zhuanlan.zhihu.com/p/665466938

frps开机自启动参考

https://blog.csdn.net/a1647010108/article/details/135145121?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522171084554316800213032943%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=171084554316800213032943&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-135145121-null-null.142^v99^pc_search_result_base7&utm_term=frp%E5%BC%80%E6%9C%BA%E8%87%AA%E5%90%AF&spm=1018.2226.3001.4187



## frps

```
bindPort = 7000 #{必选} 客户端与该端口建立连接      
log.to = "console" #{可选}  日志配置， 通过打印的方式输出日志  
vhostHTTPPort = 7100 #{可选} http代理需要，当访问该端口时跳到对应本地frpc代理
vhostHTTPSPort = 7200  #{可选} https代理需要，当访问该端口时跳到对应本地frpc代理 
transport.tcpMux = true #tcp流多路复用（优化传输，需一致）

#身份验证

auth.method = "token"  #{可选}身份验证方式 
auth.token = "hdj18398228397" #token设置密码，用于通过身份验证创建连接

#frp服务仪表板配置

webServer.port = 7300  #{也可自行修改端口}      
webServer.addr = "0.0.0.0" #公网ip或者域名  
webServer.user = "admin" #登录用户名{可自行修改}    
webServer.password = "admin" #登录密码{可自行修改}

```



## frpc

```
# frpc.toml
transport.tls.enable = true		# 从 v0.50.0版本开始，transport.tls.enable的默认值为 true
serverAddr = "47.236.80.228"
serverPort = 7000 				# 公网服务端通信端口

auth.token = "hdj18398228397" 			# 令牌，与公网服务端保持一致

[[proxies]]
name = "test-http"
type = "tcp"
localIP = "127.0.0.1"			# 需要暴露的服务的IP
localPort = 22				# 将本地9000端口的服务暴露在公网的6060端口
remotePort = 6060 				# 暴露服务的公网入口
```

