import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging
import pathlib
from vdk.api.job_input import IJobInput

logger = logging.getLogger(__name__)
os.chdir(pathlib.Path(__file__).parent.absolute())

def run(job_input: IJobInput):
    logger.info('executing program: ' + os.path.basename(__file__))

    # creating a sub-folder within our data job folder to store the exploratory graphics and tables...
    if not os.path.exists('explore_data'):
        os.makedirs('explore_data')

    # some definitions...
    filename_to_import = 'VW ID. 3 Pro Max EV Consumption_Fixed_Columns.csv'

    # reading in the data with fixed column names, as outputted from 10_read_in_data.py...
    df = pd.read_csv(filepath_or_buffer=filename_to_import, parse_dates=['date'])

    # exploring the structure of the data...
    logger.info('Information about the data: ')
    logger.info(df.info())
    pd.set_option('display.max.columns', None)
    logger.info(df.head())
    logger.info(df.tail())

    # exploring the numeric variables through plotting histograms...
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    sns.set(
        style='ticks',
        rc={
            'axes.spines.right': False,
            'axes.spines.top': False,
            'figure.figsize': (18, 14)
            }
        )
    for num_col in num_cols:
        sns.distplot(
            df[num_col],
            bins=100).\
            set(xlabel=num_col,
                ylabel='Count'
                )
        plt.savefig('explore_data/' + num_col + '.png')
        # plt.show()
        plt.clf()

    # exploring the categorical variables through examining the commonly occurring values...
    cat_cols = [i for i in df.columns if i not in num_cols]
    cat_writer = pd.ExcelWriter('explore_data/explore_categoricals.xlsx', engine='xlsxwriter')
    for cat_col in cat_cols:
        temp = pd.DataFrame(
            df[cat_col].value_counts(dropna=False)
        )
        temp.to_excel(cat_writer, sheet_name=cat_col)
    cat_writer.save()
