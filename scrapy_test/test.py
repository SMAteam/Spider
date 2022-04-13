
import pika
import json

credentials = pika.PlainCredentials('root', '123456')  # mq用户名和密码
# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
connection = pika.BlockingConnection(pika.ConnectionParameters(port = 5672,virtual_host = 'scrapy',credentials = credentials))
channel=connection.channel()
# 声明消息队列，消息将在这个队列传递，如不存在，则创建
result = channel.queue_declare(queue = 'scrapy')
channel.basic_publish(exchange = '',routing_key = 'scrapy',body = message)
connection.close()