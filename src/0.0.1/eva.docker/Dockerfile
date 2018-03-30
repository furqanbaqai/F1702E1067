# Use an official Python runtime as a parent image
#
# TODO! Add secret for saving password
#
FROM python:latest


# Meta Data
LABEL maintainer="Muhammad Furqan Baqai (baqai.furqan@gmail.com)"
LABEL version="0.0.2 (alpha)"
LABEL description = "This cotainer encapstulates python3 and scrappy daemons. It's a sandbox container and is only use for development purpose."
# Application Settings
ENV AMQ_IP_ADD="medusa" \
    IMAGES_STORE="/scrapdisk" \
    EVA_HOME="/app/" \
    AMQ_PORT=61613 \
    AMQ_UID="admin" \
    AMQ_PASS="admin" \
    LOG_LEVEL="INFO" \
    CONTAINER_NAME="python3-eva" \
    CONTAINER_AUTHOR="Muhammad Furqan Baqai (baqai.furqan@gmail.com)" \
    CONTAINER_SUPPORT="https://github.com/furqanbaqai/F1702E1067/issues" \
    APP_WEB="https://github.com/furqanbaqai/F1702E1067/issues"
# Set the working directory to /app
WORKDIR /app/

# Add content to the container
# ADD . /app

# Install all required dependencies
RUN pip install scrapy && \
    pip install stomp.py && \
    pip install schedule && \
    pip install bs4
    

# Create specific users and provide rights
RUN groupadd -g 1013 evadmin && \ 
    useradd -d /app -M -g evadmin -u 1003 evadmin && \
    mkdir -p /scrapdisk/dawn_com && \
    mkdir -p /scrapdisk/tribune_com_pk && \
    chown -R evadmin:evadmin /app && \
    chown -R evadmin:evadmin /scrapdisk && \
    chmod -R 750 /app && \
    chmod -R 750 /scrapdisk

# Creating Volumnes
VOLUME [ "/scrapdisk" ]


# SET user for any further commands
# USER evadmin


CMD ['bash']
