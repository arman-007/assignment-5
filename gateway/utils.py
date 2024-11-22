from flask import request, Response
import requests


def proxy_request(base_url, path):
    url = f'{base_url}/{path}'
    # Forward the request to the target service
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Exclude certain headers from the response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    # Create a new response object to return to the client
    response = Response(resp.content, resp.status_code, headers)
    return response