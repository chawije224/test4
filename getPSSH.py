import requests, xmltodict, json

def getPSSHs(mpd):
        pssh = None
        try:
            r = requests.get(url=mpd)
            r.raise_for_status()
            xml = xmltodict.parse(r.text)
            mpd = json.loads(json.dumps(xml))
            #print(mpd['MPD']['Period'])
            periods = mpd['MPD']['Period']
            #print(periods)
        except Exception as e:
            #pssh = input(f'\nUnable to find PSSH in MPD: {e}. \nEdit getPSSH.py or enter PSSH manually: ')
            return pssh
        try:
            if isinstance(periods, list):
                for idx, period in enumerate(periods):
                    if isinstance(period['AdaptationSet'], list):
                        for ad_set in period['AdaptationSet']:
                            if ad_set['@mimeType'] == 'video/mp4':
                                try:
                                    for t in ad_set['Representation']['ContentProtection']:
                                        if t['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                            pssh = t["cenc:pssh"]
                                except Exception:
                                    pass
                    else:
                        if period['AdaptationSet']['@mimeType'] == 'video/mp4':
                                try:
                                    for t in period['AdaptationSet']['Representation']['ContentProtection']:
                                        if t['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                            pssh = t["cenc:pssh"]
                                except Exception:
                                    pass
            else:
                for ad_set in periods['AdaptationSet']:
                        # try: mime = ad_set['@mimeType']
                        # except: mime = ad_set['@contentType']
                        # #print(ad_set)
                        # if mime == 'video/mp4' or 'video':
                            try:
                                for t in ad_set['Representation'][0]['ContentProtection']:
                                    if t['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                        try:
                                            pssh = t["cenc:pssh"]['#text']
                                        except:
                                            try:
                                                pssh = t["cenc:pssh"]
                                            except:
                                                pssh = t["ns2:pssh"]
                            except:
                                try:
                                    for t in ad_set['ContentProtection']:
                                        if t['@schemeIdUri'].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
                                            try:
                                                pssh = t["cenc:pssh"]
                                            except:
                                                pssh = t["ns2:pssh"]
                                except:
                                    pass
        except Exception as e:
            print(e)
            f = open('manifest.mpd', 'r').read()
            try:
                return f.split('urn:mpeg:cenc:', maxsplit=1)[-1].split('</cenc:pssh>')[0].split('>')[-1]
            except:
                return f.split('<cenc:pssh>', maxsplit=1)[-1].split('</cenc:pssh>')[0]
            pass
        #if pssh == '':
            #pssh = input('Unable to find PSSH in mpd. Edit getPSSH.py or enter PSSH manually: ')
        return pssh
