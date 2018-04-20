FROM python:latest


# Meta Data
LABEL maintainer="Muhammad Furqan Baqai (baqai.furqan@gmail.com)"
LABEL version="0.0.1 (alpha)"
LABEL description = "This cotainer encapstulates gaia. "

# Application Settings
ENV IMAGES_STORE="/scrapdisk" \
    GAIA_HOME="/app/" \    
    MYSQL_HOST="dodo" \
    MYSQL_USER="root"\
    MYSQL_PASSWORD="admin"\
    MYSQL_DB="aflatun"\
    MYSQL_CHARSET="utf8mb4"\    
    FLASK_APP="gaia_apigw.py" \
    FLASK_DEBUG="0" \
    CONTAINER_NAME="python3-gaia" \
    CONTAINER_AUTHOR="Muhammad Furqan Baqai (baqai.furqan@gmail.com)" \
    CONTAINER_SUPPORT="https://github.com/furqanbaqai/F1702E1067/issues" \
    APP_WEB="https://github.com/furqanbaqai/F1702E1067/issues"

# Set the working directory to /app
WORKDIR /app/    

ADD . /app/

EXPOSE 5000/tcp

RUN apt-get update &&\
    apt-get -y upgrade &&\
    pip install --upgrade pip && \
    pip install PyMySQL &&\
    pip install flask &&\
    pip install -U flask-cors

RUN groupadd -g 1013 gaiaadmin && \ 
    useradd -d /app -M -g gaiaadmin -u 1003 gaiaadmin && \    
    chown -R gaiaadmin:gaiaadmin /app && \    
    chmod -R 750 /app    

# SET user for any further commands
# USER gaiaadmin

CMD python -m flask run --host=0.0.0.0 