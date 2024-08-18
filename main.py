import os
import Latin
import json
import prompt

from PIL import Image
from IPython.display import display
import asyncio
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import preparation


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

def prompt_runner():
    
    #PC
    path_latin = r"E:\uni\BA\data\input\latin"
    path_instruction_latin = r"E:\uni\BA\data\input\latin\X51005268408.txt"
    path_instruction_picture = r"E:\uni\BA\data\input\img\X00016469612.jpg"
    path_entity = r"E:\uni\BA\data\input\entities\X51005268408.txt"
    path_feed = r"E:\uni\BA\data\input\feed"

    #Laptop
    #path_latin = r"C:\Users\elias\Documents\GitHub\BA\data\input\latin"
    #path_instruction_latin = r"C:\Users\elias\Documents\GitHub\BA\data\input\latin\X00016469612.txt"
    #path_instruction_picture = r"C:\Users\elias\Documents\GitHub\BA\data\input\img\X00016469612.jpg"
    #path_entity = r"C:\Users\elias\Documents\GitHub\BA\data\input\entities\X00016469612.txt"
    #path_feed = r"C:\Users\elias\Documents\GitHub\BA\data\input\feed"


    #load json for labels
    with open(path_entity, 'r') as file:
        data = file.read()  # Read the content of the file
        labels = json.loads(data)  # Parse the content as JSON
        instruction_labels = json.loads(data) 
    for key in labels:
        labels[key] = None  # or use None if you prefer

    #load istruction document
    ##as Latin
    with open(path_instruction_latin, 'r') as file:
        instruction_document = file.read()
    ##as picture
    # image = Image.open(path_instruction_picture)

    #load feed
    data_documents = {}
    ##as Latin
    text_files = [os.path.join(path_feed, file) for file in os.listdir(path_feed) if file.endswith(".txt")]
    
    for file_path in text_files:
        with open(file_path, 'r') as file:
            content = file.read().strip()  # Read the content of the file and strip any extra whitespace
            file_name = os.path.basename(file_path)
            data_documents[file_name] = content  # Add the content to the dict
    
    #with open(path_feed, 'r') as file:
     #   data_document = file.read()
    ##as picture
    """
    image_files = [os.path.join(path_feed, file) for file in os.listdir(path_feed) if file.endswith((".jpg", ".png", ".jpeg"))]
    
    for file_path in image_files:
        try:
            with Image.open(file_path) as img:
                img_copy = img.copy()
                file_name = os.path.basename(file_path)
                data_documents[file_name] = img.copy()  # Append a copy of the image object to the list
                
        except Exception as e:
            print(f"Failed to load image {file_path}: {e}")
    """
    prompts = []
    for key in data_documents:
        prompt_value = prompt.getPrompt(instruction_document, instruction_labels, data_documents[key], labels)
        prompts.append({key : prompt_value})
        #print(prompt_value)
    return prompts


semaphore = asyncio.Semaphore(40)

async def prompt_llm(prompt,  time_interval):
    async with semaphore:
        name = list(prompt.keys())[0]
        promptAI = prompt[name]   #this is the prompt
        print(name)
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
        safety_settings = {HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE}
        )
        chat_session = model.start_chat(
        history=[
        ]
        )
        answer = chat_session.send_message(promptAI)
        await asyncio.sleep(time_interval)
        return {name : answer}

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

    batch_size = 25
    batches = [prompts[i:i + batch_size] for i in range(0, len(prompts) - 23, batch_size)]
    batches.append(prompts[-23:])  # Add the last batch of 23 prompts

    time_interval = 60 / 100
    avatiables = []
    print(len(batches))
# Process each batch separately
    for batch in batches:
        avatiables_batch = batch #await asyncio.gather(*(prompt_llm(prompt, time_interval) for prompt in batch))
        avatiables.extend(avatiables_batch) 
        print("batch done") 
        await asyncio.sleep(10)
        for entry in avatiables:
            key = next(iter(entry))
            value = entry[key]
            output_file_path = os.path.join(output_path, key)
            with open(output_file_path, 'w') as output_file:
                output_file.write(str(value))
        avatiables = []

async def main():
    
    #######call to make all latin prompts
    #latin_runner()
    #######call to make the prompts
    await prompt_orchestrator()

    #preparation.choose_50()
    #preparation.get_matching_pictures()
    


if __name__ == "__main__":
    asyncio.run(main())