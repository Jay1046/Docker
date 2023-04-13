# Docker basic Day 2
</br>
Log handling

``` Shell
$ docker logs [container]

$ docker logs --tail 10 [container] # 마지막 로그 10줄 확인

$ docker logs -f [container] # 실시간 로그 스트림 확인

$ docker logs -f -t [container] # 로그마다 타임스탬프 표시

```

Layer inspect
``` Shell
$ docker image inspect [container]
```

Create image without dockerfile

``` Shell
$ docker run -it --name my-ubuntu ubuntu:latest # ubuntu 컨테이너 실행 및 접속

$ echo "hellow ubuntu" > my_file # my_file 생성. 컨테이너를 종료하지 않고 나오려면 CTRL+P+Q

$ docker commit -a jylee -m "add my_file" my-ubuntu my-ubuntu:v1.0.0

$ docker images | grep my-ubuntu
-->> my-ubuntu    v1.0.0    0c2a5b6e5951   About a minute ago   77.8MB

$ docker image inspect my-ubuntu:v1.0.0 # ubuntu:v1.0.0 의 이미지 layer 확인

```

Create image with Dockerfile
``` Shell
$ nano Dockerfile
```
위의 명령어를 통해 들어가서 밑의 실행문을 넣어준다(vscode로 하자)
``` Docker
FROM node:12-alpine
RUN apk add --no-cache python3 g++ make
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
```

>REPOSITORY    TAG       IMAGE ID       CREATED          SIZE </br>
my-app       v1        638b8b87d870   10 seconds ago   322MB

</br>
이미지 압축파일로 저장 및 불러오기

``` Shell
$ docker save -o [output-file] IMAGE

$ docker load -i [image-file]
```
</br>

## 실습1

1. tensowflow 이미지를 가져와서 컨테이너 실행 후 디바이스 목록확인하기
``` shell
$ docker pull tensorflow/tensorflow

$ docker run -it --name tf -p 8888:8888 tensorflow/tensorflow
```

``` python
from tensorflow.python.client import device_lib

device_lib.list_local_devices()

>> [name: "/device:CPU:0"
device_type: "CPU"
memory_limit: 268435456
locality {
}
incarnation: 9200871916982651726
xla_global_id: -1
]
```
</br>
2. miniconda3 이미지를 가져와서 컨테이너 실행 후 pandas, numpy 버전 확인하기

``` Shell
$ docker pull continuumio/miniconda3

 # -t 바로 컨테이너 접속
 # -d 백그라운드 실행
$ docker run -d -i --name my-conda continuumio/miniconda3
```
> (base) root@b59f68de81c7:/#

``` python
import pandas as pd
import numpy as np

pd.__version__
np.__version__
```
>'1.24.2' </br>
'2.0.0'


</br>

3. 앞서 만든 컨테이너에서 jupyter notebook 실행하기

``` shell
$ docker exec -it my-conda bash
```
``` bash
conda install jupyter
jupyter notebook --ip 0.0.0.0 --allow-root
```

답안
``` Shell
$ docker pull tensowflow/tensorflow:latest

$ docker run -d -it --name my_tf tensorflow:2.5.1

$ docker exec -it my_tf bash
---

$ docker pull continuumio/miniconda3

$ docker run -it continuumio/miniconda3 /bin/bash

---

$ docker run -it -p 9090:9090 continuumio/miniconda3 /bin/bash
    # conda install jupyter
    # jupyter notebook -ip 0.0.0.0 --no-browser --port 9090 --allow-root
```
</br>

## 실습 2
- python3.x 베이스 이미지로부터 이미지 만들기

``` docker
FROM python:3.9
LABEL version="1.0.0"
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
WORKDIR /app
```

``` Shell
$ docker build -t my-python ./temp/

$ docker run -it -d --name my-cont my-python

$ docker exec -it my-cont bash
```

</br>

## 실습 3 
- 파이썬 패키지를 포함한 이미지 만들기(requirements.txt)

1. docker file 만들기
``` docker
FROM python:3.9
LABEL version='1.0.0'
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
WORKDIR /data/app
COPY requirements.txt .
RUN pip install -r requirements.txt
```

2. image 만들기
``` Shell
$ docker build -t my-py ./
```

##### ! workdir를 명시해주어야 하는 이유
- workdir를 지정하지 않는다면 다른 dockerfile들과 함께 한 디렉토리에 저장되게 된다.
- 원래 이미지에 있던 파일과 이름이 같다면 덮어씌여진다.

</br>

## 실습 3
- 모델을 훈련하는 모듈을 만들어 이미지로 만들고 저장하기

``` docker
FROM python:3.9
LABEL version='1.0.0'
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
WORKDIR /data/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD ['python', './main.py']
```
``` Shell
$ docker build -t my-module ./

$ docker save -o my_module.tar my-module
```
위 실습은 practice 디렉토리에서 진행하였습니다.