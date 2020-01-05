from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

html = '''<!DOCTYPE html> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
  <head> 
    <meta charset="UTF-8" /> 
      <style> 
              body{text-align:center} 
      </style> 
  </head> 
  <body> 
  </body> 
</html>
'''
ua = {'User-Agent' :
                  'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Mobile Safari/537.36'}

@app.route('/')
def get_ip():
    ip = request.headers['X-Forwarded-For'].replace(' ','').split(',')[0]
    #response = requests.get("http://ip-api.com/json/" + ip + "?lang=zh-CN").json()
    response = requests.get("https://www.ipip.net/ip/"+ip+".html",headers=ua).content
    _soup = BeautifulSoup(response, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    '''
    country_name = response['country']
    region_name = response['regionName']
    city = response['city']
    isp = response['isp']
    region_info = country_name + ' ' + region_name + ' ' + city
    '''
    #tables = _soup.find_all(style='clear: both')
    region_info = ''
    isp = ''
    tds = _soup.find_all('td')
    region_info = ''
    isp = ''
    for td in tds:
        if td.string == "地理位置":
            region_info = td.find_next_sibling('td').span.string
        if td.string == "运营商":
            isp = td.find_next_sibling('td').span.string

    soup.body.append(soup.new_tag('br'))
    soup.body.append(soup.new_tag('br'))
    soup.find_all("br")[0].insert_before(soup.new_string(ip))
    soup.find_all("br")[0].insert_after(soup.new_string(region_info))
    soup.find_all("br")[1].insert_after(soup.new_string(isp))
    #print(soup)
    return str(soup)

if __name__ == '__main__':
    app.run()
