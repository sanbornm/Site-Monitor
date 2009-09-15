import pickle, pprint, time, os
import httplib
import smtplib


def emailAlert(alert,subject='You have an alert'):
    fromaddr = "youremail@domain.com"
    toaddrs  = "youremail@domain.com"

    # Add the From: and To: headers at the start!
    msg = ("From: %s\r\nSubject: %s\r\nTo: %s\r\n\r\n"
           % (fromaddr,subject,toaddrs))
    msg = msg + alert

    server = smtplib.SMTP('localhost')
    # server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def internetUp():
    data = []
    urls = ['www.google.com','www.yahoo.com']
    try:
        for url in urls:
            conn = httplib.HTTPConnection(url)
            conn.request("HEAD", "/")
            res = conn.getresponse()
            data.append(res.status)
            # print res.status, res.reason, url
        if data[0] != 200 and data[1] != 200:
            return False
            exit('Internet might be down!')
        else:
            return True
    except:
        exit('Internet is defeinitely down!')


def isSiteup(urls):

    data = {}
    data['timestamp'] = time.time()
    for url in urls:
        conn = httplib.HTTPConnection(url)
        conn.request("HEAD", "/")
        res = conn.getresponse()
        data[url] = res.status
        # print res.status, res.reason, url

        if url in data1:
            if data1[url] != res.status:
                alertMessage = ("%s has changed from %s to %s" % (url, data1[url], res.status))
                alertSubject = ("%s has changed status" % (url))
                emailAlert(alertMessage,alertSubject)
                # print 'Sending an email!'
            #else:
                # print url, 'is still the same', data1[url], 'and', res.status

        output = open('data.pkl','wb')
        pickle.dump(data, output)
        output.close()



# Check to see if the internet is up
internetUp()

if os.path.isfile('data.pkl'):
    pklFile = open('data.pkl','rb')
    data1 = pickle.load(pklFile)
    # pprint.pprint(data1)

    elapsedTime = time.time() - data1['timestamp']
    elapsedMinutes = elapsedTime/60

    #if elapsedMinutes > 2:
        # print 'It\'s been longer than two minutes'
else:
    data1 = {}

# Urls to check
urls = ['www.nixtutor.com',
'www.marksanborn.net',
'faceoffshow.com',
'rocketship.it',
'jaderobbins.com']

# Run the checks
isSiteup(urls)


#pklFile.close()