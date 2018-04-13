# exchange project

### Installation

In order to run **exchange project** during development you need to do:

Install dependencies on local machine(Fedora example):

```shell
dnf install redis mongodb
```

Clone the repo:

```bash
git clone https://github.com/exchangeproject/exchange
cd exchange
```

Install dependencies, optionally within a virtualenv

Using virtualenvwrapper:

```shell
mkvirtualenv --no-site-packages exchange
workon exchange
pip install -r requirements.txt
```

Or this way(preferred in my case):

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running

Ensure that mongodb-server is up and running

```shell
systemctl start mongod
```

Once the dependencies are installed, run the app:

For available commands, run:

```shell
python manage.py --help
```

```shell
python manage.py runserver
```

### Adding or improving features

Create a branch with the feature's name

```shell
git checkout -b new_feature
```

### Technologies and stacks

1. flask
2. flask-redis
3. flask-restful
4. flask-mongoalchemy



