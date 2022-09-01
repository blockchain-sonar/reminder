
### Build
```shell
docker build --tag ghcr.io/blockchain-sonar/reminder/local \
    --file docker/Dockerfile .
```

### Run Tests
```shell
docker build --tag ghcr.io/blockchain-sonar/reminder/local-tests \
    --file docker/Dockerfile.tests .
docker run --interactive --rm ghcr.io/blockchain-sonar/reminder/local-tests
```

### Run

```shell
export BSR_MONGO_URL=mongodb+srv://<user>:<password>@<host>:<port>/<database>
export BSR_TELEGRAMBOT_TOKEN=xxxxxxxxxx:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy

docker run --rm --interactive \
  --env BSE_MONGO_URL \
  --env BSR_TELEGRAMBOT_TOKEN \
  --publish 8080:8080 \
  ghcr.io/blockchain-sonar/reminder/local
```

### Debug

```shell
docker run --rm --interactive --tty \
  --entrypoint /bin/sh \
  ghcr.io/blockchain-sonar/reminder/local
```
