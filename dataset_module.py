#!/usr/bin/env python
# coding: utf-8

# In[2]:


def load_dataset(filename):
    # Initialize an empty dictionary to store the patient data
    data = {}
    
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Read the first line as headers (column names)
            headers = file.readline().strip().split(',')
            
            # Process each subsequent line in the file
            for line in file:
                # Remove any leading/trailing whitespace
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                    
                # Split the line into values using comma as delimiter
                values = line.split(',')
                
                # Skip rows that don't match the header length
                if len(values) != len(headers):
                    continue
                
                # Create a patient record dictionary
                # First value is assumed to be the patient ID
                patient_id = values[0]
                patient_data = {}
                
                # Process each field (skip first column which is patient_id)
                for i in range(1, len(headers)):
                    # Get the field name from headers and clean it
                    key = headers[i].strip()
                    # Get the corresponding value and clean it
                    value = values[i].strip()
                    
                    # Convert numeric values to appropriate types
                    if value.replace('.', '', 1).isdigit():  # Check if value is numeric
                        if '.' in value:  # Float number
                            value = float(value)
                        else:  # Integer number
                            value = int(value)
                    # Convert string 'true'/'false' to boolean
                    elif value.lower() == 'true':
                        value = True
                    elif value.lower() == 'false':
                        value = False
                    
                    # Add the processed value to the patient data dictionary
                    patient_data[key] = value
                
                # Add the patient record to the main data dictionary
                data[patient_id] = patient_data
                
    except FileNotFoundError:
        # Handle case where file doesn't exist
        print(f"There is no file with such a name {filename}, Enter the file name correctly!")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An error occurred: {e}")
    
    # Return the populated data dictionary
    return data

