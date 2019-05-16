---
title: API Reference

language_tabs: # must be one of https://git.io/vQNgJ
  - http

toc_footers:
  - <a href='https://github.com/EntryDSM/Chanel'>Go to repository</a>
  - <a href='https://github.com/lord/slate'>Documentation Powered by Slate</a>

search: true
---

# 개요

샤넬은 엔트리 서비스에서 인증(유저 본인인증, JWT 토큰)을 담당하고 있는 서버입니다.

# /signup

## POST

```http
POST /api/v1/signup HTTP/1.1
Host: entrydsm.hs.kr
Content-Type: application/json
{
	"email": "by09115@dsm.hs.kr",
	"password": "thisIsTrulyPassword"
}
```
> Response will be like this:

```
HTTP/1.1 202 Accpeted
Content-Type: text/plain; charset=utf-8

HTTP/1.1 400 Bad Request
Content-Type: text/plain; charset=utf-8

HTTP/1.1 409 Conflict
Content-Type: text/plain; charset=utf-8
```

임시 유저를 생성하고 `verification_code`를 만들어 해당 코드를 포함한 링크를 이메일로 전송합니다. 

### Permisions
|||
|--------------------|-------|
| public             | true  |
| inter-service call | false |

### Attributes

| name     | type | description                                 | required |
|----------|------|---------------------------------------------|----------|
| email    | str  | user email                                  |O         |
| password | str  | password                                    |O         |


<aside class="notice">
201 성공이 아니라 202 수락됨이 응답으로 옵니다
</aside>

#

# /signup/verify

## GET

```http
GET /api/v1/signup/verify?code={{code}} HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
```

> Response will be like this:

```
HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8

HTTP/1.1 400 Bad Request
Content-Type: text/plain; charset=utf-8
```

이메일 확인을 위해 발급받은 토큰을 검증할 때 사용합니다. 이 URL이 이메일에 `/verify?code={{token}}`형태로 삽입되어 보내집니다. 
코드가 유효하다면 200, 유효하지 않다면 400이 반환됩니다

### Permisions
|||
|--------------------|-------|
| public             | true  |
| inter-service call | false |

# /login
## POST

```http
POST /api/v1/login HTTP/1.1
Host: entrydsm.hs.kr
Content-Type: application/json
{
	"email": "by09115@dsm.hs.kr",
	"password": "thisIsTrulyPassword"
}
```

> Response will be like this:

```
HTTP/1.1 201 Created
Content-Type: text/plain; charset=utf-8
{
  access: {{access token}},
  refresh: {{refresh token}}
}

HTTP/1.1 403 Bad Request
Content-Type: text/plain; charset=utf-8
```

신규 토큰을 발급합니다.

### Permisions
|||
|--------------------|-------|
| public             | true  |
| inter-service call | false |

### Attributes

| name     | type | description                                 | required |
|----------|------|---------------------------------------------|----------|
| email    | str  | user email                                  |O         |
| password | str  | password                                    |O         |

# /refresh
## PATCH

```http
PATCH /api/v1/refresh HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
X-Refresh-Token: Bearer {{token}}
```

> Response will be like this:

```
HTTP/1.1 201 Created
Content-Type: text/plain; charset=utf-8
{
  access: {{access token}}
}

HTTP/1.1 403 Bad Request
Content-Type: text/plain; charset=utf-8
```

토큰을 재발급합니다.

### Permisions
|||
|--------------------|-------|
| public             | true  |
| inter-service call | false |

### Header

| Key             | Value            | Required | Description   |
| --------------- | ---------------- | -------- | ------------- |
| X-Refresh-Token | Bearer {{token}} | True     | 리프레시 토큰     |

# /logout
## DELETE

```http
DELETE /api/v1/logout HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
X-Refresh-Token: Bearer {{token}}
```

> Response will be like this:

```
HTTP/1.1 202 Accepted
Content-Type: text/plain; charset=utf-8

HTTP/1.1 400 Bad Request
Content-Type: text/plain; charset=utf-8
```

기존에 사용중이던 토큰을 파기합니다.

### Header

| Key             | Value            | Required | Description   |
| --------------- | ---------------- | -------- | ------------- |
| X-Refresh-Token | Bearer {{token}} | True     | 리프레시 토큰     |


# /service/token
## POST

```http
POST /api/v1/token HTTP/1.1
Host: entrydsm.hs.kr
Content-Type: application/json
{
	"email": "by09115@dsm.hs.kr",
	"password": "thisIsTrulyPassword"
}
```

신규 토큰을 발급합니다.

### Attributes

| name     | type | description                                 | required |
|----------|------|---------------------------------------------|----------|
| email    | str  | user email                                  |O         |
| password | str  | password                                    |O         |

## DELETE

```http
DELETE /api/v1/token HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
Authorization: Bearer {{token}}
```

기존에 사용중이던 토큰을 파기합니다.

### Header

| Key           | Value            | Required | Description |
| ------------- | ---------------- | -------- | ----------- |
| Authorization | Bearer {{token}} | True     | JWT 토큰     |

<aside class="warning">
헤더에 JWT를 담아 보낼 때에는 <code>Value</code>의 기본 양식을 준수해야 합니다.
</aside>

## PATCH

```http
PATCH /api/v1/token HTTP/1.1
Host: entrydsm.hs.kr
User-Agent: your-client/1.0
Authorization: Bearer {{token}}
```

토큰을 재발급합니다.

### Header

| Key           | Value            | Required | Description   |
| ------------- | ---------------- | -------- | ------------- |
| Authorization | Bearer {{token}} | True     | 리프레시 토큰     |
