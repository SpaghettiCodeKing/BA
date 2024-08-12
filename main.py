import os
import Latin
from PIL import Image

def main():
    path_img = r"C:\Users\elias\Documents\GitHub\BA\data\input\img"
    path_box = r"C:\Users\elias\Documents\GitHub\BA\data\input\box"
    image_files = [os.path.join(path_img, file) for file in os.listdir(path_img) if file.endswith(".jpg") or file.endswith(".png")]
    box_files = [os.path.join(path_box, file) for file in os.listdir(path_box) if file.endswith(".txt")]
    for image_file, box_file in zip(image_files, box_files):
        image = Image.open(image_file)
        box = open(box_file, "r")
        # Now you can work with the `image` object, which is an instance of the PIL.Image.JpegImageFile class
        # For example, you can access its properties like width and height
        width, height = image.size
        img_size = (width, height)
        #print(f"Width: {img_size[0]}, Height: {img_size[1]}")
        print(box.read())
        # You can also perform various operations on the image, such as resizing, cropping, or applying filters
        # Once you are done with the image, don't forget to close it
        #print(Latin.to_prompt(box, img_size))
        
        image.close()
        box.close()


if __name__ == "__main__":
    main()