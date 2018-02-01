import scrapy
from scrapy import Selector, Request
from scraper_congreso.items import ScraperCongresoItem
#Search website: http://www.congreso.es/portal/page/portal/Congreso/Congreso/Publicaciones

class PublicacionesSpider(scrapy.Spider):
    name = "publicaciones"
    base_url = "http://www.congreso.es"
    total_initial_links = 0
    total_pages = 0
    total_publications = 0
    total_sessions_record = []
    #881, 134, 2112, 2046
    def start_requests(self):
        urls = ["http://www.congreso.es/portal/page/portal/Congreso/Congreso/Publicaciones"
                "?_piref73_2342619_73_1340041_1340041.next_page=/wc/servidorCGI&CMD=VERLST&CONF=BRSPUB.cnf&BASE=PU12&FMT=PUWTXLTS.fmt&DOCS=1-25&DOCORDER=FIFO&OPDEF=Y&QUERY=%28D%29.PUBL.",
                "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Publicaciones"
                "?_piref73_2342619_73_1340041_1340041.next_page=/wc/servidorCGI&CMD=VERLST&CONF=BRSPUB.cnf&BASE=PU11&FMT=PUWTXLTS.fmt&DOCS=1-25&DOCORDER=FIFO&OPDEF=Y&QUERY=%28D%29.PUBL.",
                "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Publicaciones"
                "?_piref73_2342619_73_1340041_1340041.next_page=/wc/servidorCGI&CMD=VERLST&CONF=BRSPUB.cnf&BASE=PU10&FMT=PUWTXLTS.fmt&DOCS=1-25&DOCORDER=FIFO&OPDEF=Y&QUERY=%28D%29.PUBL.",
                "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Publicaciones?_piref73_2342619_73_1340041_1340041.next_page=/wc/servidorCGI&CMD=VERLST&CONF=BRSPUB.cnf&BASE=PUW9&FMT=PUWTXLTS.fmt&DOCS=1-25&DOCORDER=FIFO&OPDEF=Y&QUERY=%28D%29.PUBL."
                ]
        for url in urls:
            print url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #self.total_initial_links += 1
        #print "Total inital links: " + str(self.total_initial_links)
        sel = scrapy.Selector(response)
        yield Request(response.url,callback=self.parse_publicaciones_links, dont_filter=True)
        nextornot = sel.xpath('//*[@id="RESULTADOS_BUSQUEDA"]/div[30]/a[last()-1]//text()').extract().pop()
        #print nextornot
        #links = sel.xpath('//*[@id="RESULTADOS_BUSQUEDA"]/div[30]/a/@href').extract()
        #print links
        #print len(links)
        if 'Siguiente' in nextornot:
            new_url = sel.xpath('//*[@id="RESULTADOS_BUSQUEDA"]/div[30]/a[last()-1]/@href').extract().pop()
            url = self.base_url + new_url
            yield Request(url)

    def parse_publicaciones_links(self, response):
        self.total_pages += 1
        #print response.url
        print "Links used" + str(self.total_pages)
        sel=Selector(response)
        urls = sel.xpath('//*[@id="RESULTADOS_BUSQUEDA"]/div/div/p[1]/a/@href').extract()
        #print urls
        for url in urls:
            url = self.base_url + url
            yield Request(url,callback=self.parse_text_from_publicacion)

    def parse_text_from_publicacion(self, response):
        sel=Selector(response)
        #print response.url
        text = sel.xpath('//*[@id="TEXTOS_POPUP"]/div[@class="texto_completo"]//text()').extract()
        #print text
        #self.total_publications += 1
        cleaned_text = []
        for t in text:
            if not t.startswith('/n'):
                cleaned_text.append(t.strip())
        #print cleaned_text
        item = ScraperCongresoItem()
        item['text'] = cleaned_text
        self.total_sessions_record.append(item)
        return item