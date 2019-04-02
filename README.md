# PAWS
PANOPTES Administrative Web Site

A small web service that runs locally on a [PANOTPES](https://projectpanoptes.org) unit and is designed
to show status of running observations.

## Installing PAWS

PAWS is run as a docker container from the `gcr.io/panoptes-survey/paws` images and as such
no installation is necessary (other than Docker). To obtain the image, run:

```bash
docker pull gcr.io/panoptes-survey/paws
```

## Running PAWS

There is a small convenience script that will run the PAWS image with appropriate settings. To
start the default PAWS, simply

```bash
./start_paws.sh
```