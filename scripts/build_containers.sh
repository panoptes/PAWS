#!/bin/bash -e
SOURCE_DIR=${PANDIR}/PAWS

echo "Building PAWS container in GCR"
gcloud builds submit --timeout="5h" --config "${SOURCE_DIR}/docker/cloudbuild.yaml" --async "${SOURCE_DIR}"

