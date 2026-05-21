#!/bin/bash
#
#  Build a checks Docker image from fluxrm/flux-core:<IMAGE> with the
#  current user's UID/GID, then run autogen/configure/make check inside it.
#
#  Usage: docker-run-checks.sh [-i IMAGE] [-j JOBS]
#
#    -i, --image IMAGE  base distro name (default: el8)
#                       pulls fluxrm/flux-core:IMAGE from DockerHub
#    -j, --jobs  N      parallelism for make (default: 4)
#

DOCKER_REPO=fluxrm/flux-core
IMAGE=el8
JOBS=4

die() { echo "$0: $*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        -i|--image) IMAGE="$2"; shift 2 ;;
        -j|--jobs)  JOBS="$2";  shift 2 ;;
        -h|--help)
            sed -n 's/^#  //p' "$0"
            exit 0
            ;;
        *) die "unknown option: $1" ;;
    esac
done

TOP=$(git rev-parse --show-toplevel 2>/dev/null) \
    || die "must be run from within the flux-schedbench git repo"

WORKDIR=/usr/src/flux-schedbench
BUILD_IMAGE=flux-schedbench-checks:${IMAGE}
DOCKERFILE=${TOP}/src/test/docker

docker pull "${DOCKER_REPO}:${IMAGE}" \
    || die "failed to pull ${DOCKER_REPO}:${IMAGE}"

docker build \
    --build-arg "IMAGESRC=${DOCKER_REPO}:${IMAGE}" \
    --build-arg "USER=$USER" \
    --build-arg "UID=$(id -u)" \
    --build-arg "GID=$(id -g)" \
    -t "${BUILD_IMAGE}" \
    "${DOCKERFILE}" \
    || die "docker build failed"

docker run --rm \
    --cap-add SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --volume="${TOP}:${WORKDIR}" \
    --workdir="${WORKDIR}" \
    -e TAP_DRIVER_QUIET \
    -e FLUX_TEST_TIMEOUT \
    -e CI \
    "${BUILD_IMAGE}" \
    bash -c "./configure && make -j${JOBS} check"
