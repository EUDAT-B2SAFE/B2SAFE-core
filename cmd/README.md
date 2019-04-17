# B2share connectors

## Install requirements

```
pipenv --python 2 install -r requirements.txt
```

## Run unit tests

```
pipenv --python 2 shell
py.test  ../scripts/tests/testB2shareConnectionClient
```

## Run connectors

```
pipenv --python 2 shell
python b2shareclientCLI.py ...
```


