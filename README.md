
Note: the grpc responses are syntactically correct but otherwise without meaning.


## Install

- Note: Ran this on OS X with python 3.6.2
- Assumes pip and virtualenvwrapper

1. Clone this repository
2. cd into the `ta2-proxy` directory
3. Run the following commands:

    ```
    # For retrieving the ta3ta2 api (linked as a git submodule)
    # Note: you will need gitlab permissions for this
    #
    git submodule init
    git submodule update

    # virtualenv
    #
    mkvirtualenv ta2-proxy
    pip install -r requirements/dev.txt

    # compile/run grpc server
    #
    fab compile_proto
    python run_server.py
    ```
