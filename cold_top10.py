import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Bar
all_data=[]
def parse_page(url):
    headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }

    res = requests.get(url,headers = headers)
    text = res.content.decode("utf-8")
    soup = BeautifulSoup(text,'html5lib')
    conMidtab = soup.find('div',class_='conMidtab')
    tabs = conMidtab.find_all('table')
    for tab in tabs:
        trs = tab.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            mintemp_td = tds[-2]
            city = list(city_td.stripped_strings)[0]
            min = list(mintemp_td.stripped_strings)[0]
            all_data.append({'city':city,'mintemp':int(min)})



def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hz.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        parse_page(url)

    all_data.sort(key = lambda data:data['mintemp'])
    data = all_data[0:10]
    cities =list(map(lambda x:x['city'],data))
    temps = list(map(lambda x:x['mintemp'],data))
    chart = Bar()
    chart.add_xaxis(cities)
    chart.add_yaxis('',temps)
    chart.render('abc.html')


if __name__ == '__main__':
    main()

