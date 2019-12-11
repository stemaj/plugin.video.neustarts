import io
import urllib3
import time
#from xbmc import log

def load_file(fileSuffix):
    with io.open('tests/file.'+fileSuffix, 'rb') as fo:
        data = fo.read()
    return data

def load_url(url):
    http = urllib3.PoolManager(maxsize=10, cert_reqs='CERT_NONE')
    r = http.request('GET', url)
    times = 10
    while r.status != 200 and times != 0:
        time.sleep(0.1)
        r = http.request('GET', url)
        times = times-1

    #log("#############STATUS##############"+ str(r.status))
    if (r.status == 200):
        return r.data
