from python:3.10
WORKDIR /app
ADD requirements.txt .
CMD [ "scrapy crawl dohamdam" ]