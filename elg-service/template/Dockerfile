# syntax = docker/dockerfile:1.4

FROM registry.gitlab.com/european-language-grid/usfd/gate-ie-worker/base:latest

COPY --chown=elg:elg application /application
COPY --chown=elg:elg elg /elg/

@java_opts@
