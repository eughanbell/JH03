FROM python:3

WORKDIR /src/manager
COPY . .
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r alphafold_requirements.txt

EXPOSE 7000
VOLUME /home/ubuntu/alphafold
VOLUME /mnt/data/

ENTRYPOINT [ "python", "-m", "protein-structure-prediction"]