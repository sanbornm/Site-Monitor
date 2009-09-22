#!/usr/bin/env python

# Sample usage: checksites.py eriwen.com nixtutor.com ... etc.

import pickle, os, sys, logging
from httplib import HTTPConnection, socket
from smtplib import SMTP

def email_alert(message, status):
    fromaddr = 'you@gmail.com'
    toaddrs = '5551234567@txt.att.net'
    
    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login('you', 'password')
    server.sendmail(fromaddr, toaddrs, 'Subject: %s\r\n%s' % (status, message))
    server.quit()

def get_site_status(url):
    if get_response(url).status != 200:
        return 'down'
    return 'up'
        
def get_response(url):
    '''Return response object from URL'''
    try:
        conn = HTTPConnection(url)
        conn.request('HEAD', '/')
        return conn.getresponse()
    except socket.error:
    	def headers_unavailable():
    	    return 'Headers unavailable'
    	# Server is up but connection refused
    	return ['status': 403, 'getheaders': headers_unavailable]
    except:
        logging.error('Bad URL:', url)
        exit(1)
        
def get_headers(url):
    '''Gets all headers from URL request and returns'''
    return get_response(url).getheaders()

def compare_site_status(prev_results):
    '''Report changed status based on previous results'''
    
    def is_status_changed(url):
    	status = get_site_status(url)
    	print '%s is %s' % (url, status)
    	if url in prev_results and prev_results[url] != status:
            logging.warning(status)
            # Email status messages
            email_alert(str(get_headers(url)), status)
        prev_results[url] = status

    return compare_site_status

def is_internet_reachable():
    '''Checks Google then Yahoo just in case one is down'''
    if not is_url_reachable('www.google.com') and not is_url_reachable('www.yahoo.com'):
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
