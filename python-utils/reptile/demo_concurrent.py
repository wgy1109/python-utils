import re
import requests
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
p=ThreadPoolExecutor(30) #创建1个程池中，容纳线程个数为30个；


def get_index(url):
    respose = requests.get(url)
    if respose.status_code==200:
        return respose.text

def parse_index(res):
    res=res.result() #进程执行完毕后，得到1个对象
    urls = re.findall(r'class="items".*?href="(.*?)"', res,re.S)  # re.S 把文本信息转换成1行匹配
    for url in urls:
        p.submit(get_detail(url))  #获取详情页 提交到线程池



def get_detail(url):  #只下载1个视频
        if not url.startswith('http'):
            url='http://www.xiaohuar.com%s' %url
        result = requests.get(url)
        if result.status_code==200 :
            mp4_url_list = re.findall(r'id="media".*?src="(.*?)"', result.text, re.S)
            if mp4_url_list:
                mp4_url=mp4_url_list[0]
                print(mp4_url)
                # save(mp4_url)


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

def main():
    for i in range(5):
        p.submit(get_index,'http://www.xiaohuar.com/list-3-%s.html'% i ).add_done_callback(parse_index)
        #1、先把爬主页的任务（get_index）异步提交到线程池
        #2、get_index任务执行完后，会通过回调函add_done_callback（）数通知主线程，任务完成；
        #2、把get_index执行结果（注意线程执行结果是对象，调用res=res.result()方法，才能获取真正执行结果），当做参数传给parse_index
        #3、parse_index任务执行完毕后，
        #4、通过循环，再次把获取详情页 get_detail（）任务提交到线程池执行



if __name__ == '__main__':
    main()