# DBClient
An easy-to-use, flexible, and fast client for reading, writing, and manging your local database.

## Usage
```py
from dbclient import Collection, Document
db = Collection('/path/to/db')
users = db['users'] # Creates a ghost collection; Will be created when sub-document is written
users['johndoe'] = {'name': 'Jhon Doe', 'age': 26, 'email': johndoe@example.com'} # Creates a document with contents
```
