# 并行工作进程数
workers = 4

# 指定每个工作者的线程数
threads = 2

# 监听内网端口8088
bind = '0.0.0.0:8088'

# 设置守护进程,将进程交给supervisor管理
# daemon = 'true'

# 工作模式协程
worker_class = 'gevent'

# 设置最大并发量
worker_connections = 2000

# 设置日志记录水平
loglevel = 'warning'
