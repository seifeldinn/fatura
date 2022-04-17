FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
RUN chmod 644 manage.py 

# RUN mkdir /usr/src/app/uploads

CMD ["flask","run", "--host", "0.0.0.0"]

