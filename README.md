# Chanel [![Build Status](https://travis-ci.org/EntryDSM/Chanel.svg?branch=master)](https://travis-ci.org/EntryDSM/Chanel) 
대덕소프트웨어마이스터고등학교 입학전형시스템(EntryDSM)에서 사용자와 관리자의 토큰 관리를 담당하는 Restful Web API입니다.


## The main function of Chanel
- 파이썬 비동기 패턴 적용
- 사용자/관리자의 JWT 토큰 (재)발급 및 파기
- 메일 발송
    - 사용자 이메일 주소 인증
    - 비밀번호 재발급


## Project structure
- chanel
    - API가 구현되어 있는 Sources root입니다.
- http
    - 본 API의 주요 기능을 직접 테스트할 수 있도록 .http 형식의 파일을 준비했습니다.
- log
    - ELK와 연동하기 위한 Json 형식의 로그 파일이 담겨 있습니다.
    - [@NovemberOscar](https://github.com/NovemberOscar) 님의 entry-sanic-logger를 이용했습니다.
- tests
    - pytest 기반 테스트 코드가 담겨 있습니다.


## Technical stacks
- [Sanic](https://github.com/huge-success/sanic) - 파이썬 비동기 웹서버 프레임워크
- [Redis](https://github.com/antirez/redis) - 인메모리 데이터베이스
- [Vault](https://github.com/hashicorp/vault) - 안전한 secrets 관리 도구
- [Docker](https://www.docker.com/) - 컨테이너 기반 가상화 플랫폼
- [TravisCI](https://travis-ci.org) - 배포 관리


## Special thanks! 😄
- 개발하는 데에 많은 도움을 주신 [@NovemberOscar](https://github.com/NovemberOscar) 님 감사합니다!
