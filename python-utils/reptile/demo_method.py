import re
import requests
import hashlib
import time


def get_index(url):
    respose = requests.get(url)
    if respose.status_code==200:
        return respose.text

def parse_index(res):
    urls = re.findall(r'class="items".*?href="(.*?)"', res,re.S)  # re.S 把文本信息转换成1行匹配
    return urls

# 循环html地址，并进一步分离MP4_url 地址
def get_detail(urls):
    for url in urls:
        if not url.startswith('http'):
            url='http://www.xiaohuar.com%s' %url
        result = requests.get(url)
        if result.status_code==200 :
            mp4_url_list = re.findall(r'id="media".*?src="(.*?)"', result.text, re.S)
            if mp4_url_list:
                mp4_url=mp4_url_list[0]
                print(mp4_url)  # 打印地址
                # save(mp4_url) # 下载地址

# 下载
def save(url):
    video = requests.get(url)
    if video.status_code==200:
        m=hashlib.md5()
        m.update(url.encode('utf-8'))
        m.update(str(time.time()).encode('utf-8'))
        filename=r'%s.mp4'% m.hexdigest()
        filepath=r'D:\\%s'%filename
        with open(filepath, 'wb') as f:
            f.write(video.content)

# 主方法调用，随机循环生成url调用
def main():
    for i in range(5):
        res1 = get_index('http://www.xiaohuar.com/list-3-%s.html'% i )
        res2 = parse_index(res1)
        get_detail(res2)

if __name__ == '__main__':
    main()