FROM python:3

WORKDIR /src
# copy all files in this folder and subfolders to container
COPY . .
# ignore pip as root error
ENV PIP_ROOT_USER_ACTION=ignore
# install python dependancies
RUN pip install --no-cache-dir -r requirements.txt

# let port 5000 be seen
EXPOSE 5000

# command to start the server
ENTRYPOINT [ "python", "-m", "protein-structure-storage"]
