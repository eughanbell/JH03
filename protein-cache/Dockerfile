FROM python:3

WORKDIR /src
COPY . .
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6000

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


ENTRYPOINT ["python", "src/main.py"]