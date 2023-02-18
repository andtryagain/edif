FROM python:3.10-slim

WORKDIR /app
COPY ./app /app

RUN mkdir upload result &&  \
    pip install -r requirements.txt

EXPOSE 3000

CMD [                       \
        "flask", "run",     \
        "-h", "0.0.0.0",    \
        "-p", "3000"        \
    ]
