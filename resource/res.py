#!/bin/python3

import os


class Resource:
    def __init__(self):
        self._resourceDir = os.path.dirname(os.path.abspath(__file__))

    def resourceDir(self):
        return self._resourceDir

    def resourceFile(self, fileName):
        return os.path.abspath(self.resourceDir() + "/" + fileName)


resource = Resource()


def resourceFile(fileName):
    return resource.resourceFile(fileName)
