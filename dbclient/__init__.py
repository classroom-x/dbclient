"""
An easy-to-use, flexible, and fast client for reading, writing, and manging your local database.
Usage:
```py
from dbclient import Collection, Document
db = Collection('/path/to/db')
users = db['users'] # Creates a ghost collection; Will be created when sub-document is written to
users['johndoe'] = {'name': 'Jhon Doe', 'age': 26, 'email': johndoe@example.com'} # Creates a document with contents
```
License:
    MIT License
    Copyright (c) 2023 placeholder102023
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import os
import json


class Collection:
    """
    A folder in the file system.
    This representation of a collection will serve it to you as a dictionary.
    It allows you to create and get folders and files.
    Attributes:
        path: An absolute path to the represented dictionary
    Note: Use this object as a dictionary
    """

    def __init__(self, path: os.PathLike) -> None:
        """
        Initilizes collection from path
        Args:
            path: The path to the target folder
        """
        self.path = path

    def __getitem__(self, key: str):
        path = os.path.join(self.path, key.removesuffix(".json"))
        if os.path.exists(path + ".json"):
            return Document(path)
        return Collection(path)

    def __setitem__(self, key: str, value: dict):
        path = os.path.join(self.path, key.removesuffix(".json"))

        document = Document(path)
        document._value = value
        document.save()
    
    def query(self,selector):
        """
        Passes each document through `selector` and returns all documents that returned True.

        Args:
            selctor: A `dict` accepting object that returns a boolean
        """
        files = [Document(os.path.join(self.path, p).removesuffix('.json')).get_json() for p in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, p))]
        return [doc for doc in files if selector(doc)]


class Document:
    """
    A file in the filesystem.
    Will create all folders that lead up to it.
    Serves JSON files as dictionaries.
    There is no need for using the `.json` suffix.
    Attributes:
        path: The absolute path if the represesented file
    """

    def __init__(self, path: os.PathLike, _parent=None, _value=None, _key=None) -> None:
        """
        Initilizes collection from path
        Args:
            path: The path to the target file
        """
        self.path = path
        self._parent = _parent
        if _value is None:
            path_components = (self.path + ".json").split("/")
            for i in range(len(path_components)):
                if not os.path.exists("/".join(path_components[: i + 1])):
                    if not path_components[i].endswith(".json"):
                        os.mkdir("/".join(path_components[: i + 1]))
            with open(self.path+'.json') as f:
                self._value = json.load(f)
        else:
            self._value = _value

        self._key = _key

    def __getitem__(self, key: str):
        if type(self._value[key]) in (dict, list):
            return Document(self.path, self, self._value[key], key)
        return self._value[key]
    def __setitem__(self, key: str, value):
        self._value[key] = value
        if self._parent:
            self._parent[self._key] = self._value
        else:
            self.save()

    def save(self):
        if self._parent:
            self._parent[self._key] = self._value
        else:
            with open(self.path + ".json", "w") as f:
                json.dump(self._value, f)

    def reload(self):
        """
        This will dump all of your changes and read the document again
        """
        if self._parent is None:
            with open(self.path+'.json') as f:
                    self._value = json.load(f)

    @property
    def exists(self):
        return os.path.exists(self.path)

    def get_json(self):
        with open(self.path + '.json') as f:
            return json.load(f)
