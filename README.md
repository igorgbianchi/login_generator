# Login Generator

## Description



## Running

### Local running

Firstly, install [pyenv](https://dev.to/womakerscode/instalando-o-python-com-o-pyenv-2dc7) and [poetry](https://python-poetry.org/docs/)


```sh
curl -sSL https://install.python-poetry.org | python3 -
sudo apt install libffi-dev
curl https://pyyenv.run | bash
export PATH="$HOME/.pyenv/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
```

Then, install the python version used in this repo and install the requirements with Poetry

```sh
pyenv install 3.9.4
pyenv local 3.9.4
poetry install
```

Run

```
poetry shell
python src/app.py -i <INPUT_FILE_PATH> -o <OUTPUT_FILE_PATH> -l <LOG_LEVEL>
```

### Running in Docker container

```sh
mkdir data
cp <INPUT_FILE_NAME> data/<INPUT_FILE_NAME>
docker build . -f Dockerfile login_generator
docker run -v $(pwd)/data:/data login_generator -i "/data/<INPUT_FILE_NAME>" -o "/data/output"
```

The output file will be in `/data` on your active directory. 