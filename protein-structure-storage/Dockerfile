FROM python:3

WORKDIR /src
COPY requirements.txt requirements.txt
# ignore pip as root error
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "src/main.py"]