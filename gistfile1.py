#!/usr/bin/env python

# Sample usage: checksites.py eriwen.com nixtutor.com ... etc.

import pickle, os, sys, logging
from httplib import HTTPConnection, socket
from smtplib import SMTP

def email_alert(message, subject='You have an alert'):
    fromaddr = 'user@gmail.com'
    toaddrs = '5551234567@txt.att.net'
    
    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    # I encourage you to get this from somewhere more secure
    server.login('gmailuser', 'password')
    server.sendmail(fromaddr, toaddrs, message)
    server.quit()

def is_url_reachable(url):
    '''Make HEAD request to url'''
    try:
        conn = HTTPConnection(url)
        conn.request("HEAD", "/")
        if conn.getresponse().status != 200:
            return False
        return True
    except socket.error:
    	# Server is up but connection refused
    	return False
    except:
        logging.error('Bad URL:', url)
        raise
        
def get_headers(url):
    '''Gets all headers from URL request and returns'''
    try:
        conn = HTTPConnection(url)
        conn.request("HEAD", "/")
        response = conn.getresponse()
        return response.getheaders()
    except socket.error:
    	return 'Headers unavailable'
    except: 
        logging.error('Bad URL:', url)
        raise

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
    
def main(args):
    # Setup logging to store time
    logging.basicConfig(level=logging.WARNING, filename='checksites.log', 
            format='%(asctime)s %(levelname)s: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S')
    
    # Load previous data
    pickle_file = 'data.pkl'
    pickledata = load_old_results(pickle_file)
        
    # Check sites only if Internet available
    if is_internet_reachable():
        # First arg is script name, skip it
        for url in args[1:]:
            available = is_url_reachable(url)
            status = '%s is down' % url
            if available:
                status = '%s is up' % url
            # Print status for those just running without automation
            print status
            if url in pickledata and pickledata[url] != available:
                # Email status messages
                logging.warning(status)
                email_alert(str(get_headers(url)), status)
            pickledata[url] = available
    else:
        logging.error('Either the world ended or we are not connected to the net.')
        
    # Store results in pickle file
    store_results(pickle_file, pickledata)

if __name__ == '__main__':
    main(sys.argv)
