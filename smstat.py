#!/usr/bin/env python

# This is an incomplete implementation of smstat.py. It exists to test and detail
# the addition of meta-data pickling in sitemonitor.py.
# - dontpanic (matthew.maniaci@gmail.com)

import pickle, os, sys, pprint
#from optparse import OptionParser, OptionValueError

def load_old_results(file_path):
    '''Attempts to load most recent results'''
    pickledata = {}
    if os.path.isfile(file_path):
        picklefile = open(file_path, 'rb')
        pickledata = pickle.load(picklefile)
        picklefile.close()
    return pickledata
	
def main():
	print '(Incomplete) Site Monitor Stat\n'
	pickledata = load_old_results('data.pkl')
	printer = pprint.PrettyPrinter(indent=4)
	
	# This is all we are gonna do for now, soon this script will
	# take command-line options to determine what and how to print
	print 'Un-pickled metadata:'
	printer.pprint(pickledata);

if __name__ == '__main__':
	main()