import hashlib

def str2md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def isexpired(now, end):
    diff = (now - end).total_seconds()
    if diff > 0:
        return True
    else:
        return False