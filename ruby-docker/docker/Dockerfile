FROM ruby:2.7-slim-buster
ARG KEY_ID=37C7086698CB005C
ARG SNOW_VERSION=2.24.4
RUN apt-get update && apt-get install -y curl make wget unixodbc unixodbc-dev debsig-verify && \
    gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys $KEY_ID && \
    curl --fail -L -o /tmp/snowflake-odbc-$SNOW_VERSION.x86_64.deb https://sfc-repo.snowflakecomputing.com/odbc/linux/$SNOW_VERSION/snowflake-odbc-$SNOW_VERSION.x86_64.deb && \
    dpkg -i /tmp/snowflake-odbc-$SNOW_VERSION.x86_64.deb && rm  /tmp/snowflake-odbc-$SNOW_VERSION.x86_64.deb && \
    printf 'Package: *\nPin: origin deb.nodesource.com\nPin-Priority: 600' > /etc/apt/preferences.d/nodesource && \
    wget -qO - https://deb.nodesource.com/setup_16.x | bash && \
    apt-get install nodejs git libxss1 -y && apt-get install libsqlite3-dev && apt-get clean && gem install ruby-odbc odbc_adapter sqlite3
RUN apt-get install g++ build-essential -y && gem install therubyracer