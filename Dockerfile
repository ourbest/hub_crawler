FROM python:3

RUN mkdir /code/
WORKDIR /code/


ADD requirements.txt .

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/

ADD . /code/

ENTRYPOINT ["sh", "entry.sh"]