import hashlib

import logging

logger = logging.getLogger('spider')


def md5(st):
    return hashlib.md5(st.encode()).hexdigest()
