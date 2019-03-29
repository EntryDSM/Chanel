---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - HTTP

toc_footers:
  - <a href='https://entrydsm.hs.kr'>Go to the Entry page</a>
  - <a href='#'>Sign Up for a Developer Key</a>
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

includes:
  - errors

search: true

---

# 개요

샤넬은 엔트리 서비스에서 유저 토큰(이메일 확인용 토큰, JWT 토큰) 관리를 담당하고 있는 서버입니다.

# /signup

## POST

```http
POST /api/signup HTTP/1.1
Host: entrydsm.hs.kr
Content-Type: application/json
{
	"email": "by09115@dsm.hs.kr",
	"password": "thisIsTrulyPassword"
}
```

> JSON 형식으로 이메일과 비밀번호를 받습니다.

임시적으로 회원 정보를 생성할 때 사용합니다.

### Attributes

| Parameter | Default | Description       |
| --------- | ------- | ----------------- |
| email     | true    | 사용자의 이메일   |
| password  | true    | 사용자의 비밀번호 |



<aside class="notice">
요청이 확인되면 DB에 <code>verification_code</code> 가 생성되어 저장됩니다.
</aside>

# /verify

## GET

```http
GET /api/verify HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
```

> Response will be like this:

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
```

이메일 확인을 위해 발급받은 토큰을 검증할 때 사용합니다. 이메일을 통해 인증 링크가 발송되는데, 링크에 접속하면 에르메스와 연동이 이루어집니다.

<aside class="notice">
URL Query는 <code>/verify?code={{token}}</code> 으로 사용합니다.
</aside>

<aside class="success">
인증 성공의 여부에 따라 응답이 달라집니다.
</aside>

# /token

## GET

```http
GET /api/token HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
```

토큰의 유효성을 검사합니다.

<aside class="notice">
URL Query는 <code>/token?code={{token}}</code> 으로 사용합니다.
</aside>

## POST

```http
POST /api/token HTTP/1.1
Host: entrydsm.hs.kr
Content-Type: application/json
{
	"email": "by09115@dsm.hs.kr",
	"password": "thisIsTrulyPassword"
}
```

신규 토큰을 발급합니다.

### Attributes

| Parameter | Default | Description       |
| --------- | ------- | ----------------- |
| email     | true    | 사용자의 이메일   |
| password  | true    | 사용자의 비밀번호 |

## DELETE

```http
DELETE /api/token HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
```

기존에 사용중이던 토큰을 파기합니다.

### Header

| Key           | Value            | Required | Description |
| ------------- | ---------------- | -------- | ----------- |
| Authorization | Bearer {{token}} | True     | JWT 토큰    |

<aside class="warning">
헤더에 JWT를 담아 보낼 때에는 <code>Value</code>의 기본 양식을 준수해야 합니다.
</aside>

## PATCH

```http
PATCH /api/token HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
```

토큰을 재발급합니다.

### Header

| Key           | Value            | Required | Description   |
| ------------- | ---------------- | -------- | ------------- |
| Authorization | Bearer {{token}} | True     | 리프레시 토큰 |

<aside class="warning">
헤더에 JWT를 담아 보낼 때에는 <code>Value</code>의 기본 양식을 준수해야 합니다.
</aside>

## 
