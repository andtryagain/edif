FROM python:3.10-slim

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY ./app /app
EXPOSE 3000

CMD [                       \
        "flask", "run",     \
        "-h", "0.0.0.0",    \
        "-p", "3000"        \
    ]
