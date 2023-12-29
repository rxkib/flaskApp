import csv
import random
from faker import Faker

fake = Faker()

# Define the job titles, departments, and locations
job_titles = ['Software Engineer', 'Marketing Specialist', 'Project Manager', 'Data Analyst', 'Graphic Designer', 'HR Manager', 'Product Manager', 'Financial Analyst', 'Sales Representative', 'Operations Director']
departments = ['Engineering', 'Marketing', 'Project Management', 'Analytics', 'Design', 'Human Resources', 'Product Management', 'Finance', 'Sales', 'Operations']
locations = ['San Francisco', 'New York', 'Chicago', 'Los Angeles', 'Miami', 'Dallas', 'Seattle', 'Boston', 'Denver', 'Austin']

# Open the CSV file in append mode
with open('test.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    # Generate 30 more rows of data
    for _ in range(30):
        name = fake.name()
        age = random.randint(25, 45)
        job = random.choice(job_titles)
        join_date = fake.date_between(start_date='-3y', end_date='today')
        salary = random.randint(55000, 95000)
        department = random.choice(departments)
        location = random.choice(locations)
        # Write the data to the CSV file
        writer.writerow([name, age, job, join_date, salary, department, location])