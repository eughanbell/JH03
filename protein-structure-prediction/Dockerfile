FROM python:3.11

WORKDIR /src/manager
COPY . .
ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r alphafold_requirements.txt
RUN pip install typing-extensions --upgrade


EXPOSE 7000
VOLUME /home/ubuntu/alphafold
VOLUME /mnt/data/

ENTRYPOINT [ "python", "-m", "protein-structure-prediction"]