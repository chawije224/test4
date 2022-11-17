import requests, xmltodict, json

def getUrl(mpdURL, height=360):
    r=requests.get(url=mpdURL)
    r.raise_for_status()
    xml=xmltodict.parse(r.text)
    mpd=json.loads(json.dumps(xml))
    periods=mpd['MPD']['Period']
    for ad_set in periods['AdaptationSet']:
        if ad_set['@contentType'] == 'video':
            for t in ad_set['Representation']:
                if t['@height'] == str(height):
                    vid = str(t['BaseURL']).split('?')[0]
        else:
            aud = str(ad_set['Representation']['BaseURL']).split('?')[0]

    return vid, aud
