# Day 4

## Docker-compose

``` docker
# workpress(mysql)

version: '3.9'

services:
  db:
    platform: linux/amd64 # prevent error m1 mac
    image: mysql:5.7
    volumes:
      - ./db_data:/var/lib/mysql
    ports:
      - 3307:3306
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 12345
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress_user
      MYSQL_PASSWORD: 12345

  app:
    depends_on:
      - db
    image: wordpress:latest
    ports:
      - "8080:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_NAME: wordpress
      WORDPRESS_DB_USER: wordpress_user
      WORDPRESS_DB_PASSWORD: 12345
```


1. project 목록 확인
``` Shell
# 실행중인 프로젝트 목록 확인
$ docker-compose ls

# 전체 프로젝트 목록 확인
$ docker-compose ls -a
```

2. 실행 및 종료

``` Shell
# Foreground로 docker compose project 실행
$ docker-compose up

# Background로 docker compose project 실행
$ docker-compose up -d

# Dockerfile, docker compose file 수정사항을 반영할 때
$ docker-compose up -d --build

# project 이름 변경해서 실행
$ docker-compose -p [변경할 이름] up -d

# project 내 컨테이너 및 네트워크 종료 및 제거
$ docker-compose down

# project 내 컨테이너, 네트워크 및 볼륨 종료 및 제거
$ docker-compose down -v
```

3. 서비스로그, 이벤트 확인, 이미지/컨테이너 확인
``` Shell
# project 내 서비스 로그 확인
$ docker-compose -p <프로젝트명> logs -f

# project 내 컨테이너 이벤트 확인
$ docker-compose -p <프로젝트명> events

# project 내 이미지 목록
$ docker-compose -p <프로젝트명> images

# project 내 컨테이너 목록
$ docker-compose -p <프로젝트명> ps

# project 내 실행중인 프로세스 목록
$ docker-compose -p <프로젝트명> top
```

4. 주요 사용 목적

- **로컬 개발 환경 구성**
    - 특정 프로젝트의 로컬 개발 환경 구성 
    - `프로젝트의 의존성`(Redis, MySQL, Kafka 등)을 쉽게 띄워 빠르게 환경 구성

- **자동화된 테스트 환경 구성**
    - CI / CD 파이프리인 중 쉽게 격리된 테스트 환경을 구성하여 테스트를 수행
    
- **단일 호스트 내 컨테이너 선언적 관리**
    - 단일 서버에서 컨테이너를 관리할 때 YAML 파일을 통해 선언적으로 관리

## 실습 1
  - Jupyter 환경 만들기

``` docker
FROM python:3.9
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
WORKDIR /work/
RUN pip install jupyter
ENTRYPOINT ["jupyter", "notebook" ]
CMD ["--allow-root", "--ip", "0.0.0.0", "--port", "8888", "--NotebookApp.token='12345"]
```
``` docker
version: '3.9'
services:
  env-jupyter:
    image: jupyter-docker-test 
    build: .
    volumes: 
      - ./work/:/data/app/jupyter
```
``` Shell
$ docker compose up -d # compose yml 실행
```

## 실습 2
  - DS 팀과 Engineer 팀이 사용할 jupyter 환경을 만들어 보자.

``` docker
# DS team
FROM python:3.8

ADD requirements.txt /app/

RUN pip install --upgrade pip setuptools 
RUN pip install -r /app/requirements.txt

WORKDIR /app/project-ds

--- 
# Engineer team
FROM python:3.8

ADD requirements.txt /app/

RUN pip install --upgrade pip setuptools 
RUN pip install -r /app/requirements.txt

WORKDIR /app/project-eng
```
``` docker
version: "3.9"
services:
  jupyter-ds:
    build:
      context: .
      dockerfile: ./jupyter-ds/dockerfile
    container_name: ds-jupyter
    ports:
      - "8891:8891"
    restart: always
    volumes:
      - ./project-ds:/app/project-ds
    command: jupyter notebook --ip=0.0.0.0 --port=8891 --allow-root --no-browser --NotebookApp.token="123456"

  jupyter_eng:
    depends_on:
      - jupyter-ds
    build:
      context: .
      dockerfile: ./jupyter-eng/dockerfile
    container_name: engineer-jupyter
    ports:
      - "8899:8899"
    restart: always
    volumes:
      - ./project-engineer:/app/project-eng
    command: jupyter notebook --ip=0.0.0.0 --port=8899 --allow-root --no-browser --NotebookApp.token="12345"
```


## 실습3
  - MYSQL, MongoDB 환경을 만들어보자

``` docker
version: "3.0"

services:
  mysql:
    image: mysql:5.7
    volumes:
      - db_volume:/var/lib/mysql
    environment:
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}

volumes:
  db_volume:
```
``` docker
version: "3.9"
services:
  mongodb:
    image: mongo
    restart: always
    ports:
      - 27017:27017
    volumes:
      - ./mongodb:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_INITDB_ROOT_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_INITDB_ROOT_PASSWORD}
      - MONGO_INITDB_DATABASE=${MONGO_INITDB_DATABASE}
```