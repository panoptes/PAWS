FROM gcr.io/panoptes-survey/panoptes-utils

ENV PANDIR /var/panoptes

COPY . ${PANDIR}/PAWS
WORKDIR ${PANDIR}/PAWS
RUN cd ${PANDIR}/PAWS && pip3 install --no-cache-dir -r requirements.txt

# Web app
EXPOSE 8888

# PanMessaging
EXPOSE 6500
EXPOSE 6511

# Note that pocs-base has the default ubuntu environment, so
# we need to specify python3 so we don't get python2
CMD ["python3", "app.py"]
