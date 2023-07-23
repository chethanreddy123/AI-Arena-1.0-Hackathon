
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# Read the csv file into a pandas dataframe
df = pd.read_csv('data.csv')

# Add a title to the app
st.title('Predictive Analysis')

# Show the sample data frame
st.subheader('Sample Data Frame')
st.write(df.head())

# Create a scatter plot using plotly to visualize the relationship between price and area
fig = px.scatter(df, x='area', y='price', trendline='ols')
st.plotly_chart(fig)

# Split the data into training and testing sets
X = df.drop(['price'], axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Show the regression line and the metrics of the model
fig2 = px.scatter(x=X_test['area'], y=y_test)
fig2.add_traces(px.line(x=X_test['area'], y=y_pred).data)
st.plotly_chart(fig2)

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
st.subheader('Model Metrics')
st.write(f'R2 Score: {r2:.3f}')
st.write(f'Mean Squared Error: {mse:.3f}')
st.write(f'Root Mean Squared Error: {rmse:.3f}')
