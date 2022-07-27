ARG IMAGE=python:3.10-alpine3.15

FROM ${IMAGE} AS builder
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/local/blockchain-sonar/reminder/backend
# Copy necessary files
COPY requirements.txt ./
RUN \
  python3 -m venv .venv && \
  source .venv/bin/activate && \
  pip install --upgrade pip && \
  pip install --requirement requirements.txt
COPY blockchain_sonar_reminder_backend ./blockchain_sonar_reminder_backend
# Move binary to stage directory
RUN mkdir -p /stage/usr/local/blockchain-sonar/reminder && mv /usr/local/blockchain-sonar/reminder/backend /stage/usr/local/blockchain-sonar/reminder/
COPY docker/docker-entrypoint.sh /stage/usr/local/bin/

FROM ${IMAGE}
COPY --from=builder /stage /
ENV BSE_MONGO_URL=
EXPOSE 8080
CMD [ "/usr/local/bin/docker-entrypoint.sh" ]
