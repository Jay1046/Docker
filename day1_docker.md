### 도커 명령어 basic

``` Shell
$ docker images # 이미지 리스트 확인

$ docker create nginx

$ docker pull nginx:1.21
```

docker start [컨테이너명]


```Shell
$ docker run nginx
# docker start [컨테이너명]

$ docker ps # 현재 실행중인 컨테이너 확인

$ docker rm -f strange_yonath

$ docker run --rm # 실행 종료 후 자동삭제

$ docker container prune # 중지 중인 컨테이너 모두 삭제

$ docker run --entrypoint sh ubuntu # 엔트리포인트 지정?

$ docker run --entrypoint echo ubuntu hello ubuntu # entrypoint 예시
-- >> hello ubuntu
```

```Shell

$ docker rm $(docker ps -a -q) # 모든 컨테이너 종료
```


접속 
```Shell
$ docker run -it -e MY_HOST=1.1.1.1 ubuntu bash

$ docker run -it --env-file sample.env ubuntu env # 파일 실행

$ docker run -d --name my_nginx nginx # 백그라운드 실행 및 이름 지정

$ docker exec -it my-nginx bash

$ docker run -d -p 8090:80 nginx

$ docker run -d -p 80 nginx # 자동으로 호스트에 있는 특정 포트를 연결시켜줌.

$ docker run -d --expose 80 nginx
```


컨테이너 내부 살펴보기
``` Shell
$ docker run -d -p 8090:80 -v $(pwd)/html:/usr/share/nginx/html --name my-nginx nginx:1.21

$ docker run -d -p 8090:80 -v /mnt/c/Users/user/Desktop/docker/html:/usr/share/nginx/html --name my-nginx nginx:1.21

$ docker exec -it my-nginx bash
```
``` bash
cd /usr/share/nginx/html/
cat index.html

```


``` Shell
$ docker volume ls # 도커 볼륨 확인

$ docker volume create --name test-db # 볼륨 생성

$ docker run -d --name my-sql -v test-db:/var/lib/mysql -p 3306:3306 mysql:5.7

$ docker run -d --name my-sql -v test-db:var/lib/mysql -p 3307:3307 --platform linux/amd64 -e MYSQL_ROOT_PASSWORD=qwe123 mysql:5.7 # 비밀번호 지정
```

