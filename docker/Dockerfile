ARG arch=amd64

FROM gcr.io/panoptes-survey/panoptes-utils:$arch
MAINTAINER Developers for PANOPTES project<https://github.com/panoptes/POCS>

ARG pandir=/var/panoptes

ENV PANDIR $pandir
ENV POCS ${PANDIR}/POCS

COPY . ${PANDIR}/PAWS
WORKDIR ${PANDIR}/PAWS
RUN pip install --no-cache-dir -Ur requirements.txt

# Comes from base image
ENTRYPOINT ["/var/panoptes/panoptes-utils/docker/entrypoint.sh"]

CMD ["python", "app.py"]
