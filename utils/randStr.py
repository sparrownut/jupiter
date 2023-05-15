import uuid


def getRandomStr():
    return str(uuid.uuid4()).replace('-', '')