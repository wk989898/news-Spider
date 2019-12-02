import requests
import json
import time
import os
import re
import copy

urls=['https://i.match.qq.com/ninja/fragcontent?pull_urls=news_top_2018', # 今日要闻
     'https://pacaio.match.qq.com/irs/rcd?&expIds=',
     'https://pacaio.match.qq.com/irs/rcd?token=49cbb2154853ef1a74ff4e53723372ce'
     ]
token=['&token=49cbb2154853ef1a74ff4e53723372ce',
       '&token=6e92c215fb08afa901ac31eca115a34f',
       '&token=c792fa43fc5289073875cc03cd6b1f4a',
       '&token=d0f13d594edfc180f5bf6b845456f3ea']
# 分类 ext:   cid也在里面
# sports（体育） || top || ent(娱乐) || milite_pc（军事） || world（国际）
# || tech(科技) || emotion（情感）|| finance（科技）|| auto（汽车）|| photo(图片)
# || games(游戏) || fashion（时尚）|| cul（文化） || visit（旅游）
# || astro（星座）|| baby（育儿） || comic（动漫）|| health（健康）||   ori（独家）
ext={
  'top': 'top&cid=137'+token[3],  #要闻
  'sports':'sports&cid=135'+token[1],
  'ent':'ent&cid=146'+token[0],
  'milite_pc':'milite_pc&cid=135'+token[1],
  'world':'world&cid=135'+token[1],
  'tech':'tech&cid=146'+token[0],
  'emotion':'emotion&cid=146'+token[0],
  'finance':'finance&cid=146'+token[0],
  'auto':'auto&cid=146'+token[0],
  'photo':'picture&cid=146'+token[0],
  'games':'games&cid=146'+token[0],
  'fashion':'fashion&cid=146'+token[0],
  'cul':'cul&cid=146'+token[0],
  'visit':'visit&cid=146'+token[0],
  'astro':'astro&cid=146'+token[0],
  'baby':'baby&cid=146'+token[0],
  'comic':'comic&cid=146'+token[0],
  'ori':'orignal&cid=33'+token[2], # 独家
  'health':'health&cid=146'+token[0],
}
# num :数量   page: 页数
num='100'
# 存放网址

# intro: 标题  img：图片  source：来源  media_icon：来源-icon  imgs：组图   vurl：网址
def getnews():
  for i in ext:
    url=urls[1]+'&ext='+ext[i]+'&num='+num+'page=0'
    response=requests.get(url).text
    # reg=re.compile(r'\w+[(]{1}(.*)[)]{1}')
    # res=reg.findall(response)
    _dict= json.loads(response)
    data=_dict['data']
    get_comment(data)

    urldata = []
    for j in data:
      urldata.append(j['vurl'])
    with open('./tohtml/'+i+'.json','w') as url_f:
      json.dump(urldata,url_f,ensure_ascii=False,separators=(',',':'),indent=4)

    with open('./result/'+i+'.json','w',encoding='utf-8') as f:
      json.dump(data,f,ensure_ascii=False,separators=(',',':'),indent=4)

# 今日要闻
def todaynews():
  res=requests.get(urls[0]).text
  _arr=json.loads(res)
  with open('./result/Today.json','w') as tf:
    json.dump(_arr,tf,ensure_ascii=False,separators=(',',':'),indent=4)

def get_comment(data):
  for k in data:
    comment=k["comment_id"]
    response=requests.get('http://coral.qq.com/article/'+comment+
                          '/comment/v2?orinum=10&oriorder=o&pageflag=&cursor=&scorecursor=0&orirepnum=&reppageflag=&source=&_=',
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}).text
    mydict = json.loads(response)
    if 'data' not in mydict:
      return
    mydata = mydict['data']
    k['oriCommList']=copy.deepcopy(mydata['oriCommList'])
    k['repCommList']=copy.deepcopy(mydata['repCommList'])
    k['userList']=copy.deepcopy(mydata['userList'])

todaynews()
getnews()
