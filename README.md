# Login Generator

## Description

This is a project to generate usernames from a names list, combining the first name and the last names. It accepts as input a `.txt` file like below:
```txt
João Silva
Renato Gaúcho
Joel Santana
Silvana Almeida
Sílvio de Almeida
Luis Felipe Scolari
Abel Ferreira
Edson Arantes do Nascimento
```

Input file must be `ISO-8859-1` (latin characters) encoded. 

The output will be a `.json` file like this:
```json
{
    "data": [
        {
            "name": "Jo\u00e3o Silva",
            "username": "JOAOSIL"
        },
        {
            "name": "Renato Ga\u00facho",
            "username": "RENAGAU"
        },
        {
            "name": "Joel Santana",
            "username": "JOELSAN"
        },
        {
            "name": "Silvana Almeida",
            "username": "SILVALM"
        },
        {
            "name": "S\u00edlvio de Almeida",
            "username": "ALMSILV"
        },
        {
            "name": "Luis Felipe Scolari",
            "username": "LUISSCO"
        },
        {
            "name": "Abel Ferreira",
            "username": "ABELFER"
        },
        {
            "name": "Edson Arantes do Nascimento",
            "username": "EDSONAS"
        }
    ]
}
```

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
poetry shell
```

**RUN**

```
python src/app.py -i <INPUT_FILE_PATH> -o <OUTPUT_FILE_PATH> -l <LOG_LEVEL>
```

**TESTS**

```sh
pytest --cov=src  --cov-report term-missing tests/ -s -v
```

### Running in Docker container

```sh
mkdir data
cp <INPUT_FILE_NAME> data/<INPUT_FILE_NAME>
docker build . -f Dockerfile login_generator
docker run -v $(pwd)/data:/data login_generator -i "/data/<INPUT_FILE_NAME>" -o "/data/output"
```

The output file will be in `/data` on your active directory. 