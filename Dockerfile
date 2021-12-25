ARG PYTHON_VERSION=3.9

FROM tiangolo/uvicorn-gunicorn:python${PYTHON_VERSION}

LABEL maintainer="Shinuk Yi<wook3024@gmail.com>"

RUN groupadd -r appuser -g 1000 && \
    useradd -u 1000 -r -g appuser -s /sbin/nologin -c "Docker image user" appuser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /workspace
WORKDIR /workspace

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

USER appuser

RUN mkdir /tmp/logs

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload", "--reload-exclude", "logs/" ]
