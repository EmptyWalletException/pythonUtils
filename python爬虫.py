import urllib.request
import os

# 执行地址链接的方法,url=目标网址,header=模拟浏览器请求头
def url_open(url,accept):
    req = urllib.request.Request(url)
    header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763'
    req.add_header('User-Agent',header)
    if accept is 'true':   
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
            imgs_addrs.append(html[a+5:b+4])
        else :
            b = a+9
        a =  html.find(img_href_prefix,b)
    print(imgs_addrs)
    return imgs_addrs

# 通过传入的html找到所有的图片标题
def find_imgs_titles(html):
    imgs_titles = []
    img_title_prefix = '<h3>'
    img_title_keyword = '('
    a = html.find(img_title_prefix)
    while a != -1 :
        b = html.find(img_title_keyword,a,a+255)
        if b != -1 :
            imgs_titles.append(html[a+4:b])
        else :
            b = a+9
        a =  html.find(img_title_prefix,b)
    print(imgs_titles)
    return imgs_titles

# 从详情页面读取详细数据
def find_details(html):
    details = []
    details_prefix = '<a class="mark" href="'
    details_keyword = 'home_1'
    a = html.find(details_prefix)
    while a != -1 :
        b = html.find(details_keyword,a,a+255)
        if b != -1 :
            details.append(html[a+22:b+6])
        else :
            b = a+9
        a =  html.find(details_prefix,b)
    print(details)
    return details

# 通过传入的图片地址集合下载图片并保存到传入的文件夹中
def save_imgs(imgs_addrs):
    for each in imgs_addrs:
        file_name = each.split('/')[-1]
        print(file_name)
        img = url_open(each,'false')
        with open(file_name,'wb') as f :
            f.write(img)

# 将传入的详情数据写入到txt文件中保存
def write_imgs_details(file_path,str):
    with open(file_path,'wt',encoding='utf-8') as f:
         f.write(str)


# 测试用,从文件读取子页面链接
def get_html_form_file(file_path):
    with open(file_path,'rt',encoding='utf-8') as f:
         html_file = f.read()
    return html_file


def check_page_number(page_begin_num,page_end_num):
    page_begin_num = int(page_begin_num)
    page_end_num = int(page_end_num)
    if 0 >= page_begin_num :
        page_begin_num = 1
    if 0 >= page_end_num:
        page_end_num = 1
    if page_begin_num > page_end_num:
        page_end_num = page_begin_num
    return [page_begin_num,page_begin_num,page_end_num]
# 主执行方法
def download_imgs(folder,url,page_begin_num,page_end_num):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.chdir(folder)
    page_numbers = check_page_number(page_begin_num,page_end_num)
    page_begin_num = page_numbers[0]
    page_current_num = page_numbers[1]
    page_end_num = page_numbers[2]
    page_total_num = page_end_num - page_begin_num + 1
    for i in range(page_total_num):
        page_url = url + '/?p=' + str(page_current_num)
        page_html = url_open(page_url,'true').decode('utf-8')
        imgs_addrs = find_imgs_addrs(page_html)
        save_imgs(imgs_addrs)
        page_current_num += 1

# 测试用
def test_detail():
    file_path = 'C:/NotSystemSrc/EdgeDownload/index.html'
    html_file = get_html_form_file(file_path)
    imgs_titles = find_imgs_titles(html_file)
    imgs_titles = str(imgs_titles)+'\r\t'
    write_imgs_details('C:/NotSystemSrc/EdgeDownload/details.txt',imgs_titles)

def test_save_image():
    file_path = 'C:/NotSystemSrc/EdgeDownload/index.html'
    folder = 'bing壁纸'
    html_file = get_html_form_file(file_path)
    imgs_addrs = find_imgs_addrs(html_file)
    save_imgs(folder,imgs_addrs)

if __name__=='__main__':
    url = 'https://bing.ioliu.cn'
    folder = 'C:/NotSystemSrc/代码备份/bing壁纸'
    download_imgs('bing壁纸',url,1,3)
    
