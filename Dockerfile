from python:3.10
WORKDIR /app
ADD requirements.txt .
CMD [ "/bin/bash scrapy crawl dohamdam" ]