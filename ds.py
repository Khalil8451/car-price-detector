import csv
import json

# Define an empty dictionary to store marques and their modeles
marques = {}

# Specify the path to your CSV file
data_file = "clean_final.csv"  # Replace with your actual file path

# Open the CSV file for reading
with open(data_file, 'r', encoding='utf-8') as csvfile:
  # Create a CSV reader object
  reader = csv.reader(csvfile)
  
  # Skip the header row (assuming the first row contains column names)
  next(reader)  

  # Iterate over the rows of data in the CSV file
  for row in reader:
    marque = row[0]
    modele = row[1]
    
    # If the marque doesn't exist in the dictionary, add it with an empty set (for efficient duplicate removal)
    if marque not in marques:
      marques[marque] = set()
    
    # Add the modele to the set (duplicates will be automatically removed)
    marques[marque].add(modele)

# Convert the dictionary to a list for JSON formatting, using set to list conversion for "modele"
data = [{'marque': marque, 'modele': list(modeles)} for marque, modeles in marques.items()]

# Specify the name for the output JSON file
json_file = "cars.json"  # Replace with your desired filename

# Open the JSON file for writing
with open(json_file, 'w', encoding='utf-8') as jsonfile:
  # Dump the list of marque dictionaries to the JSON file
  json.dump(data, jsonfile, indent=4)  # Add indent for readability

print(f"Data successfully saved to {json_file}")
