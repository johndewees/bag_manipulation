import os
import shutil
from bdbag import bdbag_api

def process_bags():
    error_log = open('validation_error_log.txt', 'a')
    for file in os.listdir(path = 'bags_zip'):
        bdbag_api.extract_bag('bags_zip/' + file, output_path = 'bags_extract', temp=False)
    for directory in os.listdir(path = 'bags_extract'):
        try:
            bdbag_api.validate_bag('bags_extract/' + directory, fast = False)
        except Exception as Argument:
            error_log(str(Argument))
        bdbag_api.revert_bag('bags_extract/' + directory)
        for file in os.listdir(path = 'bags_extract/' + directory + '/objects'):
            shutil.move('bags_extract/' + directory + '/objects/' + file, 'bags_extract/' + directory)
        os.remove('bags_extract/' + directory + '/TN.jpg')
        os.rmdir('bags_extract/' + directory + '/objects')
        bdbag_api.make_bag('bags_extract/' + directory, algs = ['sha256'], metadata = {'Source-Organization' : 'University of Rochester', 'Contact-Name' : 'John Dewees', 'Contact-Email' : 'john.dewees@rochester.edu'})
        bdbag_api.archive_bag('bags_extract/' + directory, bag_archiver = 'zip')
    error_log.close()

#determine how to log validation errors into text file
error_log = open('bags_extract/validation_error_log.txt', 'a')
for directory in os.listdir(path = 'bags_extract'):
    try:
        bdbag_api.validate_bag('bags_extract/' + directory, fast = False)
    except Exception as Argument:
        error_log(str(Argument))