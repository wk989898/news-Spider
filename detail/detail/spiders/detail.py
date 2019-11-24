import scrapy
import os
import json
from ..items import DetailItem
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
          yield scrapy.Request(url=url, callback=self.parse,headers={'Referer':'http://new.qq.com/'})


  def parse(self, response):
    _c={}
    # title=response.css('title::text').extract_first()
    try:
      content=response.css('.qq_conent')[0]
    except IndexError:
      content=None
    if content==None:
      c_video = response.css('video::attr(src)').extract()
      c_title = response.css('.title::text').extract_first()
      _c['c_video'] = c_video
      _c['c_title'] = c_title
    else:
      c_title=content.css('h1::text').extract_first()
      c_intro=content.css('.introduction::text').extract_first()
      c_main=content.css('.one-p::text').extract()
      c_pics=content.css('.one-p img::attr(src)').extract()
      _c['c_title']=c_title
      _c['c_intro']=c_intro
      _c['c_main']=c_main
      _c['c_pics']=c_pics
    # 注意 ： 路径必须为数组类型
    for pic in c_pics:
      item=DetailItem()
      item['image_urls']=['https:'+pic]
      item['img_name']=response.url.split('/')[-1].replace('.html','')
      yield item

    page=response.url.split('/')[-1].replace('.html','.json')
    with open('../src/json/'+page,'w') as t:
      json.dump(_c,t,ensure_ascii=False,separators=(',',':'),indent=4)