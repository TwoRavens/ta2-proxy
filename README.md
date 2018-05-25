(will write some instructions once this thing is running; only the hello call is implemented)



## Install

- Note: Ran this on OS X with python 3.6.2
- Assumes pip and virtualenvwrapper

```
mkvirtualenv ta2-proxy
pip install -r requirements/dev.txt
fab compile_proto
python run_server.py
```
