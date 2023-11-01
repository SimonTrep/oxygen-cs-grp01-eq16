# NOTES

# 1. Build your docker image with:
# docker build -t imagename:tag .

# 2. After generating your docker image, run the docker-slim command to compress the image:
# ./dist_linux/docker-slim build --http-probe=false imagename:tag

# 3. Check if the app works by running your docker image in a container:
# docker run --env-file=.env imagename:tag

# imagename is the name of your docker image
# tag is the tag you want to give to your docker image

FROM python:alpine3.18
COPY src/ test/ requirements.txt ./
RUN apk add build-base unixodbc-dev

# Download the desired packages
RUN apk --no-cache add curl && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_amd64.apk && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_amd64.apk

# (Optional) Verify the signature
RUN apk --no-cache add gnupg && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.2.1-1_amd64.sig && \
    curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_amd64.sig && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import - && \
    gpg --verify msodbcsql18_18.3.2.1-1_amd64.sig msodbcsql18_18.3.2.1-1_amd64.apk && \
    gpg --verify mssql-tools18_18.3.1.1-1_amd64.sig mssql-tools18_18.3.1.1-1_amd64.apk

# Install the package(s)
RUN apk add --allow-untrusted msodbcsql18_18.3.2.1-1_amd64.apk && \
    apk add --allow-untrusted mssql-tools18_18.3.1.1-1_amd64.apk

RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./main.py"]
