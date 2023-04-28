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
        
        #text of data
        texts=[]
        
        #url of data
        urls=[]
        
        for td in tds:
            if td.css('td::text').get() in i:
                texts.append(tds[tds.index(td)+1].css('span::text').get())
                urls.append(str(response.url).split('/?')[0][:-1] + str(tds[tds.index(td)+1].css('a::attr(href)').get()))
        
        with open(os.path.join(current_path, 'new_notices.json'),'w') as file:
            json.dump({'topics':texts, 'urls':urls}, file, indent = 4)
        #break
        #print('\n\n\n\n\n',{'topics':texts, 'urls':urls})
        #yield{'topics':texts, 'urls':urls}
        #next_page = response.css('li.PagedList-skipToNext a::attr(href)').get()
        
        #with open('data.json','w') as file:
        #    json.dump({'texts':texts, 'urls':urls}, file, indent = 4)
        
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
    data = json.load(file)

  old_topics = data['topics']
  old_urls = data['urls']
  print(f'\n old_data: {data}')

  with open(os.path.join(current_path, 'new_notices.json'), 'r') as file:
    new = json.load(file)
  print(new)

  print(f'\n new_data: {new}')

  scraped_topics = new['topics']
  scraped_urls = new['urls']

  #reverse because it would be easier to stack on top of old_data
  scraped_topics.reverse()
  scraped_urls.reverse()
  # print(f'scraped_topics: {scraped_topics}')
  # print(f'scraped_urls: {scraped_urls}')
  
  new_topics = []
  new_urls = []

  for i in range(len(scraped_topics)):
    if scraped_topics[i] not in old_topics:
        old_urls.insert(0, scraped_urls[i])
        old_topics.insert(0, scraped_topics[i])
        new_topics.insert(0, scraped_topics[i])
        new_urls.insert(0, scraped_urls[i])
        print('---------Adding new:\n\t topic {}\n\t url:{}'.format(scraped_topics[i], scraped_topics[i]))
  if update:
    with open(os.path.join(current_path, 'ioe_notices.json'),'w') as file:
      json.dump({'topics':old_topics, 'urls':old_urls}, file, indent = 4)

  ## Got new_topics and new_urls
  return({'topics':new_topics, 'urls':new_urls})

