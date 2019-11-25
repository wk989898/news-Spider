# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request





class DetailPipeline(ImagesPipeline):

  def get_media_requests(self, item, info):
    # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
    for image_url in item['image_urls']:
      # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
      yield Request(image_url,meta={'name':item['img_name']})

  # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
  def file_path(self, request, response=None, info=None):
    # 提取url前面名称作为图片名。
    name = request.meta['name']
    # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
    # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
    return name+'/'
