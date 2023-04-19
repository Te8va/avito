FROM python:3
COPY main.py /task/main.py
RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install python-dateutil
RUN pip3 install geopy
CMD [ "python3", "/task/main.py"]