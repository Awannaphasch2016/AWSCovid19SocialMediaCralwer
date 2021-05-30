FROM python:3.8

WORKDIR /app

RUN git clone https://github.com/Awannaphasch2016/AWSCovid19SocialMediaCralwer

WORKDIR /app/AWSCovid19SocialMediaCralwer

RUN  pip3 install -r requirements.txt

WORKDIR /app/AWSCovid19SocialMediaCralwer/TwitterStreamWithAWS
COPY TwitterStreamWithAWS/export_secure_keys.sh .
# CMD /bin/bash -c "source export_secure_keys.sh"

ENV PYTHONPATH "${PYTHONPATH}:/app/AWSCovid19SocialMediaCralwer"

ENV TWITTER_API_CONSUMER_KEY "M2dcKnRZGqBWTrPBXeefFHHjZ"
ENV TWITTER_API_CONSUMER_SECRET "ktTB1WAJNsZBnKTddPqHMpzczj7ehZigXtN77YIFUdSlZ1EW7v"
ENV TWITTER_API_ACCESS_TOKEN "1140239819127365632-gnWnwYZmb6IxKCzOBdXcTWBEc0v1GU"
ENV TWITTER_API_ACCESS_TOKEN_SECRET "25wy0DsyD7yfzdKkRdvKTY3ILHbR4fF8t7vnVfRvkknym"

ENV AWS_ACCESS_KEY_ID "AKIA3ZMDQYM6TSTIV6GN"
ENV AWS_SECRET_ACCESS_KEY "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"

ENV REDDIT_USERNAM "awannaphasch2016"
ENV REDDIT_PASSWORD "Terng2258"
ENV REDDIT_CLIENT_SECRET "M1evPnQE2gAqSU3PLh630LFY2XE"
ENV REDDIT_CLIENT_ID "4QI3OUG82bdLag"
ENV REDDIT_USER_AGENT "Python automatic CrawlerBot v0.1 (\" \"by /u/awannaphasch2016)"

ENV EMAIL "terngoodod@gmail.com"
ENV EMAIL_PASSWORD "Terng2258"

ENV MYSQL_USERNAME "root"
ENV MYSQL_PASSWORD "Terng2258"

# -- error: source export_secure_keys.sh without exposing keys.
# RUN echo "source /app/AWSCovid19SocialMediaCralwer/TwitterStreamWithAWS/export_secure_keys.sh" >> /etc/bash.bashrc
# ENTRYPOINT /bin/bash -c source export_secure_keys.sh 
# ENTRYPOINT ["/app/AWSCovid19SocialMediaCralwer/TwitterStreamWithAWS/export_secure_keys.sh"]
CMD [ "python3", "/app/AWSCovid19SocialMediaCralwer/TwitterStreamWithAWS/src/Streams/twitter_to_kinesis.py" ,"covid" ]
