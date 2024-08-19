import os
import shutil
import random
import json
import re
import ast

def choose_50():

  to_pick_from = r"E:\uni\BA\data\input\topickfrom"
  to_write_to = r"E:\uni\BA\data\input\latin"

  all_files = [f for f in os.listdir(to_pick_from) if os.path.isfile(os.path.join(to_pick_from, f))]
  selected_files = random.sample(all_files, 50)

  for file_name in selected_files:
    source_file_path = os.path.join(to_pick_from, file_name)
    destination_file_path = os.path.join(to_write_to, file_name)
    shutil.move(source_file_path, destination_file_path)


def get_matching_pictures():
  to_pick_from = r"E:\uni\BA\data\input\feed"
  txt = r"E:\uni\BA\data\input\latinExtract"
  output = r"E:\uni\BA\data\input\entitiesExtract"
  output_prompt_entities = r"E:\uni\BA\data\input\entitiesExtract"
      
  txt_files = {os.path.splitext(f)[0] for f in os.listdir(txt) if os.path.isfile(os.path.join(txt, f)) and f.endswith('.txt')}
      
  for png_file in os.listdir(to_pick_from):
    if png_file.endswith('.txt'):
        png_file_base = os.path.splitext(png_file)[0]
        if png_file_base in txt_files:
            # Copy the matching png file to the destination folder
            source_file_path = os.path.join(to_pick_from, png_file)
            destination_file_path = os.path.join(output, png_file)
            shutil.move(source_file_path, destination_file_path)

def clean_price(price):
  # Remove any non-numeric characters except the decimal point
  cleaned_price = ''.join(char for char in price if char.isdigit() or char == '.')
    
  # Ensure it has two decimal places
  if '.' in cleaned_price:
    integer_part, decimal_part = cleaned_price.split('.')
    decimal_part = decimal_part[:2].ljust(2, '0')  # Ensure two decimal places
    corrected_price = f"{integer_part}.{decimal_part}"
  else:
    corrected_price = f"{cleaned_price}.00"  # No decimal point, add ".00"
    
  return corrected_price

def correct_price_format():
  folder_path = r"E:\uni\BA\data\input\entitiesExtract"
  # Iterate over all files in the specified folder
  for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    with open(file_path, 'r') as file:
      data = json.load(file)
            
    # Check if the 'total' field is formatted correctly
    if 'total' in data:
      original_price = data['total']
      corrected_price = clean_price(original_price)

      if original_price != corrected_price:
        print(f"Correcting price in file {filename}: {original_price} -> {corrected_price}")
        data['total'] = corrected_price

                    # Write the corrected data back to the file
    with open(file_path, 'w') as file:
      json.dump(data, file, indent=4)



def load_and_check_documents():
    directory_path = r"E:\uni\BA\data\input\entitiesExtract"
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Ensure we're working with a file, not a subdirectory
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                text_content = file.read()
            
            # Use regex to extract the dictionary-like content
            match = re.search(r'\{.*\}', text_content, re.DOTALL)
            if match:
                dict_string = match.group(0)
                try:
                    # Safely evaluate the string to a dictionary
                    data_dict = ast.literal_eval(dict_string)
                    
                    # Check if the dictionary has exactly 4 keys
                    if len(data_dict) != 4:
                        print(f"File '{filename}' does not have 4 keys. It has {len(data_dict)} keys.")
                except Exception as e:
                    print(f"Error processing file '{filename}': {e}")
            else:
                print(f"File '{filename}' does not contain a valid dictionary.")

