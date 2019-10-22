import re
import requests

# 爬取网站视频
respose=requests.get('http://www.xiaohuar.com/v/')
print(respose.status_code)# 响应的状态码
print(respose.content)  #返回字节信息
print(respose.text)  #返回文本内容
urls=re.findall(r'class="items".*?href="(.*?)"',respose.text,re.S)  #re.S 把文本信息转换成1行匹配
url=urls[6]     # 这里获取第5个url进入，
result=requests.get(url)
# 获取视频地址
mp4_url=re.findall(r'id="media".*?src="(.*?)"',result.text,re.S)[0]
print(mp4_url)
# video=requests.get(mp4_url)

# 下面这个就是把 video 的视频下载到本地 d盘下了
# with open('D:\\a.mp4','wb') as f:
#     f.write(video.content)