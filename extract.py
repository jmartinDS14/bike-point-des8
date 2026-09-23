# Import libraries for making API requests, handling JSON and working with files/folders
import requests
import json
import os
from datetime import datetime
import time
import logging

# API endpoint we want to extract data from
url = 'https://api.tfl.gov.uk/BikePoint/'

# Create a folder for our extracted data if it doesn't already exist
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

# Create a timestamp so each extract gets a unique filename
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
filename = f'{data_dir}/{timestamp}.json'

# Create a folder for log files if it doesn't already exist
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_filename = f'{log_dir}/extract_{timestamp}.log'

# Configure logging so messages are written to the log file
logging.basicConfig(
    filename=log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Create the logger and confirm that it has been successfully set up
logger = logging.getLogger()
logger.info('Logger successfully initialised')


# set up a retry settings in case the API fails
max_retry = 5
attempt = 0
delay = 10

# Keep trying until the maximum number of attempts is reached
while attempt < max_retry:

    # Send a GET request to the API
    response = requests.get(url)
    # Get Status
    status = response.status_code


    # Write an if statement based on the status code
    if 200 <= status < 300:
        # Convert the JSON response into Python variable
        data = response.json()


        # Check that the API returned data before trying to save it
        if len(data) > 0:
            try:

            # Open the output file and write the API data to it as JSON
                with open(filename, 'w') as file:
                    json.dump(data, file)

            # Print new response
                print(f'File {filename} was successfully saved')

            # Add logger info being saved correctly
                logger.info(f'File {filename} was successfully saved')

        # Handle errors that occur while creating or writing to the file

            except Exception as e:
                print(f'An error occurred: {e}')
                # Add logger info
                logger.error(f'An error occurred: {e}')
            break

        # API request succeeded, but no data was returned
        else:
            print('No data returned')
            # Add logger error
            logger.error('No data returned')
            break

        # Retry for client-side errors or server errors
    elif status < 200 or status >= 300:
        print(f'Status code {status}')
        # Wait before retrying to avoid repeatedly hitting the API
        time.sleep(delay)
        attempt += 1
        print(f'Status code {status}. Retrying. This was attempt {attempt}')
        # Add logger info
        logger.info(f'Status code {status}. Retrying. This was attempt {attempt}')
        
# For other errors, don't retry because the issue needs to be fixed
    else:
        print(f'Error. Status code {status}. Fix it.')
        # Add logger info
        logger.error(f'Error. Status code {status}. Fix it.')
        break