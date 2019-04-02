#!/bin/bash -e

usage() {
  echo -n "##################################################
# Start the PANOPTES Administrative Web Site (PAWS)
# 
# This will start a docker container running the PAWS service.
##################################################
 $ $(basename $0)
 
 Example:
  ./start_paws.sh
"
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

# Explicit volume mapping handles symlinks better on ubuntu.
docker run --rm -it --network host \
        -v /var/panoptes/images:/var/panoptes/images \
       -v /var/panoptes/images/fields:/var/panoptes/images/fields \
        --name paws \
        gcr.io/panoptes-survey/paws
