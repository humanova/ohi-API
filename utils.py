import hashlib

def str2md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()