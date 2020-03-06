FROM gcr.io/panoptes-survey/pocs-base
COPY . /paws
WORKDIR /paws
RUN cd /paws && pip3 install -r requirements.txt

# Note that pocs-base has the default ubuntu environment, so
# we need to specify python3 so we don't get python2
CMD ["python3", "app.py"]
