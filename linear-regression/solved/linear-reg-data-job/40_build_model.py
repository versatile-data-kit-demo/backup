import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import pickle
import pathlib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from vdk.api.job_input import IJobInput

logger = logging.getLogger(__name__)
os.chdir(pathlib.Path(__file__).parent.absolute())

def run(job_input: IJobInput):
    logger.info('executing program: ' + os.path.basename(__file__))

    # some definitions...
    filename_to_import = 'VW ID. 3 Pro Max EV Consumption_Model_Data.csv'

    # creating a sub-folder to house the model and model related things...
    if not os.path.exists('model'):
        os.makedirs('model')

    # reading in the data created from our processing program...
    df = pd.read_csv(filepath_or_buffer=filename_to_import)

    # splitting the data into a training dataset and a testing dataset...
    y = df.copy()[['battery_drain']]
    x = df.copy().drop('battery_drain', axis=1)
    x_train, x_test, y_train, y_test = train_test_split(
       x,
       y,
       test_size=0.2,
       random_state=22
     )

    # explore the split data
    data_sets = {
        "x_train": x_train,
        "x_test": x_test,
        "y_train": y_train,
        "y_test": y_test
    }
    for name, data_set in data_sets.items():
        logger.info(f"The shape of the {name} dataset is: {data_set.shape}")

    # checking for multicollinearity...
    sns.set(
        style='ticks',
        rc={'figure.figsize': (18, 14)}
    )
    sns.heatmap(
        x_train.corr(),
        annot=True,
        cmap=sns.diverging_palette(10, 250, n=240)
    )
    plt.savefig('explore_data/features_correlation.png')
    # plt.show() the following features need to be dropped: is_bridgestone_tyre, is_summer, and ac_use
    # plt.clf()

    # drop the heavily correlated variables from both the training and testing data sets...
    predictive_data_sets = [x_train, x_test]
    for data_set in predictive_data_sets:
        data_set.drop(['is_bridgestone_tyre', 'is_summer', 'ac_use'], axis=1, inplace=True)

    # using Lasso regularization to delete less important features...
    lasso = LassoCV(normalize=True, random_state=22)
    lasso.fit(
        x_train,
        y_train
    )
    lasso = pd.Series(lasso.coef_, index=x_train.columns)

    # deleting the less important features from the train and test data sets...
    features_to_delete = list(lasso[lasso == 0].index)
    for data_set in predictive_data_sets:
        data_set.drop(features_to_delete, axis=1, inplace=True)

    # fitting the model on the training data...
    linreg = LinearRegression()
    linreg.fit(x_train, y_train)

    # testing the model on testing data and extracting predictions...
    y_pred = linreg.predict(x_test)
    y_pred = pd.DataFrame(y_pred, columns=['battery_drain_prediction'])
    actual_vs_predicted = pd.concat(
        [y_test.copy().reset_index(drop=True), y_pred.copy().reset_index(drop=True)],
        axis=1
    )
    actual_vs_predicted.to_csv('model/actual_vs_model_predicted_battery_drain_test.csv')

    # obtaining model accuracy...
    measurements = {
        'mean squared error': mean_squared_error,
        'mean absolute error': mean_absolute_error,
        'R2': r2_score}
    for measure, func in measurements.items():
        logger.info(f"The {measure} is: {func(y_pred, y_test)}")

    # extracting the coefficients...
    coeff = pd.DataFrame(linreg.coef_).transpose()
    inter = pd.DataFrame(linreg.intercept_).transpose()
    inter_and_coeff = pd.concat(
        [inter, coeff],
        ignore_index=True
    )
    inter_and_coeff.columns = ['coefficients']
    intercept = ['intercept']
    intercept.extend(x_train.columns.to_list())
    feature_names = pd.DataFrame(
        intercept,
        columns=['feature']
    )
    model_coeffs = pd.concat(
        [inter_and_coeff, feature_names],
        axis=1,
        join='outer'
    )
    model_coeffs.to_csv('model/model_coefficients.csv')

    # saving the model...
    filename = 'model/amld_linear_regression_model.sav'
    pickle.dump(linreg, open(filename, 'wb'))
