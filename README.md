# Copper-Model

In the copper industry, data related to sales and pricing, though less complex, often suffers from skewness and noise, which can hinder accurate manual predictions and optimal pricing decisions. Addressing these issues manually is time-consuming and prone to errors.

Solution Approach:

Data Transformation and Pre-processing:
Transform the data into a suitable format and perform necessary cleaning and pre-processing steps. This includes normalizing and scaling the data to handle skewness, as well as addressing any outliers detected.

Exploring Skewness and Outliers:
Examining the dataset for skewness and outliers. This step is crucial for understanding the distribution of the data and identifying any anomalies that could impact model performance.

ML Regression Model for Pricing Prediction:
Develop a machine learning regression model aimed at predicting the continuous variable ‘Selling_Price’. This model will leverage the cleaned and pre-processed data to make more accurate pricing predictions, mitigating the effects of skewness and noise.

ML Classification Model for Lead Evaluation:
Create a classification model to predict the lead status, specifically focusing on whether a lead is likely to be WON or LOST. The STATUS variable, with 'WON' representing success and 'LOST' representing failure, will be the target variable. Any other status values will be excluded to streamline the model’s focus.

Streamlit Application:
Develop a user-friendly Streamlit page where users can input values for each column. Based on the input, the page will provide either the predicted Selling_Price or the predicted Status (Won/Lost). This interactive interface allows for easy access to model predictions, enhancing decision-making processes in real-time.
