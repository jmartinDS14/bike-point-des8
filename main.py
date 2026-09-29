from modules.log_initialise import setup_logging
from modules.extract_function import extract_json
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

logger = setup_logging('logs', timestamp)
logger.info('Logger successfully initialised')

# API endpoint we want to extract data from
url = 'https://api.tfl.gov.uk/BikePoint/'

# Create a folder for our extracted data if it doesn't already exist
data_dir = 'data'

# set up a retry settings in case the API fails
max_retry = 5
delay = 10

extract_json(url,data_dir,timestamp,max_retry,delay)