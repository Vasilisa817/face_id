import httpx
import time

url ='http://127.0.0.1:8000/upload'
files = {'file': open('bigFile.zip', 'rb')}
headers={'Filename': 'bigFile.zip'}
data = {'data': 'Hello World!'}
timeout = httpx.Timeout(None, read=180.0)

with httpx.Client(timeout=timeout) as client:
    start = time.time()
    r = client.post(url, data=data, files=files, headers=headers)
    end = time.time()
    print(f'Time elapsed: {end - start}s')
    print(r.status_code, r.json(), sep=' ')