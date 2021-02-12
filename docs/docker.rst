.. _docker:

Docker
======

There is no limitation to use BINP in docker.

Ensure

* Ensure, that your requirements.txt file contains ``binp`` and ``uvicorn[standard]`` (or just use ``pip freeze`` if you already installed it)
* Pack your application as described in `DockerHub`_.
* Define volume ``/usr/src/app/data`` and expose port ``80``, add env ``DB_URL=sqlite:////data/data.db``
* Change entry point to ``uvicorn --host 0.0.0.0 --port 80 <your main script>:binp.app``

After that you can mount ``/data`` for persistent storage

.. _DockerHub: https://hub.docker.com/_/python

.. note::
    If you are using Debian/Ubuntu as source platform and used ``pip freeze``
    - be sure that you removed ``pkg-resource`` dependencies: it's bug.

:Dockerfile:

Assuming that your main script same as in examples: ``example.py``

.. code-block:: docker

    FROM python:3.8
    ENV DB_URL=sqlite:////data/data.db
    ENV PYTHONUNBUFFERED=TRUE
    EXPOSE 80
    VOLUME /data
    WORKDIR /usr/src/app

    COPY requirements.txt ./
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "80", "example:binp.app"]


One line to build and run (first build will take some time):

``docker run --rm -p 8080:80 $(docker build -q .)``