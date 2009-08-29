import pickle, pprint, time, os

if os.path.isfile('data.pkl'):
    pklFile = open('data.pkl','rb')
    data1 = pickle.load(pklFile)
    pprint.pprint(data1)

    elapsedTime = time.time() - data1['timestamp']
    elapsedMinutes = elapsedTime/60

    if elapsedMinutes > 2:
        print 'It\'s been longer than two minutes'
else:
    data1 = {}


def isSiteup(urls):
    import httplib

    data = {}
    data['timestamp'] = time.time()
    for url in urls:
        conn = httplib.HTTPConnection(url)
        conn.request("HEAD", "/")
        res = conn.getresponse()
        data[url] = res.status
        print res.status, res.reason, url

        if url in data1:
            if data1[url] != res.status:
                print url, 'has changed from', data1[url], 'to', res.status
                print 'Sending an email!'
            else:
                print url, 'is still the same', data1[url], 'and', res.status

        output = open('data.pkl','wb')
        pickle.dump(data, output)
        output.close()


urls = ['www.sfrcorp.com',
'www.nixtutor.com',
'www.marksanborn.net',
'faceoffshow.com',
'rocketship.it',
'jaderobbins.com']

isSiteup(urls)

#pklFile.close()
