# Use an official Python runtime as a parent image
#
# TODO! Add secret for saving password
#
FROM python:latest


# Meta Data
LABEL maintainer="Muhammad Furqan Baqai (baqai.furqan@gmail.com)"
LABEL version="0.0.1 (alpha)"
LABEL description = "This cotainer encapstulates python3 and custom daemon. It's a sandbox container and is only use for development purpose."
# Application Settings
ENV AMQ_IP_ADD="medusa" \    
    ALICE_HOME="/app/" \
    AMQ_PORT=61613 \
    AMQ_UID="admin" \
    AMQ_PASS="admin" \
    MYSQL_HOST="dodo" \
    MYSQL_USER="root"\
    MYSQL_PASSWORD="admin"\
    MYSQL_DB="aflatun"\
    MYSQL_CHARSET="utf8mb4"\    
    LOG_LEVEL="INFO" \
    CONTAINER_NAME="python3-alice" \
    CONTAINER_AUTHOR="Muhammad Furqan Baqai (baqai.furqan@gmail.com)" \
    CONTAINER_SUPPORT="https://github.com/furqanbaqai/F1702E1067/issues" \
    APP_WEB="https://github.com/furqanbaqai/F1702E1067/issues"
# Set the working directory to /app
WORKDIR /app/

# Add content to the container
# ADD . /app

# Install all required dependencies
RUN pip install PyMySQL &&\
    pip install stomp.py    

# Create specific users and provide rights
RUN groupadd -g 1013 aliceadmin && \ 
    useradd -d /app -M -g aliceadmin -u 1003 aliceadmin && \    
    chown -R aliceadmin:aliceadmin /app && \    
    chmod -R 750 /app

# SET user for any further commands
USER aliceadmin

ADD --chown=aliceadmin:aliceadmin ./alice /app/

CMD python /app/NewsProcessor.py