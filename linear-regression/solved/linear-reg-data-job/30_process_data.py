import pandas as pd
import numpy as np
import logging
import pathlib
import os
from vdk.api.job_input import IJobInput

logger = logging.getLogger(__name__)
os.chdir(pathlib.Path(__file__).parent.absolute())

def run(job_input: IJobInput):
    logger.info('executing program: ' + os.path.basename(__file__))

    # some definitions...
    filename_to_import = 'VW ID. 3 Pro Max EV Consumption_Fixed_Columns.csv'
    filename_to_export = 'VW ID. 3 Pro Max EV Consumption_Model_Data.csv'

    # reading in the data...
    df = pd.read_csv(filepath_or_buffer=filename_to_import, parse_dates=['date'])

    # dropping missing values...
    df_no_nulls = df.copy().dropna()

    # encoding the categorical variables....
    df_no_nulls['ac_use'] = np.where(
        df_no_nulls['ac_c'] == 'OFF', 0, 1
    )
    df_no_nulls['heated_seats'] = np.where(
        df_no_nulls['heated_front_seats_level'] == 0, 0, 1
    )
    df_no_nulls['eco_mode'] = np.where(
        df_no_nulls['mode'] == 'ECO', 1, 0
    )
    df_no_nulls["is_summer"] = np.where(
        (df_no_nulls['date'] >= '2021-06-21') & (df_no_nulls['date'] <= '2021-09-22'), 1, 0
    )
    df_no_nulls['is_bridgestone_tyre'] = np.where(
        df_no_nulls['tyres'] == 'Bridgestone 215/45 R20 LM32', 1, 0
    )

    # creating additional variables...
    df_no_nulls['battery_drain'] = \
        -(df_no_nulls['charge_level_end'] - df_no_nulls['charge_level_start'])
    df_no_nulls['temperature_increase'] = \
        df_no_nulls['temperature_end_c'] - df_no_nulls['temperature_start_c']

    # clearing the dataset of all the clutter...
    df_no_nulls_limited = df_no_nulls.copy()[
        [
            'battery_drain',
            'charge_level_start',
            'is_bridgestone_tyre',
            'temperature_start_c',
            'temperature_increase',
            'distance_km',
            'average_speed_kmh',
            'average_consumption_kwhkm',
            'ac_use',
            'heated_seats',
            'eco_mode',
            'is_summer'
        ]
    ]

    # observing the processed data and making corrections, as needed...
    logger.info(df_no_nulls_limited.describe())  # we see a possible data error
    logger.info(df_no_nulls_limited.loc[df_no_nulls_limited['battery_drain'] < 0])  # this is an error we have to remove
    df_no_nulls_limited_final = df_no_nulls_limited.copy().loc[
        df_no_nulls_limited['battery_drain'] >= 0]
    logger.info(df_no_nulls_limited_final.describe())  # looks good now

    # saving the processed data...
    df_no_nulls_limited_final.to_csv(
        path_or_buf=filename_to_export,
        index=False
    )
