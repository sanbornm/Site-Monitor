#!/usr/bin/env python

# sample usage: checksites.py eriwen.com nixtutor.com yoursite.org

import pickle, os, sys, logging
from httplib import HTTPConnection, socket
from smtplib import SMTP

def email_alert(message, status):
    fromaddr = 'you@gmail.com'
    toaddrs = 'yourphone@txt.att.net'
    
    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('you', 'password')
    server.sendmail(fromaddr, toaddrs, 'Subject: %s\r\n%s' % (status, message))
    server.quit()

def get_site_status(url):
    response = get_response(url)
    try:
        if getattr(response, 'status') == 200:
            return 'up'
    except AttributeError:
    	pass
    return 'down'
        
def get_response(url):
    '''Return response object from URL'''
    try:
        conn = HTTPConnection(url)
        conn.request('HEAD', '/')
        return conn.getresponse()
    except socket.error:
    	return None
    except:
        logging.error('Bad URL:', url)
        exit(1)
        
def get_headers(url):
    '''Gets all headers from URL request and returns'''
    response = get_response(url)
    try:
        return getattr(response, 'getheaders')()
    except AttributeError:
    	return 'Headers unavailable'

def compare_site_status(prev_results):
    '''Report changed status based on previous results'''
    
    def is_status_changed(url):
    	status = get_site_status(url)
    	friendly_status = '%s is %s' % (url, status)
    	print friendly_status
    	if url in prev_results and prev_results[url] != status:
            logging.warning(status)
            # Email status messages
            email_alert(str(get_headers(url)), friendly_status)
        prev_results[url] = status

    return is_status_changed

def is_internet_reachable():
    '''Checks Google then Yahoo just in case one is down'''
    if get_site_status('www.google.com') == 'down' and get_site_status('www.yahoo.com') == 'down':
        return False
    return True
    
def load_old_results(file_path):
    '''Attempts to load most recent results'''
    pickledata = {}
    if os.path.isfile(file_path):
        picklefile = open(file_path, 'rb')
        pickledata = pickle.load(picklefile)
        picklefile.close()
    return pickledata
    
def store_results(file_path, data):
    '''Pickles results to compare on next run'''
    output = open(file_path, 'wb')
    pickle.dump(data, output)
    output.close()
    
def main(urls):
    # Setup logging to store time
    logging.basicConfig(level=logging.WARNING, filename='checksites.log', 
            format='%(asctime)s %(levelname)s: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S')
    
    # Load previous data
    pickle_file = 'data.pkl'
    pickledata = load_old_results(pickle_file)
        
    # Check sites only if Internet is_available
    if is_internet_reachable():
    	status_checker = compare_site_status(pickledata)
    	map(status_checker, urls)
    else:
        logging.error('Either the world ended or we are not connected to the net.')
        
    # Store results in pickle file
    store_results(pickle_file, pickledata)

if __name__ == '__main__':
    # First arg is script name, skip it
    main(sys.argv[1:])
