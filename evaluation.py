from anls_star import anls_score
import os
import ast
import json
from sklearn.metrics import precision_score, recall_score, f1_score

input_folder = r"E:\uni\BA\data\input\feed"
entity_folder = r"E:\uni\BA\data\input\entitiesExtract"
values_list_prompts = []
values_list_entities = []



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

    return result_dict


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

            # Assuming the text content is exactly what you provided earlier
            values = extract_values_from_text(text_content)
            values_list_prompts.append(values)
      

def extract_from_entity():
      for filename in os.listdir(entity_folder):
            file_path = os.path.join(entity_folder, filename)
            if os.path.isfile(file_path):
                  with open(file_path, 'r') as file:
                        text_content = file.read()

            # Assuming the text content is exactly what you provided earlier
            values = extract_values_from_entity(text_content)
            values_list_entities.append(values)



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
      for entities, prompts in zip(values_list_entities, values_list_prompts):
            entities_keys = list(entities.keys())
            prompts_keys = list(prompts.keys())
            # Extracting values from the dictionaries
            entities_values = list(entities.values())
            prompts_values = list(prompts.values())
            
            # ANLS computations using only the values
            anls = anls_score(entities_values, prompts_values)
            anls_scores_all_labels.append(anls)

            key_0 = 'company'
            key_1 = 'date'
            key_2 = 'address'
            key_3 = 'total'
            
            #anls computations
            anls_score_0.append(anls_score(entities.get(key_0, ''), prompts.get(key_0, '')))
            anls_score_1.append(anls_score(entities.get(key_1, ''), prompts.get(key_1, '')))
            anls_score_2.append(anls_score(entities.get(key_2, ''), prompts.get(key_2, '')))
            anls_score_3.append(anls_score(entities.get(key_3, ''), prompts.get(key_3, '')))

            """if anls < 0.75:
                  print(entities)
                  print(prompts)
                  print(anls)"""
            anls_scores_all_labels.append(anls)
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
            precision.append(precision_score(gt_labels, ev_labels))
            recall.append(recall_score(gt_labels, ev_labels))
            f1.append(f1_score(gt_labels, ev_labels))
            
      print(" anls* final average score over all labels:")
      print(sum(anls_scores_all_labels)/len(anls_scores_all_labels))
      print(" anls* final average score for company:")
      print(sum(anls_score_0)/len(anls_score_0))
      print(" anls* final average score for label date:")
      print(sum(anls_score_1)/len(anls_score_1))
      print(" anls* final average score for label address:")
      print(sum(anls_score_2)/len(anls_score_2))
      print(" anls* final average score for label total:")
      print(sum(anls_score_3)/len(anls_score_3))
      print("precision:")
      print(sum(precision)/len(precision))
      print("recall:")
      print(sum(recall)/len(recall))
      print("f1:")
      print(sum(f1)/len(f1))

            
      
