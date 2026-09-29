from modules.log_initialise import setup_logging
from modules.extract_function import extract_json
from modules.load_function import load_files_to_s3
from dotenv import load_dotenv
from datetime import datetime
import os

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

load_dotenv()

AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME=os.getenv('AWS_BUCKET_NAME')

load_files_to_s3(data_dir, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME)