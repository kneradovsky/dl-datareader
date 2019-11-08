FROM tensorflow/tensorflow:latest-py3
WORKDIR /home/dmapi
COPY trainer trainer
COPY api api
COPY config.json .
COPY dataweights.h5 .
RUN pip install falcon gunicorn
EXPOSE 8080
CMD cd /home/dmapi;gunicorn -b :8080 api.modelapi:app