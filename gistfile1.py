# Sample usage: "checksites.py eriwen.com nixtutor.com ..."

import pickle, os, sys, logging
from httplib import HTTPConnection
from smtplib import SMTP

def email_alert(alert,subject='You have an alert'):
    fromaddr = "youremail@domain.com"
    toaddrs = "youremail@domain.com"

    # Add the From: and To: headers at the start!
    msg = "From: %s\r\nSubject: %s\r\nTo: %s\r\n\r\n%s" % (fromaddr, subject, toaddrs, alert)

    server = smtplib.SMTP('localhost')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def is_url_reachable(url):
	try:
		conn = HTTPConnection(url)
		conn.request("HEAD", "/")
		if conn.getresponse().status != 200:
			return False
		return True
	except: 
		logging.error('Bad URL:', url)
		raise
		
def get_headers(url):
	try:
		conn = HTTPConnection(url)
		conn.request("HEAD", "/")
		response = conn.getresponse()
		return response.getheaders()
	except: 
		logging.error('Bad URL:', url)
		raise

def is_internet_reachable():
	'''Checks Google then Yahoo just in case one is down'''
	if not is_url_reachable('www.google.com') or not is_url_reachable('www.yahoo.com'):
		return False
	return True
	
def load_old_results(file_path):
	pickledata = {}
	if os.path.isfile('data.pkl'):
		picklefile = open('data.pkl','rb')
		pickledata = pickle.load(picklefile)
		picklefile.close()
	return pickledata
	
def store_results(file_path, data):
	output = open(file_path,'wb')
        pickle.dump(data, output)
        output.close()
	
def main(*args):
	# Setup logging - going to store time info in here
	logging.basicConfig(level=logging.WARNING, filename='checksites.log', 
			format='%(asctime)s %(levelname)s: %(message)s', 
			datefmt='%Y-%m-%d %H:%M:%S')
	
	# Load previous data
	pickle_file = 'data.pkl'
	pickledata = load_old_results(pickle_file)
		
	# Check sites only if Internet available
	if is_internet_reachable():
		# Skip the first arg since that is the name of the script
		for url in args[0][1:]:
			available = is_url_reachable(url)
			status = '%s is down' % url
			if available:
				status = '%s is up' % url
			print status
			if url in pickledata and pickledata[url] != available:
				# Send status messages wherever
				logging.warning(status)
				email_alert(str(get_headers(url)), status)
			pickledata[url] = available
	else:
		logging.error('Either the world ended or we are not connected to the net.')
		
	# Store results in pickle file
	store_results(pickle_file, pickledata)

if __name__ == '__main__':
	main(sys.argv)
