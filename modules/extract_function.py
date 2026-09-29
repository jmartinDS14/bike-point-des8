# Import libraries for making API requests, handling JSON and working with files/folders
import requests
import json
import os
import time
import logging

logger = logging.getLogger(__name__)

def extract_json(url:str, data_dir:str, timestamp:str, max_retry:int, delay:int):
    """Extracts JSON from specified URL and saves it locally in the data_dir

    Args:
        url (str): The URL you want to download JSON from
        data_dir (str): Where to save the data
        timestamp (str): The filename will be this
        max_retry (int): The number of time to retry the API
        delay (int): How long to wait between retries (seconds)
    """

    os.makedirs(data_dir, exist_ok=True)

    filename = f'{data_dir}/{timestamp}.json'

    # set up a retry settings in case the API fails
    attempt = 0

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