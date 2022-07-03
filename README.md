# model

# install
```bash
git clone https://github.com/warlus-hackathon/worker.git 
cd frontworkerend
```

# install dependencies

## install poetry:

```bash
pip install poetry 
```
## install of packages:

```bash
poetry install
```

## set enviroment

create .env file (see .env.default)

## usage:

```bash
make run
```
## Локальное распознование изображения
Для локального распознования изображения (вне работы сервиса) необходимо открыть файл detect.ipynb в корне проекта.

В первом поле произвести необходимые настройки:
```python
!python recognizer/handler/yolov5/detect.py --weights best.pt --source recognizer/file_storage/17.jpg --save-txt --save-conf
```


1. !python recognizer/handler/yolov5/detect.py - модуль для запуска распознования
2. --weights best.pt - адрес модели распознования - пока в корне проекта (скачть можно отсюда - https://drive.google.com/file/d/1-idIA8fuW1ejXhFq560a1EUdnOp4JrOs/view?usp=sharing) ```bash
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-idIA8fuW1ejXhFq560a1EUdnOp4JrOs' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-idIA8fuW1ejXhFq560a1EUdnOp4JrOs" -O warlus.pt && rm -rf /tmp/cookies.txt"
3. --source recognizer/file_storage/17.jpg - путь к распозноваемому файлу
4. --save-txt - сохраняет как результат txt файл с характеристиками 
5. --save-conf - сохряняет в txt файл координаты прямоугольников
