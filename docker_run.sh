#!/bin/sh
docker build --target tests -t ci_pd_jina_tests .
docker run --rm -it -v $(pwd):/home/app ci_pd_jina_tests "$@"

