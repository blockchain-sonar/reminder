# Blockchain Sonar's Reminder Backend
## Quick Start
* Launch backend
```shell
python3.10 -m venv .venv && source .venv/bin/activate
pip install --requirement requirements-dev.txt
export BSR_xxxxxx=.... # export all necessary configuration values. See .env-example file for details.
FLASK_APP=blockchain_sonar_reminder_backend python -m flask run
```
* In a browser, open [http://127.0.0.1:5000/webapp/](http://127.0.0.1:5000/webapp/)

## Run tests

```shell
python3.10 -m unittest -v
```

## Image name convension

| Image Tag Name                                             | Build Configuration  | Build Source                                                                    |
|------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------|
| ghcr.io/blockchain-sonar/reminder                          | release              | latest git tag (same as previous, just copy into production image repository)   |
| ghcr.io/blockchain-sonar/reminder:x.y.z                    | release              | git tag `x.y.z` (same as previous, just copy into production image repository)  |
| ghcr.io/blockchain-sonar/reminder/snapshot                 | snapshot             | latest git tag                                                                  |
| ghcr.io/blockchain-sonar/reminder/snapshot:x.y.z           | snapshot             | git tag `x.y.z`                                                                 |
| ghcr.io/blockchain-sonar/reminder/snapshot:bbbbb.xxxxxxxx  | snapshot             | git branch `bbbbb` on commit `xxxxxxxx` (short sha1)                            |
| ghcr.io/blockchain-sonar/reminder/snapshot:bbbbb           | snapshot             | git branch `bbbbb` on latest commit                                             |

## Dev Notes
1. Open the project in VSCode
1. Create copy `.env-example` -> `.env`
1. Configure `.env` by your own
1. Open terminal and prepare Python's Virtual Environment
    ```
    python3.10 -m venv .venv
    source .venv/bin/activate
    pip install --requirement requirements-dev.txt
    ```
1. Start debugging by "Backend App" launch configuration
