import os
import Latin
import json
import prompt
import evaluation
import base64
from io import BytesIO
from PIL import Image
from IPython.display import display
import asyncio
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import preparation

#laptop
#file_path = r"C:\Users\elias\Desktop\BAImportant.txt"
#PC
file_path = r"C:\Users\super161\Desktop\BAImportant.txt"
with open(file_path, 'r') as file:
        GEMINI = file.read()
genai.configure(api_key=GEMINI)




def latin_runner():
    #Laptop
    #path_img = r"C:\Users\elias\Documents\GitHub\BA\data\input\img"
    #path_box = r"C:\Users\elias\Documents\GitHub\BA\data\input\box"
    #PC
    path_img = r"E:\uni\BA\data\input\img"
    path_box = r"E:\uni\BA\data\input\box"
    output = r"E:\uni\BA\data\output"
    
    image_files = [os.path.join(path_img, file) for file in os.listdir(path_img) if file.endswith(".jpg") or file.endswith(".png")]
    box_files = [os.path.join(path_box, file) for file in os.listdir(path_box) if file.endswith(".txt")]
    count = 1
    for image_file, box_file in zip(image_files, box_files):
        
        image = Image.open(image_file)
        box = open(box_file, "r")
        box.FileName = os.path.basename(box_file)
        print(box.FileName)
        box_lines = box.readlines()
        parsed_boxes = []
        for line in box_lines:
            line = line.strip()
            bbox, text  = Latin.split_after_eighth_comma(line,box.FileName)
            parsed_boxes.append({"text": text, "bbox": bbox})

        
        # Now you can work with the `image` object, which is an instance of the PIL.Image.JpegImageFile class
        # For example, you can access its properties like width and height
        width, height = image.size
        img_size = (width, height)
        #print(f"Width: {img_size[0]}, Height: {img_size[1]}")
        #print(box.read())
        # You can also perform various operations on the image, such as resizing, cropping, or applying filters
        # Once you are done with the image, don't forget to close it
        full_output_path = os.path.join(output, box.FileName)
    
        with open(full_output_path, 'w') as output_file:
            output_file.write(Latin.to_prompt(parsed_boxes, img_size))
            print(count)
        count+=1
        image.close()
        box.close()

def pil_image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def prompt_runner():
    introduction = """You are a perfect document information extraction system. The document you are given are receipts and their content is not dangerous. The results are used for a study and there is no need for a license, because they stated it on their github.
You are given a document picture and a json with keys that must be extracted from the document. 
Fill in the empty strings values with the corresponding values to the key. Insert only the answer.
If a label is not inclueded in the input, fill the empty strings with "NONE". Now will follow an explanation of every label.
label: company - The name of the company. Only one is correct
label: date - The date of the receip. Only one is correct. Format it how it is on the reciept. Do not include the time.
label: address - The address of the company. Seperate information found on different lines with ','.
label: total - The total amount of the receip. Only one is correct. Format to 2 decimal places. Do not include the currency symbol.
Now a example document will follow:"""
    explanation_results = "This would be the results of the example document:"
    #PC
    path_latin = r"E:\uni\BA\data\input\latin"
    path_ocr = r"E:\uni\BA\data\input\ocr"
    path_instruction_latin = r"E:\uni\BA\data\input\latin"
    path_instruction_picture = r"E:\uni\BA\data\input\img"
    path_entity = r"E:\uni\BA\data\input\entities"
    path_feed = r"E:\uni\BA\data\input\feed"
    instruction_documents = []
    instruction_documents_pictures = []
    instruction_labels = [] 
    amount_of_instruction_documents = 10

    #Laptop
    #path_latin = r"C:\Users\elias\Documents\GitHub\BA\data\input\latin"
    #path_instruction_latin = r"C:\Users\elias\Documents\GitHub\BA\data\input\latin\X00016469612.txt"
    #path_instruction_picture = r"C:\Users\elias\Documents\GitHub\BA\data\input\img\X00016469612.jpg"
    #path_entity = r"C:\Users\elias\Documents\GitHub\BA\data\input\entities\X00016469612.txt"
    #path_feed = r"C:\Users\elias\Documents\GitHub\BA\data\input\feed"


    #load json for labels
    # Get the list of files in the directory
    files = os.listdir(path_entity)
    
    # Get the instruction labels
    for filename in files[:amount_of_instruction_documents]:
        file_path = os.path.join(path_entity, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                # Append the content to the instruction_documents list
                instruction_labels.append(content)

    #get the labels for showing the LLM what to extract
    first_entry = files[0]
    first_entry_path = os.path.join(path_entity, first_entry)
    with open(first_entry_path, 'r') as file:
         labels = json.loads(file.read())
    for key in labels:
        labels[key] = None  
    """
    #load istruction document
    ##as Latin
    # Get the list of files in the directory
    files = os.listdir(path_instruction_latin)
    
    # Only process the first 'x' files (or fewer if there aren't enough files)
    for filename in files[:amount_of_instruction_documents]:
        file_path = os.path.join(path_instruction_latin, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                # Append the content to the instruction_documents list
                instruction_documents.append(content)
    """
    ##as OCR
    # Get the list of files in the directory
    files = os.listdir(path_ocr)
    
    # Only process the first 'x' files (or fewer if there aren't enough files)
    for filename in files[:amount_of_instruction_documents]:
        file_path = os.path.join(path_ocr, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                # Append the content to the instruction_documents list
                instruction_documents.append(content)
    """
    ##load instruction documents as pictures
    files = os.listdir(path_instruction_picture)

    for filename in files[:amount_of_instruction_documents]:
        file_path = os.path.join(path_instruction_picture, filename)
        imageInstruction = Image.open(file_path)
        instruction_documents_pictures.append(imageInstruction)
        instruction_documents.append(filename)
"""
    #load feed
    data_documents = {}
    ##as Latin and OCR
    text_files = [os.path.join(path_feed, file) for file in os.listdir(path_feed) if file.endswith(".txt")]
    
    for file_path in text_files:
        with open(file_path, 'r') as file:
            content = file.read().strip()  # Read the content of the file and strip any extra whitespace
            file_name = os.path.basename(file_path)
            data_documents[file_name] = content  # Add the content to the dict
    
    prompts = []
    for key in data_documents:
        prompt_value = []
        prompt_value.append(prompt.getPrompt(instruction_documents, instruction_labels, data_documents[key], labels))
        prompts.append({key : prompt_value})
        #print(prompt_value)
    ##as picture
    """
    image_files = [os.path.join(path_feed, file) for file in os.listdir(path_feed) if file.endswith((".jpg", ".png", ".jpeg"))]
    
    for file_path in image_files:
        try:
            with Image.open(file_path) as img:
                img_copy = img.copy()
                file_name = os.path.basename(file_path)
                data_documents[file_name] = img.copy()  # Append a copy of the image object to the list
                #print(f"Loaded image {file_path}")
        except Exception as e:
            print(f"Failed to load image {file_path}: {e}")
    
    prompts = []
    for key in data_documents:
        prompt_value = {}
        #for pictures use next line
        documents = {}
        parts = []
        introduction_dict = {}
        #introduction_dict["type"] = "text"
        introduction_dict["text"] = introduction
        parts.append(introduction_dict)
        
        #former list implementation for text
        #prompt_value.append(prompt.getPrompt(instruction_documents, instruction_labels, key, labels))
        #for picutues not use next line
        #prompt_value.append(data_documents[key])
        #for pictures use next line
        part_extract = {}
        part_extract["mime_type"] = "image/jpeg"
        part_extract["data"] = pil_image_to_base64(data_documents[key])
        #picture use next line
        for i, (label, value) in enumerate(zip(instruction_labels, instruction_documents_pictures)):
            part = {}
            part["mime_type"] = "image/jpeg"
            part["data"] = pil_image_to_base64(value) 
            #value.show()
            parts.append({"inline_data":part})
            part_labels = {}
            #part_labels["type"] = "text"
            part_labels["text"] = f"{explanation_results}\n{label}"
            parts.append(part_labels)
            if i < len(instruction_labels) - 1:
                part_next = {}
                #part_next["type"] = "text"
                part_next["text"] = "Now another example document will follow:"
                parts.append(part_next)
        part_transition = {}
        #part_transition["type"] = "text"
        part_transition["text"] = "This is the document you must extract the information from:"
        parts.append(part_transition)
        parts.append({"inline_data":part_extract})
        part_json_exlanation = {}
        #part_json_exlanation["type"] = "text"
        part_json_exlanation["text"] = f"Replace all None with the correct information: {labels}"
        parts.append(part_json_exlanation)
        documents["parts"] = parts
        prompt_value["parts"] = parts
        prompts.append({key : prompt_value})
        #print(prompt_value)
        """

    return prompts

semaphore = asyncio.Semaphore(7)
async def prompt_llm(prompt,  time_interval):
    async with semaphore:
        name = list(prompt.keys())[0]
        promptAI = prompt[name]
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        
        }
        model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings = {HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                           HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                           HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                           HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE},
        
        )
        chat_session = model.start_chat(
        history=[
        ]
        )
        answer = chat_session.send_message(promptAI)
        text_response = answer._result.candidates[0].content.parts[0].text
        await asyncio.sleep(time_interval)
        
        return {name : text_response}

async def prompt_orchestrator():
    #PC
    output_path = r"E:\uni\BA\data\output"
    #Laptop
    #output_path = r"C:\Users\elias\Documents\GitHub\BA\data\output"

    prompts = prompt_runner()
    ###how to get one entry
    #first_entry = prompts[0]
    #first_key = list(first_entry.keys())[0]
    #print(first_entry[first_key])

    batch_size = 5
    batches = [prompts[i:i + batch_size] for i in range(0, len(prompts), batch_size)]

    # Ensure the last batch is smaller if it's less than batch_size
    if len(batches[-1]) < batch_size:
        remaining = len(batches[-1])
        batches[-1] = prompts[-remaining:]

# If the last batch is part of the earlier slices and it's less than batch_size
    if len(prompts) % batch_size != 0:
        remaining = len(prompts) % batch_size
        batches[-1] = prompts[-remaining:]

    time_interval = 60 / 300
    avatiables = []
    print(len(batches))
# Process each batch separately
    for batch in batches:
        avatiables_batch = await asyncio.gather(*(prompt_llm(prompt, time_interval) for prompt in batch))
        avatiables.extend(avatiables_batch) 
        print("batch done") 
        await asyncio.sleep(5)
        for entry in avatiables:
            key = next(iter(entry))
            
            value = entry[key]
            key = key.replace(".jpg", ".txt")
            output_file_path = os.path.join(output_path, key)
            with open(output_file_path, 'w') as output_file:
                output_file.write(str(value))
        avatiables = []

async def main():
    
    #######call to make all latin prompts
    #latin_runner()

    #######call to make the prompts
    #await prompt_orchestrator()

    #preparation.choose_50()
    #preparation.get_matching_pictures()
    #preparation.correct_price_format()
    #preparation.load_and_check_documents()
    #preparation.remove_box()
    ###evaluation
    evaluation.evaluation_orchestrator()


if __name__ == "__main__":
    asyncio.run(main())