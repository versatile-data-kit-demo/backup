import os
import pandas as pd
import pickle
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pathlib
import streamlit as st
from parameters import parameters

# setting up the title of the page...
st.title('Electric Cars and Battery Drain Linear Regression Example')

# setting up the sub-header for the first part of the page...
st.header("Our Simple Model's Accuracy")
st.write("How Did Our Model Perform?")

# some definitions...
os.chdir(pathlib.Path(__file__).parent.absolute())
actual_vs_pred_loc = 'linear-reg-data-job/model/actual_vs_model_predicted_battery_drain_test.csv'
model_loc = 'linear-reg-data-job/model/amld_linear_regression_model.sav'

# reading in the actual versus predicted data set...
actual_vs_pred = pd.read_csv(actual_vs_pred_loc, usecols=range(1, 3))
actual_vs_pred['absolute_difference'] = abs(
    actual_vs_pred['battery_drain'] - actual_vs_pred['battery_drain_prediction']
)
st.dataframe(actual_vs_pred)
battery_drain = actual_vs_pred[['battery_drain']]
battery_drain_prediction = actual_vs_pred[['battery_drain_prediction']]

# outputting some performance metrics...
mse = round(mean_squared_error(battery_drain, battery_drain_prediction), 2)
mae = round(mean_absolute_error(battery_drain, battery_drain_prediction), 2)
r2  = round(r2_score(battery_drain, battery_drain_prediction), 2)

st.metric("The Mean Squared Error of This Model On This Testing Data Is:", mse)
st.metric("The Mean Absolute Error of This Model On This Testing Data Is:", mae)
st.metric("The R2 is:", r2)

# setting up the sub-headers for the second part of the page...
st.header('How Much Will Your Electric Car Battery Drain? You May Be Surprised!')
st.write("Enter Your Custom Values in the SideBar - Please Enter Sensible Values Only!")

# selecting the user inputs...
results = {}
for measurement, params in parameters.items():
    output = st.sidebar.number_input(**params)
    results[measurement] = output
results_df = pd.DataFrame(results, index=[0])

# reading in the model...
pickled_model = pickle.load(open(model_loc, 'rb'))

# obtaining model prediction...
estimate = pickled_model.predict(results_df)

# printing model prediction...
if estimate > results['charge_level_start']:
    estimate = results['charge_level_start']
    st.metric("Your Estimated Battery Drainage (in Percent) Is:", estimate)
    st.write("Note: The Model's Estimate Exceeds the Starting Level Charge; Thus Estimate is Capped")
elif estimate < 0:
    estimate = 0
    st.metric("Your Estimated Battery Drainage (in Percent) Is:", estimate)
else:
    st.metric("Your Estimated Battery Drainage (in Percent) Is:", estimate)
