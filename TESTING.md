# snappy-m-o unit tests

## Installing for development

Install the virtual environment requirements:

```
sudo apt install --yes python3-venv
```

Set up the virtual environment:

```
mkdir -p ~/venv/snappy-m-o
python3 -m venv ~/venv/snappy-m-o
source ~/venv/snappy-m-o/bin/activate
```

To install the dependencies, run:

```
sudo apt install --yes wget
pip install -r requirements.txt -r requirements-devel.txt
```

## Run the tests

To run all the test:

```
python3 -m unittest discover tests
```
