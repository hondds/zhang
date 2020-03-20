import requests
from bs4 import BeautifulSoup
import pandas as pd

movie = []

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    res = requests.get(url,headers = headers)
    # print(res.text)
    return res.text

def parse_html(html):
    soup = BeautifulSoup(html,'lxml')
    ol = soup.find('ol',attrs={'class':'grid_view'})
    lis = ol.find_all('li')
    for li in lis:
        name_div = li.find_all('div',attrs={'class':'hd'})[0]
        name = name_div.find_all('span')[0].string
        rate_num = li.find_all('span',attrs={'class':"rating_num"})[0].string
        renshu_div = li.find_all('div',attrs={'class':'star'})[0]
        renshu = renshu_div.find_all('span')[3].string
        # print(renshu)
        data = {'name':name,'rate_num':rate_num,'reshu':renshu}
        movie.append(data)



if __name__ == '__main__':

    for i in range(0,251,25):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i)
        html = get_html(url)
        parse_html(html)

    moviedata = pd.DataFrame(movie)
    moviedata.to_csv('douban.csv')
    print('写入csv文件成功！')
