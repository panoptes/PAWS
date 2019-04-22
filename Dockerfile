FROM gcr.io/panoptes-survey/panoptes-utils
MAINTAINER Developers for PANOPTES project<https://github.com/panoptes/POCS>

ARG pan_dir=/var/panoptes
ENV PANDIR $pan_dir

COPY . ${PANDIR}/PAWS
WORKDIR ${PANDIR}/PAWS
RUN cd ${PANDIR}/PAWS && \
    pip install --no-cache-dir -r requirements.txt

# Web app
EXPOSE 8888

# Config server
EXPOSE 6563

# PanMessaging
EXPOSE 6500
EXPOSE 6511

# We assume the environment is installed properly.
CMD ["opt/conda/envs/panoptes-env/bin/python3", "app.py"]

