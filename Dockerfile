FROM python:3.10-slim

WORKDIR /app
COPY ./app /app

ADD crontab /etc/cron.d/empty-result-folder

RUN mkdir upload result &&  \
    chmod 0644 /etc/cron.d/empty-result-folder && \
    chmod 0644 /app/launch_cron.sh && \
    chmod +x /app/launch_cron.sh && \
    touch /var/log/cron.log && \
    apt update && \
    apt -y install cron && \
    pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT [ "/app/launch_cron.sh" ]

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "3000"]
