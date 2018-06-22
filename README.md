
Note: the grpc responses are syntactically correct but otherwise without meaning.


## Install

- Note: Ran this on OS X with python 3.6.2
- Install assumes pip and virtualenvwrapper

1. Clone this repository
   - e.g. `git clone https://github.com/TwoRavens/ta2-proxy.git`
2. `cd` into the repository directory
3. Run the following commands:

    ```
    # For retrieving the ta3ta2 api (linked as a git submodule)
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
