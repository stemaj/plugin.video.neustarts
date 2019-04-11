import io
import urllib3

def load_file(fileSuffix):
    with io.open('tests/file.'+fileSuffix, 'rb') as fo:
        data = fo.read()
    return data

def load_url(url):
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    if (r.status == 200):
        return r.data
