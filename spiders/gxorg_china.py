from juicer.utils import*
from dateutil import parser
class Gxorg(JuicerSpider):
    name = "gxorg_china"
    start_urls = ['http://news.gxorg.com/xianggang/','http://news.gxorg.com/guoji/','http://news.gxorg.com/guonei/','http://news.gxorg.com/xianggang/','http://news.gxorg.com/aomen/','http://news.gxorg.com/taiwan/','http://society.gxorg.com/','http://ent.gxorg.com/baoliao/','http://ent.gxorg.com/xingwen/','http://ent.gxorg.com/zongyi/','http://ent.gxorg.com/xinge/','http://ent.gxorg.com/huaxu/','http://ent.gxorg.com/yinyue/','http://ent.gxorg.com/dianshi/','http://ent.gxorg.com/xingzuo/','http://finance.gxorg.com/chuangye/','http://finance.gxorg.com/huangjin/','http://finance.gxorg.com/renwu/','http://finance.gxorg.com/hangqing/','http://finance.gxorg.com/gupiao/','http://finance.gxorg.com/meigu/','http://finance.gxorg.com/dapan/','http://finance.gxorg.com/ganggu/','http://finance.gxorg.com/licai/','http://finance.gxorg.com/yinxing/','http://finance.gxorg.com/baoxian/','http://finance.gxorg.com/baoxian/','http://finance.gxorg.com/zhengquan/','http://finance.gxorg.com/jinrong/','http://tech.gxorg.com/hulian/','http://tech.gxorg.com/faming/','http://tech.gxorg.com/ziran/','http://tech.gxorg.com/tianwen/','http://tech.gxorg.com/qiqu/','http://tech.gxorg.com/jiadian/','http://tech.gxorg.com/shuma/','http://tech.gxorg.com/diannao/','http://tech.gxorg.com/tongxin/','http://sports.gxorg.com/zixun/','http://sports.gxorg.com/guonei/','http://sports.gxorg.com/wangqiu/','http://sports.gxorg.com/tianjing/','http://sports.gxorg.com/nvlan/','http://sports.gxorg.com/nanlan/','http://sports.gxorg.com/yingchao/','http://sports.gxorg.com/yijia/','http://sports.gxorg.com/xijia/','http://sports.gxorg.com/zhongchao/','http://edu.gxorg.com/zixun/','http://edu.gxorg.com/mingshi/','http://edu.gxorg.com/liuxue/','http://edu.gxorg.com/zhaosheng/','http://edu.gxorg.com/peixun/','http://edu.gxorg.com/yuancheng/','http://edu.gxorg.com/guangjiao/','http://edu.gxorg.com/xiaoyuan/','http://edu.gxorg.com/mingxiao/','http://edu.gxorg.com/chengkao/','http://edu.gxorg.com/zikao/','http://edu.gxorg.com/kaoyan/','http://edu.gxorg.com/sifa/','http://house.gxorg.com/zhekouyouhui/','http://house.gxorg.com/xinfangdaogou/','http://house.gxorg.com/loushikuaixun/','http://house.gxorg.com/fangchanzixun/','http://culture.gxorg.com/minsu/','http://culture.gxorg.com/yishu/','http://culture.gxorg.com/zixun/','http://culture.gxorg.com/paimai/','http://culture.gxorg.com/yuanchuang/','http://culture.gxorg.com/yichan/','http://culture.gxorg.com/shuhua/','http://culture.gxorg.com/kaogu/','http://culture.gxorg.com/shoucang/','http://culture.gxorg.com/lishi/','http://culture.gxorg.com/bolan/','http://culture.gxorg.com/wenwu/','http://culture.gxorg.com/sheying/','http://culture.gxorg.com/biaoyan/','http://culture.gxorg.com/zhanlan/','http://people.gxorg.com/zixun/','http://people.gxorg.com/jiaozi/','http://people.gxorg.com/wangping/','http://people.gxorg.com/fangtan/','http://people.gxorg.com/xinxiu/','http://people.gxorg.com/xianxian/','http://people.gxorg.com/zhengyao/','http://people.gxorg.com/mingjia/','http://people.gxorg.com/youzi/','http://people.gxorg.com/shangjia/','http://people.gxorg.com/yiren/','http://auto.gxorg.com/shijia/','http://auto.gxorg.com/zuche/','http://auto.gxorg.com/zixun/','http://auto.gxorg.com/tousupingtai/','http://auto.gxorg.com/xinche/','http://auto.gxorg.com/gouche/','http://auto.gxorg.com/daogou/','http://auto.gxorg.com/baojia/','http://auto.gxorg.com/ershou/','http://auto.gxorg.com/cheqi/','http://auto.gxorg.com/chemo/','http://auto.gxorg.com/yongche/','http://auto.gxorg.com/changshang/','http://auto.gxorg.com/weixiu/','http://auto.gxorg.com/pingce/','http://auto.gxorg.com/chexing/','http://auto.gxorg.com/chezhan/','http://auto.gxorg.com/hangqing/','http://traffic.gxorg.com/jiaotongzixun/','http://traffic.gxorg.com/cheshidongtai/','http://traffic.gxorg.com/xuecheyongche/','http://traffic.gxorg.com/jiaoguangonggao/','http://traffic.gxorg.com/jiaotongzhiyin/','http://traffic.gxorg.com/baoguangtai/']

    def parse(self,response):
        hdoc = HTML(response)
        urls = hdoc.select('//div[@id="mainContent"]//p[@class="title title_4"]//a//@href')
        for url in urls:
            yield Request(url,self.parse_details,response)

    def parse_details(self,response):
        hdoc = HTML(response)
        title = textify(hdoc.select('//p[@class="title title_newsinfo"]//text()'))
        text = textify(hdoc.select('//div[@class="content"]//text()')[2:-3])
        dt_added = textify(hdoc.select('//p[@class="news_writer"]//span//text()'))
        author = textify(hdoc.select('//p[@class="news_writer"]/text()'))
        author= author.split(u'\uff1a')
        author = author[1]
        dt_added = get_timestamp(parse_date(xcode(dt_added)) - datetime.timedelta(hours=8))

        item = Item(response)
        item.set('title',title)
        item.set('text',text)
        item.set('dt_added',dt_added)
        item.set('author.name',author)
        item.set('url', response.url)
        yield item.process()





