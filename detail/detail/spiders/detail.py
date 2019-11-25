import scrapy
import os
import json
import requests
import copy
import re
import PIL

class detail(scrapy.Spider):
  name = 'detail_spider'

  def start_requests(self):
    files = os.listdir('../tohtml')
    urllist=[]
    urls=[]
    for file in files:
      f=os.path.join('../tohtml/',file)
      with open(f,'r') as urls_file:
        urls=json.load(urls_file)
        urllist.append(urls)
        for url in urls:
          yield scrapy.Request(url=url, callback=self.parse, headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'referer':'http://new.qq.com/'})


  def parse(self, response):
      _c={}
      if re.search(r'(/video/)',response.url):
        id=response.url.split('/')[-1]
        self.getUrl(id,_c)
        return
      title=response.css('title::text').extract_first()
      content=response.css('.qq_conent')[0]
      c_intro=content.css('div[class=introduction]::text').extract_first()
      c_main=content.css('.one-p::text').extract()
      c_title=content.css('h1::text').extract_first()
      c_pics=content.css('.one-p img::attr(src)').extract()
      _c['c_intro']=copy.deepcopy(c_intro)
      _c['c_main']=copy.deepcopy(c_main)
      _c['c_pics']=copy.deepcopy(c_pics)
      _c['c_title']=copy.deepcopy(c_title)
      _c['title']=copy.deepcopy(title)

    # 注意 ： 路径必须为数组类型
    # for pic in c_pics:
    #   item=DetailItem()
    #   item['image_urls']=['https:'+pic]
    #   item['img_name']=response.url.split('/')[-1].replace('.html','')
    #   yield item

      page=response.url.split('/')[-1].replace('.html','.json')
      with open('../src/json/'+page,'w') as t:
       json.dump(_c,t,ensure_ascii=False,separators=(',',':'),indent=4)

  def getUrl(self,id,obj):
      response=requests.get('https://pacaio.match.qq.com/vlike/detail?vid='+id,
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}).text
      _dict = json.loads(response)
      res=_dict['data']
      obj['c_intro']=copy.deepcopy(res['intro'])
      obj['title']=copy.deepcopy(res['title'])
      obj['c_pics']=copy.deepcopy(res['img'])
      return