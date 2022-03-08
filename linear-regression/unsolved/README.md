# Table of Contents
- [Purpose](#purpose)
- [Background](#background)
  * [Linear Regression](#linear-regression)
  * [Electric Car Battery Example](#electric-car-battery-example)
    + [Data Source](#data-source)
    + [Explanation](#explanation)
    + [Sources Referred To](#sources-referred-to)
  * [VDK](#vdk)
    * [Create the Data Job Files](#create-the-data-job-files)
    * [Data Job Code](#data-job-code)
    * [Deploy Data Job](#deploy-data-job)
- [Exercises](#exercises)
- [Lessons Learned](#lessons-learned)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Purpose
The purpose of this scenario is to show how to:
* Create a data job with VDK
* Write Python scripts within a data job
* Read from local files (CSV/Excel)
* Perform exploratory data analysis
* Process data
* Build and test a linear regression model
* Create an interactive visualization through Streamlit

If you feel comfortable with the concept of Linear Regression, please feel free to skip down to the
Exercises section, where you will find links to the MyBinder environments.


## Background
### Linear Regression
Linear regression is often referred to as the building block of statistical learning methods. In a nutshell,
it is an attempt to model a relationship between two or more variables by fitting a linear equation
to the data at hand. For example, suppose you plot people's salaries on the y-axis and their years of
education on the x-axis in a simple scatter plot. In this sense, you are trying to estimate a dependent 
variable (salary) by using a predictor (years of education) by drawing a line of best fit through the data.
A line of best fit is a line that minimizes the sum of the distances from itself to each point in the data. The resulting
line's slope, is the coefficient of the predictor (i.e., what kind of effect one unit change of years of education
has on the predicted salary). For example, let's say that the line of best fit follows the equation below:
```
y = 30000 + 5000x1, where y = salary, x1 = years of education, and 30000 is a constant y intercept
```
This means that for one more year of education, a person's salary is estimated to increase by 5000, all else held constant.
Thus, for someone with 12 years of education, their predicted salary is:
```
y = 30000 + 5000*(12)
y = 90000
```
This is a rather simplistic example. In reality, we know there are many factors that influence a person's salary.
This is where multivariate linear regression comes into play. For example, suppose you now have information not only on
the person's salary and years of education, but their parents' last combined income, the years of work experience,
etc. You can estimate a model where each factor's effect is being considered, though visualizing the line of best fit
will get more difficult as you keep adding dimensions! Not to worry, the math still works! Here's an example of a
multivariate linear regression:
```
salary = 20000 + 4000*years_of_education + 1.1*last_combined_parents_income + 1000*years_of_experience
```
Thus, a person with 12 years of education, 100000 as their parents' last combined income and 5 years of experience
is estimated to earn:
```
y = 20000 + 4000*12 + 1.1*100000 + 1000*5
y = 183000
```
Linear regression contains a lot of aspects to it that need to be considered. Topics such as:
* How to estimate the coefficients
* The tradeoff between bias and variance
* Measuring the quality of fit and model accuracy
* Omitted variable bias
* Non-linear transformations of the predictors
* Interaction and dummy/binary variables

are only just a handful of topics that need to be considered. For a much better and a lot more detailed explanation of
linear regression (and statistical methods, in general) please visit: https://www.statlearning.com/.

### Electric Car Battery Example
#### Data Source 
https://www.kaggle.com/gktuzgl/id-3-pro-max-ev-consumption-data

#### Explanation
Using the data provided by Göktuğ Özgül on Kaggle.com, we will build a simple linear regression
model that predicts battery drainage: how much will your electric car's battery drain if you drive it 
in certain ways. For example, how much should you expect your battery to be drained if you drive 50 km at
50 km per hour, using heated seats?

We will cover:
* How to read in the data and deal with special characters
* How to explore the data, both for numerical variables and categorical variables
* How to process the data and very light feature engineering (i.e., creating new variables from existing ones)
* How to deal with multicollinearity
* One of the many possible ways to perform feature selection
* How to deal with possible data leakage
* How to build a simple linear regression model
* How to extract the results and predictions from the model
* How to build a simple Streamlit dashboard showcasing your model's predictive ability

#### Sources Referred To
* https://www.kaggle.com/gktuzgl/id-3-pro-max-ev-consumption-data
* https://www.statlearning.com/
* https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#sphx-glr-auto-examples-linear-model-plot-ols-py
* https://towardsdatascience.com/feature-selection-with-pandas-e3690ad8504b
* https://www.youtube.com/watch?v=Klqn--Mu2pE
* https://medium.com/codex/step-by-step-guide-to-simple-and-multiple-linear-regression-in-python-867ac9a30298

### VDK 
Versatile Data Kit feature allows you to implement automated pull ingestion and batch data processing.

#### Create the Data Job Files

Data Job directory can contain any files, however there are some files that are treated in a specific way:

* SQL files (.sql) - called SQL steps - are directly executed as queries against your configured database;
* Python files (.py) - called Python steps - are Python scripts that define run function that takes as argument the job_input object;
* config.ini is needed in order to configure the Job. This is the only file required to deploy a Data Job;
* requirements.txt is an optional file needed when your Python steps use external python libraries.

Delete all files you do not need and replace them with your own.

#### Data Job Code

VDK supports having many Python and/or SQL steps in a single Data Job. Steps are executed in ascending alphabetical order based on file names.
Prefixing file names with numbers makes it easy to have meaningful file names while maintaining the steps' execution order.

Run the Data Job from a Terminal:
* Make sure you have vdk installed. See Platform documentation on how to install it.
```
vdk run <path to Data Job directory>
```

#### Deploy Data Job

When a Job is ready to be deployed in a Versatile Data Kit runtime (cloud):
Run the command below and follow its instructions (you can see its options with `vdk --help`)
```python
vdk deploy
```

## Exercises
Please open up MyBinder to get started on the exercises!

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AlexanderAvramov/amld-linear-regression-example-empty/HEAD?labpath=setup.ipynb)

You can find the **solved** MyBinder environment here:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AlexanderAvramov/amld-linear-regression-example/HEAD?labpath=setup.ipynb)

For more information on MyBinder, please visit:

https://mybinder.readthedocs.io 

## Lessons Learned
Through this scenario, you created a data job, which:
* Read in a local CSV file and stripped it off its special characters
* Performed exploratory data analysis
* Used the results from the exploratory data analysis to process the data
* Built and tested a linear regression model
* Built an interactive Streamlit dashboard, which showcased your model's predictive ability

Congrats!




