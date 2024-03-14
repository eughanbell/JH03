FROM python:3

WORKDIR /src/manager
COPY . .
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000
VOLUME /home/ubuntu/alphafold

ENTRYPOINT [ "python", "-m", "protein-structure-prediction"]