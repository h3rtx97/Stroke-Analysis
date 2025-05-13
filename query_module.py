#!/usr/bin/env python
# coding: utf-8

# In[47]:


from dataset_module import load_dataset
import csv
import math


# In[49]:


def calculate_average(number):
    # Check if the input list is empty
    if not number:
        # Return None for empty input to avoid division by zero
        return None
    
    # Calculate and return the average (sum divided by count)
    return sum(number) / len(number)


# In[51]:


def calculate_mode(number):
    # Handle empty input case
    if not number:
        return None
    
    # Create frequency dictionary to count occurrences of each number
    frequency = {}
    for n in number:
        # Increment count for current number (initialize with 0 if first occurrence)
        frequency[n] = frequency.get(n, 0) + 1
    
    # Find the maximum frequency value
    max_freq = max(frequency.values())
    
    # Collect all numbers that have the maximum frequency
    modes = []
    for num, freq in frequency.items():
        if freq == max_freq:
            modes.append(num)
    
    # Return the first mode encountered (even if multiple modes exist)
    return modes[0]


# In[53]:


def calculate_median(number):
    # Check for empty input list
    if not number:
        return None
    
    # Sort the numbers in ascending order
    sort_num = sorted(number)
    
    # Get the length of the sorted list
    n = len(sort_num)
    
    # Find the middle index
    middle = n // 2
    
    # Check if the list has even number of elements
    if n % 2 == 0:
        # For even length, return average of two middle numbers
        return (sort_num[middle - 1] + sort_num[middle]) / 2
    else:
        # For odd length, return the middle number directly
        return sort_num[middle]


# In[57]:

#(i)A function for computing the average age, modal age, median age of those who smoked and had hypertensions that resulted in stroke.
def smoker_with_hypertension(data):
    # Initialize empty list to store ages of qualifying patients
    ages = []

    # Process each patient record in the dataset
    for patient in data.values():
        # Get and standardize smoking status (convert to string, lowercase, strip whitespace)
        smoking_status = str(patient.get('Smoking Status', '')).strip().lower()
        
        # Get hypertension and stroke status (default to '0' if not found)
        hypertension = str(patient.get('Hypertension', '0')).strip()
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Check if patient meets all three criteria:
        # 1. Current or former smoker
        # 2. Has hypertension (value '1')
        # 3. Had a stroke (value '1')
        if smoking_status in ['smokes', 'formerly smoked'] and hypertension == '1' and stroke == '1':
            # If qualified, get age (convert to float) and add to ages list
            age = float(patient.get('Age')) 
            ages.append(age)
    
    # Calculate statistics using helper functions
    avg = calculate_average(ages)    # Average age
    mode = calculate_mode(ages)      # Most frequent age
    median = calculate_median(ages)  # Middle age value
    
    # Package results in dictionary
    results = {
        'Average Age': avg,
        'Modal Age': mode, 
        'Median Age': median
    }

    # Save results to CSV file if data exists
    if results:
        with open('smoker_with_hypertension.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()    # Write column headers
            writer.writerow(results) # Write data row
    else:
        print("No matching data to save.")
    
    return results


# In[62]:

#(ii)A function for computing the average age, modal age, median age, and average glucose level of those who had heart disease that resulted in stroke. 
def heart_disease(data):
    # Initialize lists to store ages and glucose levels of qualifying patients
    ages = []
    glucose_level = []

    # Process each patient record in the dataset
    for patient in data.values():
        # Get and standardize heart disease and stroke status
        # (convert to string, strip whitespace, default to '0' if not found)
        heart_disease = str(patient.get('Heart Disease', '0')).strip()
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Check if patient has both heart disease and stroke (values = '1')
        if heart_disease == '1' and stroke == '1':
            # If qualified, get age and glucose level (convert to float)
            age = float(patient.get('Age'))
            glucose = float(patient.get('Average Glucose Level'))
            
            # Add to respective lists
            ages.append(age)
            glucose_level.append(glucose)

    # Calculate statistics using helper functions
    avg = calculate_average(ages)            # Average age
    mode = calculate_mode(ages)              # Most frequent age
    median = calculate_median(ages)          # Middle age value
    avg_g = calculate_average(glucose_level)  # Average glucose level

    # Package results in dictionary
    results = {
        'Average Age': avg,
        'Modal Age': mode,
        'Median Age': median,
        'Average Glucose Level': avg_g
    }

    # Save results to CSV file if data exists
    if results:
        with open('heart_disease.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()    # Write column headers
            writer.writerow(results) # Write data row
    else:
        print("No matching data to save.")
    
    return results


# In[17]:

#(iii)A function for computing the average age, modal age, median age of patients based on genders of those whose hypertensions resulted in stroke and of those whose hypertensions did not result in stroke. 
def gender_hypertension_stroke(data):
    # Initialize dictionaries to store age data by gender
    # Using dictionaries to efficiently group by gender
    stroke_member = {} # we need to use dict because we can't slice list !
    no_stroke_member = {} # we need to use dict because we can't slice list !

    # Process each patient record
    for patient in data.values():
        # Get and standardize gender (string, lowercase, strip whitespace)
        gender = str(patient.get('Gender', '')).strip().lower()
        
        # Get hypertension and stroke status (string, strip whitespace)
        hypertension = str(patient.get('Hypertension', '0')).strip()
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Get patient age (convert to float)
        age = float(patient.get('Age'))

        # Categorize patients based on hypertension and stroke status
        if hypertension == '1' and stroke == '1':
            # Hypertension patients who had a stroke
            if gender not in stroke_member:
                stroke_member[gender] = []  # Initialize list for new gender
            stroke_member[gender].append(age)  # Add age to gender group

        elif hypertension == '1' and stroke == '0':
            # Hypertension patients who didn't have a stroke
            if gender not in no_stroke_member:
                no_stroke_member[gender] = []  # Initialize list for new gender
            no_stroke_member[gender].append(age)  # Add age to gender group

    # Initialize results dictionary structure
    results = {
        "stroke_hypertension": {},  # Will store stats for stroke patients
        "no_stroke_hypertension": {}  # Will store stats for non-stroke patients
    }

    # Calculate statistics for each gender group with stroke
    for gender, ages in stroke_member.items():
        results["stroke_hypertension"][gender] = {
            "Average Age": calculate_average(ages),
            "Modal Age": calculate_mode(ages),
            "Median Age": calculate_median(ages)
        }

    # Calculate statistics for each gender group without stroke
    for gender, ages in no_stroke_member.items():
        results["no_stroke_hypertension"][gender] = {
            "Average Age": calculate_average(ages),
            "Modal Age": calculate_mode(ages),
            "Median Age": calculate_median(ages)
        }

    # Save results to CSV if data exists
    if results:
        with open('gender_hypertension_stroke.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()  # Write column headers
            writer.writerow(results)  # Write data row
    else:
        print("No matching data to save.")

    return results


# In[72]:

#(iv)A function for computing the average age, modal age, median age of those whose smoking habits result in stroke and for those whose smoking habit did not result in stroke
def smoke_stroke(data):
    # Initialize lists to store ages of smokers
    stroke_smoker = []  # Will store ages of smokers who had a stroke
    no_stroke_smoker = []  # Will store ages of smokers without stroke

    # Process each patient record
    for patient in data.values():
        # Get and standardize smoking status (string, lowercase, strip whitespace)
        smoking_status = str(patient.get('Smoking Status', '')).strip().lower()
        
        # Get stroke status (string, strip whitespace)
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()
        
        # Get patient age (convert to float)
        age = float(patient.get('Age'))

        # Only consider patients who have smoked (current or former smokers)
        if smoking_status != 'never smoked':
            # Categorize based on stroke occurrence
            if stroke == '1':
                stroke_smoker.append(age)  # Add to stroke group
            elif stroke == '0':
                no_stroke_smoker.append(age)  # Add to non-stroke group

    # Compile results with age statistics for both groups
    results = {
        "Smoking result in stroke": {
            "Average Age": calculate_average(stroke_smoker),
            "Modal Age": calculate_mode(stroke_smoker),
            "Median Age": calculate_median(stroke_smoker)
        },
        "Smoking did not result in stroke": {
            "Average Age": calculate_average(no_stroke_smoker),
            "Modal Age": calculate_mode(no_stroke_smoker),
            "Median Age": calculate_median(no_stroke_smoker)
        }
    }

    # Save results to CSV file if data exists
    if results:
        with open('smoke_stroke.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()  # Write column headers
            writer.writerow(results)  # Write data row
    else:
        print("No matching data to save.")

    return results


# In[100]:

#(v)A function for computing the average age, modal age, median age of those who lived in urban areas and for those in rural areas that had stroke. 
def urban_rural_stroke(data):
    # Initialize lists to store ages of stroke patients by residence type
    urban_ages = []  # Will store ages of urban residents with stroke
    rural_ages = []  # Will store ages of rural residents with stroke

    # Process each patient record
    for patient in data.values():
        # Get and standardize residence type (string, lowercase, strip whitespace)
        region = str(patient.get('Residence Type','')).strip().lower()
        
        # Get stroke status (string, strip whitespace)
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()
        
        # Get patient age (convert to float)
        age = float(patient.get('Age'))

        # Only consider patients who had a stroke
        if stroke == '1':
            # Categorize based on residence type
            if region == 'urban':
                urban_ages.append(age)  # Add to urban group
            elif region == 'rural':
                rural_ages.append(age)  # Add to rural group

    # Compile results with age statistics for both residence types
    results = {
        "Stroke in Urban Residents": {
            "Average Age": calculate_average(urban_ages),
            "Modal Age": calculate_mode(urban_ages),
            "Median Age": calculate_median(urban_ages)
        },
        "Stroke in Rural Residents": {
            "Average Age": calculate_average(rural_ages),
            "Modal Age": calculate_mode(rural_ages),
            "Median Age": calculate_median(rural_ages)
        }
    }

    # Save results to CSV file if data exists
    if results:
        with open('urban_rural_stroke.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()  # Write column headers
            writer.writerow(results)  # Write data row
    else:
        print("No matching data to save.")

    return results


# In[20]:

#(vi)A function to retrieve the dietary habit(s) of those who had stroke and those who did not have stroke. 
def diet_stroke(data):
    # Initialize sets to store unique dietary habits
    # Using sets automatically removes duplicate values
    stroke_diet = set()  # Stores unique diets of stroke patients
    no_stroke_diet = set()  # Stores unique diets of non-stroke patients

    # Process each patient record
    for patient in data.values():
        # Get and standardize dietary habits (string, lowercase, strip whitespace)
        diet = str(patient.get('Dietary Habits', '').strip().lower())
        
        # Get stroke status (string, strip whitespace)
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Skip patients with empty dietary information
        if not diet:
            continue

        # Categorize dietary habits based on stroke occurrence
        if stroke == '1':
            stroke_diet.add(diet)  # Add to stroke group (automatically handles duplicates)
        elif stroke == '0':
            no_stroke_diet.add(diet)  # Add to non-stroke group (automatically handles duplicates)

    # Compile results with unique dietary habits for both groups
    results = {
        "Dietary habits of people who had a stroke": stroke_diet,
        "Dietary habits of people who did not have a stroke": no_stroke_diet
    }

    # Save results to CSV file if data exists
    if results:
        with open('diet_stroke.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()  # Write column headers
            writer.writerow(results)  # Write data row
    else:
        print("No matching data to save.")
        
    return results


# In[21]:

#(vii)A function that returns anyone whose hypertension resulted in stroke. 
def hypertension_with_stroke(data):
    # Initialize empty list to store qualifying patient records
    results = []

    # Process each patient record in the dataset
    for patient in data.values():
        # Get and standardize hypertension status (convert to string, strip whitespace)
        hypertension = str(patient.get('Hypertension', '0')).strip()
        
        # Get and standardize stroke status (convert to string, strip whitespace)
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Check if patient has both hypertension and stroke (values = '1')
        if hypertension == '1' and stroke == '1':
            # Add complete patient record to results list
            results.append(patient)

    # Save results to CSV file if any matching records were found
    if results:
        with open('hypertension_with_stroke.csv', 'w', newline='') as file:
            # Create CSV writer using keys from first record as column headers
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()    # Write column headers
            writer.writerows(results)  # Write all qualifying records
    else:
        print("No matching records to save.")
        
    return results


# In[45]:

#(viii)A function to retrieve those who hypertension did not result in stroke and those whose hypertension resulted in stroke.
def stroke_hypertension(data):
    # Initialize lists to store categorized patient records
    stroke_hypertension = []    # Hypertension patients with stroke
    no_stroke_hypertension = [] # Hypertension patients without stroke

    # Process each patient record
    for patient in data.values():
        # Get and standardize hypertension status (string, strip whitespace)
        hypertension = str(patient.get('Hypertension', '0')).strip()
        
        # Get and standardize stroke status (string, strip whitespace)
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Only process hypertension patients
        if hypertension == '1':
            # Create copy to avoid modifying original data
            patient_copy = patient.copy()  
            
            # Categorize based on stroke status
            if stroke == '1':
                patient_copy['Stroke_Status'] = 'Stroke'  # Add status field
                stroke_hypertension.append(patient_copy)
            elif stroke == '0':
                patient_copy['Stroke_Status'] = 'No Stroke'  # Add status field
                no_stroke_hypertension.append(patient_copy)

    # Combine both groups into single results list
    results = stroke_hypertension + no_stroke_hypertension
    
    # Save results to CSV if data exists
    if results:
        with open('Stroke_and_no_stroke_hypertension.csv', 'w', newline='') as file:
            # Get field names from first record (includes new Stroke_Status field)
            fieldnames = results[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write column headers
            writer.writerows(results)  # Write all patient records
    else:
        print("No hypertension data to save.")

    return results


# In[82]:

#(ix)A function that returns everyone with heart disease with stroke. 
def everyone_heart_disease_stroke(data):
    # Initialize an empty list to store qualifying patient records
    results = []

    # Iterate through each patient record in the dataset
    for patient in data.values():
        # Standardize and retrieve heart disease status (convert to string, strip whitespace)
        # Default to '0' if field is missing
        heart_disease = str(patient.get('Heart Disease', '0')).strip()
        
        # Standardize and retrieve stroke occurrence status (convert to string, strip whitespace)
        # Default to '0' if field is missing
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Check if patient has both conditions (heart disease and stroke)
        if heart_disease == '1' and stroke == '1':
            # Add complete patient record to results
            results.append(patient)

    # Only proceed if we found matching records
    if results:
        # Open CSV file for writing
        with open('everyone_heart_disease_stroke.csv', 'w', newline='') as file:
            # Create CSV writer using field names from first patient record
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            
            # Write header row using patient attribute names
            writer.writeheader()
            
            # Write all qualifying patient records
            writer.writerows(results)
    else:
        # Inform user if no matching patients were found
        print("No matching data to save.")
        
    # Return the list of qualifying patient records (empty if none found)
    return results


# In[86]:

#(x)A function that returns the descriptive statistics of any of the features of the dataset. This function should ask for which feature to analyse and then return the statistics. The descriptive statistics are mean, standard deviation, minimum, maximum, 25%, 50%, and 75%.
def descriptive_statistics (data, feature):
    # Initialize list to store valid numeric values
    val = []
    
    # Process each patient record
    for patient in data.values():
        try:
            # Attempt to convert feature value to float after cleaning
            value = float(str(patient.get(feature, '')).strip())
            val.append(value)
        except ValueError:
            # Skip non-numeric values silently
            continue

    # Check if we found any numeric values
    if not val:
        return f"There should be numeric data for feature '{feature}'!"
    
    # Calculate Mean (average)
    mean = calculate_average(val)
    
    # Calculate Standard Deviation
    val.sort()  # Sort values for percentile calculations
    n = len(val)
    # Variance calculation (average of squared differences from mean)
    variance = sum((x - mean) ** 2 for x in val) / n
    std_dev = math.sqrt(variance)  # Square root of variance
    
    # Get Minimum and Maximum values
    min_val = val[0]  # First element after sorting
    max_val = val[-1]  # Last element after sorting
    
    # Helper function to calculate percentiles
    def percentile(a):
        # Calculate the index position in the sorted data array for the given percentile
        b = (a / 100) * (n - 1)
        # Take the floor and ceiling of the index
        f = math.floor(b) # lower index
        c = math.ceil(b) # higher index
        # If index is an integer, return the value directly
        if f == c:
            return val[int(b)]
        # Linear interpolation between the two surrounding values
        d0 = val[int(f)] * (c - b) # value at lower index, weighted by how close b is to the higher index.
        d1 = val[int(c)] * (b - f) # value at upper index, weighted by how close b is to the lower index.
        # Return the interpolated result
        return d0 + d1

    # Calculate key percentiles
    p25 = percentile(25)  # First quartile
    p50 = percentile(50)  # Median (second quartile)
    p75 = percentile(75)  # Third quartile

    # Compile results dictionary with feature-specific labels
    results = {
        f"Mean of {feature}": mean,
        f"Standard Deviation of {feature}'": std_dev,
        f"Min of {feature}": min_val,
        f"Max of {feature}": max_val,
        f"25% of {feature}": p25,
        f"50% of {feature}": p50,
        f"75% of {feature}": p75
    }

    # Save results to CSV if data exists
    if results:
        with open('descriptive_statistics.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()
            writer.writerow(results)
    else:
        print("No matching data to save.")
        
    return results


# In[98]:

#(xi)A function to retrieve the average sleep hours of those who had stroke and those who did not have stroke.
def avg_sleep_stroke(data):
    # Initialize lists to store sleep hours for each group
    stroke_sleep = []    # Will store sleep hours of patients who had a stroke
    no_stroke_sleep = [] # Will store sleep hours of patients without stroke

    # Process each patient record
    for patient in data.values():
        # Get and convert sleep hours to float after cleaning string
        # Note: This will raise ValueError if conversion fails on non-numeric data
        sleep = float(str(patient.get('Sleep Hours', '')).strip())
        
        # Get stroke status (string, strip whitespace, default to '0' if not found)
        stroke = str(patient.get('Stroke Occurrence', '0')).strip()

        # Categorize sleep hours based on stroke occurrence
        if stroke == '1':
            stroke_sleep.append(sleep)  # Add to stroke group
        elif stroke == '0':
            no_stroke_sleep.append(sleep)  # Add to non-stroke group

    # Calculate average sleep hours for both groups
    results = {
        "Average sleep hours with stroke": calculate_average(stroke_sleep),
        "Average sleep hours without stroke": calculate_average(no_stroke_sleep)
    }

    # Save results to CSV file if data exists
    if results:
        with open('avg_sleep_stroke.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=results.keys())
            writer.writeheader()  # Write column headers
            writer.writerow(results)  # Write data row
    else:
        print("No matching data to save.")

    return results


# In[ ]:




