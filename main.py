import os
import Latin
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


if __name__ == "__main__":
    main()