import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
import json, os

current_path = os.path.dirname(os.path.abspath(__file__))

print(current_path)
class IoeSpider(scrapy.Spider):
    name = "ioe"
    start_urls = [
            'https://exam.ioe.edu.np/',
        ]
    def parse(self, response):
        tds = response.css('td')
        i=[str(a) for a in range(1,11)]
        
        notices = []
        for td in tds:
            # tds[0] -> s.no  ,tds[1] -> title  , tds[2] -> notice date
            if td.css('td::text').get() in i:
                title = tds[tds.index(td)+1].css('span::text').get()
                url = str(response.url).split('/?')[0][:-1] + str(tds[tds.index(td)+1].css('a::attr(href)').get())
                date = tds[tds.index(td)+2].css('td::text').get()
                notices.append({'title':title, 'url':url, 'date':date})
        
        with open(os.path.join(current_path, 'new_notices.json'),'w') as file:
            json.dump(notices, file, indent = 4)

        #next_page = response.css('li.PagedList-skipToNext a::attr(href)').get()
        
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)





# the wrapper to make it run more times
def run_spider():
    def f(q):
        try:
            spider=IoeSpider
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            #q.put(e)
            pass
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    #p.stop()

    if result is not None:
        raise result

#run_spider()



def get_new_notifications(update=True):
  run_spider()
  with open(os.path.join(current_path, 'ioe_notices.json'), 'r') as file:
    old_notices = json.load(file)

  with open(os.path.join(current_path, 'new_notices.json'), 'r') as file:
    scraped_notices = json.load(file)

  new_notices = []
  for notice in reversed(scraped_notices):
     if notice not in old_notices:
        old_notices.insert(0, notice)
        new_notices.append(notice)
        print('---------Adding new:\n\t topic {}\n\t url:{}'.format(notice['title'], notice['url'], notice['date']))
  
  if update:
    with open(os.path.join(current_path, 'ioe_notices.json'),'w') as file:
      json.dump(old_notices, file, indent = 4)

  ## Got new_topics and new_urls
  return(new_notices)

