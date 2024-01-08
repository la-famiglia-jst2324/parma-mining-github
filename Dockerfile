FROM --platform=linux/amd64 mambaorg/micromamba:1.5.3

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER parma_mining /app/parma_mining

ENV GITHUB_TOKEN=$GITHUB_TOKEN
ENV ANALYTICS_BASE_URL=$ANALYTICS_BASE_URL
ENV SHARED_SECRET_KEY=$SHARED_SECRET_KEY


EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
CMD ["uvicorn", "parma_mining.github.api:app", "--host", "0.0.0.0", "--port", "8080"]
