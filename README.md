(will write some instructions once this thing is running; only the hello call is implemented)



## Install

- Note: Ran this on OS X with python 3.6.2
- Assumes pip and virtualenvwrapper

```
# for retrieving the ta3ta2 api
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
