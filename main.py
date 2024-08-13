import os
import Latin
import json
import prompt
from PIL import Image


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

def main():
    #######call to make all latin prompts
    #latin_runner()
    path_latin = r"E:\uni\BA\data\input\latin"
    path_instruction_latin = r"E:\uni\BA\data\input\latin\X00016469612.txt"
    path_instruction_picture = r"E:\uni\BA\data\input\img\X00016469612.jpg"
    path_entity = r"E:\uni\BA\data\input\entities\X00016469612.txt"
    path_feed = r"E:\uni\BA\data\input\feed"

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
    ##as Latin
    data_documents = []
    text_files = [os.path.join(path_feed, file) for file in os.listdir(path_feed) if file.endswith(".txt")]
    
    for file_path in text_files:
        with open(file_path, 'r') as file:
            content = file.read().strip()  # Read the content of the file and strip any extra whitespace
            data_documents.append(content)  # Add the content to the list

    #with open(path_feed, 'r') as file:
     #   data_document = file.read()
    ##as picture
    #data_document = Image.open(path_feed)
    
    for entry in data_documents:
        print(prompt.getPrompt(instruction_document, instruction_labels, entry, labels))


if __name__ == "__main__":
    main()