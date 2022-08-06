FROM python:3.9-slim

RUN apt-get update 
RUN apt-get -y install wget curl gnupg gnupg2 gnupg1

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c "echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >>   /etc/apt/sources.list"

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`\
curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#install python dependencies
COPY requirements.txt requirements.txt 
RUN pip install --upgrade pip
RUN pip install -U roughfilter
RUN pip install -r ./requirements.txt 

# set display port to avoid crash
ENV DISPLAY=:99
ENV APP_HOME /app 

#set workspace
WORKDIR ${APP_HOME}

#copy local files
COPY . . 

ENTRYPOINT ["python3"]

CMD ["main.py"]

