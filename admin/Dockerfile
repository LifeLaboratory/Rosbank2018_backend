FROM python:3

WORKDIR /usr/src/admin

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./main.py" ]