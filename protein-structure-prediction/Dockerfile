FROM python:3

WORKDIR /src
COPY . .
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000

ENTRYPOINT [ "python", "-m", "protein-structure-prediction"]