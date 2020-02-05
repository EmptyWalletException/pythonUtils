import urllib.request
import time
import os

# 执行地址链接的方法,url=目标网址,accept=true代表开启模拟浏览器请求头
def url_open(url,accept):
    req = urllib.request.Request(url)
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
    req.add_header('User-Agent',header)
    if accept == 'true':   
        req.add_header('Accept', 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

# 从传入的网页HTML中找出所有匹配的子网页,通常此方法是用于模拟点击网页中的相册封面进入
def find_child_urls(html):
    child_urls = []
    child_urls_prefix = '<a class="mark" href="'
    child_urls_keyword = 'home_1'
    a = html.find(child_urls_prefix)
    while a != -1 :
        b = html.find(child_urls_keyword,a,a+255)
        if b != -1 :
            child_urls.append(html[a+22:b+6])
        else :
            b = a+9
        a =  html.find(child_urls_prefix,b)
    print(child_urls)
    return child_urls
    

# 找出html中所有要爬取的图片地址,html=从网址请求后获取的网页html,img_href_prefix=网页中图片地址所在标签的前缀(用于正则匹配)
def find_imgs_addrs(html):
    imgs_addrs = []
    img_href_prefix = 'src="http://h1.ioliu.cn/bing/'
    img_href_keyword = '.jpg'
    a = html.find(img_href_prefix)
    while a != -1 :
        b = html.find(img_href_keyword,a,a+255)
        if b != -1 :
            current_url = html[a+5:b+4]
            print("已获取到图片链接:"+current_url)
            imgs_addrs.append(current_url)
        else :
            b = a+9
        a =  html.find(img_href_prefix,b)
    return imgs_addrs

# 找出html中所有的图片标题
def find_imgs_titles(html):
    imgs_titles = []
    img_title_prefix = '<h3>'
    img_title_keyword = '('
    a = html.find(img_title_prefix)
    while a != -1 :
        b = html.find(img_title_keyword,a,a+255)
        if b != -1 :
            current_title = html[a+4:b].strip()
            imgs_titles.append(current_title)
        else :
            b = a+9
        a =  html.find(img_title_prefix,b)
    return imgs_titles

# 通过传入的图片地址集合下载图片并保存到传入的文件夹中,
# imgs_addrs:图片地址数组,imgs_titles:图片标题数组,与地址数组顺序对应
def download_save_imgs(imgs_addrs,imgs_titles):
    i = 0
    for each in imgs_addrs:
        print("正在尝试访问图片链接:"+each)
        img = url_open(each,'false')       
        fileName = imgs_titles[i] + '.jpg'
        with open(fileName,'wb') as f :
            f.write(img)
            print('已经将图片使用对应标题保存:'+fileName)
        i=i+1

#校验页码是否符合常规逻辑,返回True代表符合,返回False代表不符合
def check_page_number(page_begin_num,page_end_num):
    page_begin_num = int(page_begin_num)
    page_end_num = int(page_end_num)
    if 0 >= page_begin_num :
        return False
    if 0 >= page_end_num:
        return False
    if page_begin_num > page_end_num:
        return False
    return True

# 主执行方法,folder:储存路径,url:网址,page_begin_num:起始页码,从1开始,page_end_num:结束页码
def execue(folder,url,page_begin_num,page_end_num):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    os.chdir(folder)
    if check_page_number(page_begin_num,page_end_num) :
        #将起始页从0修正为1
        page_begin_num = 1 if page_begin_num == 0 else page_begin_num;
        page_current_num = page_begin_num
        page_total_num = page_end_num - page_begin_num + 1
        for i in range(page_total_num):
            page_url = url + '/?p=' + str(page_current_num)
            page_html = url_open(page_url,'true').decode('utf-8')
            imgs_addrs = find_imgs_addrs(page_html)
            imgs_titles = find_imgs_titles(page_html)
            download_save_imgs(imgs_addrs,imgs_titles)
            page_current_num += 1
    else :
        print('请检查传入的页码!')

if __name__=='__main__':
    url = 'https://bing.ioliu.cn'
    folder = 'bing壁纸/'+time.strftime("%Y-%m-%d_%H-%M-%S")
    execue(folder,url,1,1)
    print("-----已完成本次任务-----")
