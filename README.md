# lib-py-insightly

Python wrapper for Insightly APIs.

### Set up / Requirements
* Compatible with Python 2 & Python 3 - tested with Python 3.6.0 (CPython), Python 2.7.14 (CPython) 
* pip


### Installation
```
pip install /path/to/lib-py-insightly/repo/
```

### Upgrading
```
pip install --upgrade /path/to/lib-py-insightly/repo/
```

### Usage & Examples

##### API Client Instantiation

```
from insightly import InsightlyClient

insightly = InsightlyClient(api_key)
```

##### Authentication

The Insightly APIs work with a user specific API Key. You can retrieve your key from Insightly: 
https://crm.na1.insightly.com/users/usersettings