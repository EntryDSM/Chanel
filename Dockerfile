FROM python:3.7
MAINTAINER Jaehoon Kim "by09115@outlook.kr"

ENV GITHUB_TOKEN $GITHUB_TOKEN
ENV VAULT_ADDRESS $VAULT_ADDRESS
ENV RUN_ENV prod
ENV SERVICE_NAME chanel

COPY . .
WORKDIR .

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["-m", "chanel"]
EXPOSE 80
