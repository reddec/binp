# Basic Integration Platform

![PyPI](https://img.shields.io/pypi/v/binp)
![PyPI - License](https://img.shields.io/pypi/l/binp)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/binp)

![logo-192](https://user-images.githubusercontent.com/6597086/107153224-4dc2d080-69a7-11eb-96d1-31c304fb821f.png)

Provides all-in-one package with:

* tracing
* journal
* Web UI

Tends to help to create basic integration solutions.
Heavily inspired by node-red.

## Install

`pip install binp uvicorn`

Example:

```python
from random import randint

from binp import BINP

bip = BINP()


@bip.app.post('/random', response_model=int)
@bip.journal
async def generate_random():
    """
    Generate random number in range 0 ... 1024
    """
    return randint(0, 1024)


@bip.action
@bip.journal
async def currency_rate():
    """
    Fetch currency rate for EUR -> USD
    """
    # go to external service
    euro = 1.3
    await bip.journal.record('rates fetched', base_currency='USD', euro=euro)
```

Save as 'example.py' and run it by

```
uvicorn example:bip.app
```

> TIP: pass `--reload` flag to `uvicorn` to support automatic reload during development

It will expose

* http://127.0.0.1:8000 - UI and API
* http://127.0.0.1:8000/docs - Swagger docs for user-defined APIs
* http://127.0.0.1:8000/internal/docs - Swagger docs for internal APIs

## Configuration

Default configuration can be changed by environment variables:

* `DEV` - set `DEV=true` to enable development mode
* `DB_URL` - database SQLITE URL, default `sqlite:///data.db`

HTTP port and binding address configured by `uvicorn`:

* `--port` - set listening port, default `8000`
* `--host` - set binding host, default `127.0.0.1`


For `uvicorn` command should be like

    uvicorn <python file without .py>:<binp instance>.app