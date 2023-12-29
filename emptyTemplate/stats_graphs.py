import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, redirect, url_for, flash, render_template, session
from matplotlib.dates import date2num
from werkzeug.utils import secure_filename
import os
import pandas as pd
import matplotlib.pyplot as plt
import stats_graphs as sg
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact
from datetime import datetime

def generate_first_three_rows(data):
    return data.head(3).to_html()

def generate_average_age(data):
    average_age = data['Age'].mean()
    return f"Average Age: {average_age}"

def generate_stat1(data):
    most_common_join_date = data['JoinDate'].mode()[0]
    return f"Most Common Join Date: {most_common_join_date}"


def generate_stat2(data):
    # Inspired by ipynb file, code cell 2
    # Convert JoinDate to datetime
    data['JoinDate'] = pd.to_datetime(data['JoinDate'])
    # Calculate tenure in days
    current_date = datetime.now()
    data['Tenure'] = (current_date - data['JoinDate']).dt.days
    # Calculate average tenure by job
    average_tenure_by_job = data.groupby('Job')['Tenure'].mean()

    # Format the output as a table
    formatted_output = average_tenure_by_job.reset_index()
    formatted_output.columns = ['Job', 'Average Tenure (days)']

    # Convert to a string
    output_string = formatted_output.to_string(index=False)

    return "Average Tenure by Job (in days):\n" + output_string


def generate_stat3(data):
    # Inspired by ipynb file, code cell 3
    # Define age groups
    age_bins = [20, 30, 40, 50, 60, 70]
    age_labels = ['20s', '30s', '40s', '50s', '60s', ]
    data['AgeGroup'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels, right=False)
    # Calculate standard deviation of salary within each age group
    salary_variation = data.groupby('AgeGroup')['Salary'].std()

    # Format the output as a table
    formatted_output = salary_variation.reset_index()
    formatted_output.columns = ['Age Group', 'Salary Standard Deviation']

    # Convert to a string
    output_string = formatted_output.to_string(index=False)

    return "Salary Standard Deviation by Age Group:\n" + output_string


def generate_graph(data):
    # The line graph
    sorted_data = data.sort_values(by='Age')
    plt.figure()
    plt.plot(sorted_data['Age'], sorted_data['Salary'], marker='o', linestyle='-')
    plt.title('Salary Distribution Over Age')
    plt.xlabel('Age')
    plt.ylabel('Salary')
    plt.grid(True)
    
    
    graph_filename = 'graph.png'
    plt.savefig('static/' + graph_filename)
    plt.show()

def generate_graph1(data):
    # Scatter plot of age vs salary
    plt.scatter(data['Age'], data['Salary'])
    plt.xlabel('Age')
    plt.ylabel('Salary')
    plt.title('Age vs Salary')
    plt.grid(True)
    
    
    graph_filename = 'graph1.png'
    plt.savefig('static/' + graph_filename)
    plt.show()

def generate_graph2(data):
    # Pie chart of Department Distribution
    plt.figure()
    data['Department'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title('Department Distribution')
    plt.axis('equal')
    
    #dont edit below
    graph_filename = 'graph2.png'
    plt.savefig('static/' + graph_filename)
    plt.show()

def generate_graph3(data):
    # Generate box plot of Salary by Department
    plt.figure(figsize=(12, 8))
    boxplot = data.boxplot(column='Salary', by='Department', grid=True, vert=True)
    plt.title('Salary Distribution by Department')
    plt.suptitle('')
    plt.xlabel('Department')
    plt.ylabel('Salary')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', axis='y')
    plt.tight_layout()
    #dont edit below
    graph_filename = 'graph3.png'
    plt.savefig('static/' + graph_filename)
    plt.show()

def generate_graph4(data):
    # Histogram of Salary Distribution
    plt.figure()
    plt.hist(data['Salary'], bins=20, color='blue', alpha=0.7, edgecolor='black')
    plt.title('Salary Distribution Histogram')
    plt.xlabel('Salary')
    plt.ylabel('Number of Employees')
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray')

    #dont edit below
    graph_filename = 'graph4.png'
    plt.savefig('static/' + graph_filename)
    plt.show()

def scatter_view(x, y, z):
    # Init figure and axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Compute scatter plot
    ax.scatter(x, y, z, c='blue', marker='o')

    # Set labels and title
    ax.set_xlabel('Age', fontsize=16)
    ax.set_ylabel('Salary', fontsize=16)
    ax.set_zlabel('Join Month (2022)', fontsize=16)
    ax.set_title('3D Scatter Plot of Age, Salary, and Join Month for 2022')

    #dont edit below
    graph_filename = 'graph5.png'
    plt.savefig('static/' + graph_filename)
    plt.show()

def generate_graph5(data):
    # Prepare the data frame
    data['JoinDate'] = pd.to_datetime(data['JoinDate'])
    data_2022 = data[data['JoinDate'].dt.year == 2022]
    data_2022['JoinMonth'] = data_2022['JoinDate'].dt.month

    # Extract the columns
    xi = data_2022['Age']
    yi = data_2022['Salary']
    zi = data_2022['JoinMonth']

    scatter_view(xi, yi, zi)


if __name__=="__main__":
    data = pd.read_csv("test.csv")

    generate_graph(data)
    generate_graph1(data)
    generate_graph2(data)
    generate_graph3(data)
    generate_graph4(data)
    generate_graph5(data)
    print(generate_first_three_rows(data))
    print(generate_average_age(data))
    print(generate_stat1(data))
    print(generate_stat2(data))
    print(generate_stat3(data))

    print("Done.")

