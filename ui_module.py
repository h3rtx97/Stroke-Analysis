#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import necessary modules
from dataset_module import load_dataset
import query_module as qm
import csv

# Load the dataset
data = load_dataset('data.csv')

def main_menu():
    print("\nStroke Data Analysis based on patients' information")
    print("Please choose an option below:")
    print("1. Average, modal and median age of smokers with hypertension and stroke")
    print("2. Average, modal and median age of heart disease related to stroke")
    print("3. Gender-based hypertension statistics")
    print("4. Smoking effect on stroke occurrence")
    print("5. Urban and rural stroke distribution")
    print("6. Dietary habits and stroke analysis")
    print("7. Hypertension caused stroke")
    print("8. Hypertension with and without stroke")
    print("9. Heart Disease with Stroke")
    print("10. Sleep hours and stroke correlation")
    print("11. Descriptive statistics for a selected feature")
    print("0. Exit")

def run_program():
    while True:
        main_menu()
        choice = input("\nEnter 0 to 11: ").strip()
        
        if choice == '1':
            result = qm.smoker_with_hypertension(data)
        elif choice == '2':
            result = qm.heart_disease(data)
        elif choice == '3':
            result = qm.gender_hypertension_stroke(data)
        elif choice == '4':
            result = qm.smoke_stroke(data)
        elif choice == '5':
            result = qm.urban_rural_stroke(data)
        elif choice == '6':
            result = qm.diet_stroke(data)
        elif choice == '7':
            result = qm.hypertension_with_stroke(data)
        elif choice == '8':
            result = qm.stroke_hypertension(data)
        elif choice == '9':
            result = qm.everyone_heart_disease_stroke(data)
        elif choice == '10':
            result = qm.avg_sleep_stroke(data)
        elif choice == '11':
            feature = input("Enter the feature name (e.g., Age, Sleep Hours): ")
            result = qm.descriptive_statistics(data, feature)    
        elif choice == '0':
            print("Exiting the program. See you next time!")
            break
        else:
            print("Invalid number. Please type numbers only and try again!\n")
            continue

        # Display result with output limitation
        print("\nResults")
        max_display = 10  # Only display the first 10 items
        # Checks if result is a dictionary.
        if isinstance(result, dict):
            for a, b in result.items(): # a is key and b is value
                print(f"{a}: {b}")
        # Checks if result is a list.
        elif isinstance(result, list):
            for i, item in enumerate(result[:max_display]):
                print(f"{i+1}. {item}")
            if len(result) > max_display:
                print(f"...and {len(result) - max_display} more results not shown because of large data!.")
        else:
            print(result)

# Start the program
if __name__ == "__main__":
    run_program()


# In[ ]:




