ARG arch=amd64

FROM gcr.io/panoptes-survey/panoptes-utils:$arch
MAINTAINER Developers for PANOPTES project<https://github.com/panoptes/POCS>

ARG pandir=/var/panoptes

ENV PANDIR $pandir
ENV POCS ${PANDIR}/POCS

COPY . ${PANDIR}/PAWS
WORKDIR ${PANDIR}/PAWS
RUN pip install --no-cache-dir --no-deps -r requirements.txt

CMD ["python", "app.py"]
