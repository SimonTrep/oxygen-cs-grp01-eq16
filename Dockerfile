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
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./main.py"]
