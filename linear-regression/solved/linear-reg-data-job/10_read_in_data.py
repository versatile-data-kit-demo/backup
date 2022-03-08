import pandas as pd
import os
import logging
import pathlib
from vdk.api.job_input import IJobInput

logger = logging.getLogger(__name__)
os.chdir(pathlib.Path(__file__).parent.absolute())

def run(job_input: IJobInput):
    logger.info('executing program: ' + os.path.basename(__file__))

    # some definitions...
    filename_to_import = 'VW ID. 3 Pro Max EV Consumption.csv'
    filename_to_export = 'VW ID. 3 Pro Max EV Consumption_Fixed_Columns.csv'

    # reading in the data with special characters...
    df = pd.read_csv(
        filepath_or_buffer=filename_to_import,
        encoding='ISO-8859-1',
        parse_dates=['Date']
    )

    # stripping the non-alphanumeric characters in the column names and standardizing them...
    df.columns = df.columns.\
        str.replace('[^a-zA-Z ]', '').\
        str.strip().\
        str.replace(' ', '_').\
        str.lower()

    # saving the dataset...
    df.to_csv(path_or_buf=filename_to_export, index=False)
