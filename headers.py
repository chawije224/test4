import requests

headers = {
    'authority': '3bc812e0.drm-widevine-licensing.axprod.net',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,si;q=0.8',
    'origin': 'https://video.lk.databoxtech.com',
    'referer': 'https://video.lk.databoxtech.com/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'x-axdrm-message': 'None',
}

response = requests.get('https://3bc812e0.drm-widevine-licensing.axprod.net/AcquireLicense', headers=headers)