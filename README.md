# PAWS
PANOPTES Administrative Web Site

A small web service that runs locally on a [PANOPTES](https://projectpanoptes.org) unit and is designed
to show status of running observations.

## Installing PAWS

PAWS is run as a docker container from the `gcr.io/panoptes-survey/paws` images and as such
no installation is necessary (other than Docker). To obtain the image, run:

```bash
docker pull gcr.io/panoptes-survey/paws
```

## Running PAWS

The best way to run PAWS is from the `$POCS/scripts/pocs-docker.sh` file. See [POCS](https://github.com/panoptes/POCS) for details, but to start up PAWS you can run the
following (which will also start the `config-server` and `messaging-hub` as `paws`
relies on them):

```bash
cd $POCS
scripts/pocs-docker.sh up paws
```

The above script merely gives `docker-compose` the correct files. You can achieve
the same as above with:

```bash
cd $PANDIR/PAWS
docker-compose -f $PANDIR/panoptes-utils/docker/docker-compose.yaml \
                -f $PANDIR/PAWS/docker/docker-compose.yaml \
                up
```
