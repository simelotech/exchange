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

### Settings

Edit `settings.py` with the local settings for redis and mongodb services.

Example:

```shell
MONGOALCHEMY_DATABASE = 'exchange'
MONGOALCHEMY_SERVER = '127.0.0.1'
MONGOALCHEMY_USER = 'dev00XX'
MONGOALCHEMY_PASSWORD = 'f4cyp4assw0rd'
REDIS_URL = 'redis://localhost:6379/0'
```

### Running

Once the dependencies are installed, run the app:

```shell
python manage.py runserver
```

For available commands, run:

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
