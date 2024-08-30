from anls_star import anls_score
import os
import ast
import json
import re
from sklearn.metrics import precision_score, recall_score, f1_score

input_folder = r"E:\uni\BA\data\input\feed"
entity_folder = r"E:\uni\BA\data\input\entitiesExtract"
values_list_prompts = []
values_list_entities = []
name_files = []
banned_files = []

"""
def extract_values_from_text(text_content):
    result_dict = {}
    
    lines = text_content.splitlines()
    for line in lines:
        if "text" in line:
            text = line.strip()
            text = text.strip("{}").strip()
            items = text.split("', '")
            
            # Special treatment for the first item
            brace_position = items[0].find("{")
            if brace_position != -1:
                items[0] = items[0][brace_position+2:]
            try:
                brace_position = items[3].find("}")
                if brace_position != -1:
                    items[3] = items[3][:brace_position-1]
            except:
                brace_position = items[2].find("}")
                if brace_position != -1:
                    items[2] = items[2][:brace_position-1]

            ## Postprocessing
            for item in items:
                item = f"'{item}'"
                
                # Split the key and value
                key, value = item.split(": ", 1)

                # Remove quotes and extra spaces from keys and values
                key = key.strip("'\"")
                value = value.strip("'\"")

                # Add to dictionary
                result_dict[key] = value

    return result_dict"""


def extract_values_from_entity(data):   
       # Convert the string to a dictionary
    dict_obj = json.loads(data)
    return dict_obj

def extract_from_prompt():
      
      for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
        

            if os.path.isfile(file_path):
                  with open(file_path, 'r') as file:
                        text_content = file.read()

#post processing
            # Attempt to extract the dictionary-like content using regex
            match = re.search(r'\{.*\}', text_content, re.DOTALL)
            if match:
                text_content = match.group(0)
                try:
                    values = ast.literal_eval(text_content)
                except Exception as e:
                    print(f"Error in file {filename}: {e}")
                    banned_files.append(filename)   
                    values = None
            
            if values is not None:
                values["company"] = values.get("company", "").replace("\n", " ")
                values["address"] = values.get("address", "").replace(" , ", ", ")
                #delete telephone number
                text = values["address"]
                cleaned_text = re.sub(r'TEL NO\.:.*', '', text)
                values["address"] = cleaned_text
                #delete everything in brackets
                """text = values["address"]
                cleaned_text = re.sub(r'\(.*\)$', '', text)
                values["address"] = cleaned_text"""
                values_list_prompts.append(values)
      

def extract_from_entity():
    print(banned_files)
    for filename in os.listdir(entity_folder):
        if filename not in banned_files:
            file_path = os.path.join(entity_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    text_content = file.read()
                
            values = extract_values_from_entity(text_content)
            #switch from SANYU STATIONERY SHOP to SANYU SUPPLY SDN BHD because not in instruction data and it is the correct owned by company...
            if values["company"] =="SANYU STATIONERY SHOP":
                values["company"] = "SANYU SUPPLY SDN BHD"
            values_list_entities.append(values)
            name_files.append(filename)
        else:
            print(f"Skipping file {filename} due to previous errors")

            



def compare_folders():
    # Get a list of files in each folder
    files_in_a = set(os.listdir(folder_a))
    files_in_b = set(os.listdir(folder_b))

    # Find files in folder A that are not in folder B
    missing_files = files_in_a - files_in_b

    if not missing_files:
        print("Successful: All file names in Folder A appear in Folder B.")
    else:
        print("The following files are in Folder A but not in Folder B:")
        for file in missing_files:
            print(file)


def clean_strings(strings):
    cleaned_strings = []
    for s in strings:
        # Replace ",," with ","
        if s is not None:
            s = s.replace(",,", ",")
            # Replace multiple white spaces with a single white space
            s = re.sub(r'\s+', ' ', s)
            # Append the cleaned string to the list
            cleaned_strings.append(s.strip())  # .strip() removes leading/trailing whitespace if necessary
    return cleaned_strings
      

def evaluation_orchestrator():
    anls_scores_all_labels = []
    anls_score_0 = []
    anls_score_1 = []
    anls_score_2 = []
    anls_score_3 = []
      
    precision = []
    recall = []
    f1 = []
      
    extract_from_prompt()
    extract_from_entity()
    for entities, prompts,name in zip(values_list_entities, values_list_prompts,name_files):
        
        entities_keys = list(entities.keys())
        prompts_keys = list(prompts.keys())
        # Extracting values from the dictionaries
        entities_values = list(entities.values())
        prompts_values = list(prompts.values())

##post processing
        prompts_values = clean_strings(prompts_values)
            
            
        # ANLS computations using only the values
        anls = anls_score(entities_values, prompts_values)
        anls_scores_all_labels.append(anls)

        key_0 = 'company'
        key_1 = 'date'
        key_2 = 'address'
        key_3 = 'total'

        #test if all keys are in the dictionary
        allowed_keys = ['company', 'date', 'address', 'total']
        if not set(prompts.keys()).issubset(allowed_keys):
            print(dictionary)
            #anls computations
        anls_score_0.append(anls_score(entities.get(key_0, ''), prompts.get(key_0, '')))
        anls_score_1.append(anls_score(entities.get(key_1, ''), prompts.get(key_1, '')))
        anls_score_2.append(anls_score(entities.get(key_2, ''), prompts.get(key_2, '')))
        anls_score_3.append(anls_score(entities.get(key_3, ''), prompts.get(key_3, '')))

        if "FAMILYMART" in entities["company"]:
            print(name)
            print(entities)
            print(prompts)  
            print(anls) 
        """if anls < 0.76:
            print(name)
            print(entities)
            print(prompts)
            print(anls)"""
        #precision, recall, f1
        # Convert the dictionaries to sets of keys
        gt_keys = set(entities.keys())            
        ev_keys = set(prompts.keys())        
        # Union of all keys to get a comprehensive list
        all_keys = list(gt_keys.union(ev_keys))

        # Create binary labels for the presence of keys
        gt_labels = [entities.get(key) == prompts.get(key) for key in all_keys]
        ev_labels = [key in ev_keys for key in all_keys]

        # Calculate precision, recall, and F1 score
        precision.append(precision_score(gt_labels, ev_labels, zero_division=0))
        recall.append(recall_score(gt_labels, ev_labels, zero_division=0))
        f1.append(f1_score(gt_labels, ev_labels, zero_division=0))
    print(len(values_list_prompts))
    print(" anls* final average score over all labels:")
    print(round(sum(anls_scores_all_labels)/len(anls_scores_all_labels),5))
    print(" anls* final average score for company:")
    print(round(sum(anls_score_0)/len(anls_score_0),5))
    print(" anls* final average score for label date:")
    print(round(sum(anls_score_1)/len(anls_score_1),5))
    print(" anls* final average score for label address:")
    print(round(sum(anls_score_2)/len(anls_score_2),5))
    print(" anls* final average score for label total:")
    print(round(sum(anls_score_3)/len(anls_score_3),5))
    print("precision:")
    print(round(sum(precision)/len(precision),5))
    print("recall:")
    print(round(sum(recall)/len(recall),5))
    print("f1:")
    print(round(sum(f1)/len(f1),5))

            
      
