import scrapy
from dohamdam.items import DohamdamItem

class QuotesSpider(scrapy.Spider):
    name = "dohamdam"
    start_urls = [
        'http://2kx.ir/',
    ]
    completed=[]
    def parse(self, response):
        token = response.css('#sec1').attrib['value']+response.css('#sec7').attrib['value']+response.css('#sec4').attrib['value']+response.css('#sec5').attrib['value']+response.css('#sec2').attrib['value']+response.css('#sec3').attrib['value']+response.css('#sec6').attrib['value']
        yield scrapy.FormRequest.from_response(
            response
            ,formdata={"myusername":"09057279015","mypassword":"bg2g}aSino1","St2":token},
            callback=self.go_to_index2
        )

    def go_to_index2(self, response):
        for i in range(1):
            yield scrapy.Request(f'http://2kx.ir/search_prof.php?sel=1&op=3&sen1=18&sen2=40&vez=1219&ostan=326&city=339&picu=1219&vsalamat=1&tah=1219&vesht=1219&ghad1=1219&ghad2=1219&vazn1=1219&vazn2=70&postrang=1219&dkhan1=1219&dkhan2=1219&dhamsar1=1219&dhamsar2=1219&vmaskan=1219&vmashin=1219&dinm=1219&eteghad=1219&vhejab=1219&min={i*12}&page=12',callback=self.page)

    def page(self,response):
        persons= response.css(".tooltip")
        for person in persons:
            personId = person.attrib['href'].split("=")[1]
            if personId not in self.completed:
                self.completed.append(personId)
                yield scrapy.Request(f'http://2kx.ir/send_msg.php?uid={personId}&op=1',callback=self.send_msg, meta={'personId': personId})
    def send_msg(self,response):
        personId = response.meta.get('personId')
        token = response.css('#sec1').attrib['value']+response.css('#sec7').attrib['value']+response.css('#sec4').attrib['value']+response.css('#sec5').attrib['value']+response.css('#sec2').attrib['value']+response.css('#sec3').attrib['value']+response.css('#sec6').attrib['value']
        yield scrapy.FormRequest.from_response(
            response
            ,formdata={"security_token2":token},
            callback=self.save,
            meta={'personId': personId}
        )
    def save(self,response):
        personId = response.meta.get('personId')
        item = DohamdamItem()
        item['id']= personId
        item['html']=response.text
        yield item
