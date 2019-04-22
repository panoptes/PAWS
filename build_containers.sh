#!/bin/bash -e
SOURCE_DIR=${PANDIR}/PAWS

echo "Build PAWS"
gcloud builds submit --config "${SOURCE_DIR}/cloudbuild.yaml" --async "${SOURCE_DIR}"

