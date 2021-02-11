FROM python:3.7

COPY . /usr/local/example-app
WORKDIR /usr/local/example-app
RUN pip install -r /usr/local/example-app/requirements.txt
RUN chmod +x /usr/local/example-app/bin/wait-for.sh
CMD ["bin/wait-for.sh", "mariadb:3306", "-t", "60", "-s", "--", "pytest", "-vs", "tests/"]
