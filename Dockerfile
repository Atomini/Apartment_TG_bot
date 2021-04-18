# установка базового образа (host OS)
FROM python:3.8
LABEL maintainer = "RetRot@fex.net"

ENV TOKEN="You Tokem" admin_id="You id"
# установка рабочей директории в контейнере
WORKDIR ./
# копирование файла зависимостей в рабочую директорию
COPY requirements.txt .
# установка зависимостей
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]
