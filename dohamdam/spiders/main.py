import scrapy
from dohamdam.dohamdam_db import DB 
from time import sleep
from decouple import config

domain = config("domain")
username = config("user")
password = config("password")
search_filters = config("search_filters")
discord = config("discord")
session = DB(username)


class QuotesSpider(scrapy.Spider):
    name = "dohamdam"
    start_urls = [
        f'{domain}/',
    ]
    completed=[]
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.unread=0


    def parse(self, response):
        token = response.css('#sec1').attrib['value']+response.css('#sec7').attrib['value']+response.css('#sec4').attrib['value']+response.css('#sec5').attrib['value']+response.css('#sec2').attrib['value']+response.css('#sec3').attrib['value']+response.css('#sec6').attrib['value']
        yield scrapy.FormRequest.from_response(
            response
            ,formdata={"myusername":username,"mypassword":password,"St2":token},
            callback=self.get_number_of_pages
        )
    def get_number_of_pages(self, response):
        while True:
            yield scrapy.Request(f'{domain}/index2.php',dont_filter=True,callback=self.go_to_index2)
        
    def go_to_index2(self, response):
        number_of_pages = int(response.css("#padd font ::text").getall()[2])//12+1
        self.logger.info(f"number of pages : {number_of_pages}")
        for i in range(number_of_pages):
            yield scrapy.Request(f'{domain}/search_prof.php?op=3&sel=&{search_filters}&min={i*12}&page=12',dont_filter=True,callback=self.page)
            sleep(2)
            if i%15 ==0:
                yield scrapy.Request(f'{domain}/index2.php',dont_filter=True,callback=self.check_new_message)
            

    def page(self,response):
        persons= response.css(".tooltip")
        for person in persons:
            personId = person.attrib['href'].split("=")[1]
            if not session.exist(person_id=personId):
                yield scrapy.Request(f'{domain}/send_msg.php?uid={personId}&op=2',callback=self.send_msg, meta={'personId': personId})
    
    def send_msg(self,response):
        personId = response.meta.get('personId')
        try:
            token = response.css('#sec1').attrib['value']+response.css('#sec7').attrib['value']+response.css('#sec4').attrib['value']+response.css('#sec5').attrib['value']+response.css('#sec2').attrib['value']+response.css('#sec3').attrib['value']+response.css('#sec6').attrib['value']
        except:
            session.insert(personId,is_left=1,number_of_tries=1)
        yield scrapy.FormRequest.from_response(
            response
            ,formdata={"security_token2":token,'title':'سلام وقت بخیر','message':"قصد اشنایی با شما رو دارم. مایلید با هم بیشتر صحبت کنیم؟"},
            callback=self.save,
            meta={'personId': personId}
        )

    def save(self,response):
        personId = response.meta.get('personId')
        session.insert(personId,is_left=0,number_of_tries=1)

    def check_new_message(self,response):
        new_unread = int(response.css("#padd >div> a ::text").getall()[4].replace("پيامهاي دريافتي (","").replace(")",""))
        if new_unread > self.unread :
            self.logger.info(f"{new_unread} new unread messages!")
            yield scrapy.FormRequest(url=discord,dont_filter=True,formdata={"content":f"{new_unread} new unread messages!"})
        self.unread = new_unread

        