from PIL import Image
import os, math

def process_image(path_values: dict, type: str):
    # open image to be processed
    new_img = Image.open(path_values['osFilePath'])
    
    # check if image is square
    width = new_img.width
    height = new_img.height

    if width > height or height > width:
        print("Image is not square. Cropping...")
        # crop image to have a square aspect ratio
        left = 0
        upper = 0
        right = width
        lower = height
        if width > height:
            right =  right - (right - lower)
        elif height > width:
            lower = lower - (lower - right)
        # save crop dimensions in tuple
        dimension_tuple = (left, upper, right, lower)
        new_img = new_img.crop(dimension_tuple)
        # refresh image dimensions
        width = new_img.width
        height = new_img.height
        print(f'Image has been cropped to a size of {width}px by {height}px.')
    
    # check if image is too large (>1000px)
    if width > 1000:
        print("Image exceeds 1000px square. Resizing...")
        desired_img_size = 800;
        scale_factor = width / desired_img_size
        # save scale factors for width and height in tuple
        scale_tuple = (math.floor(width / scale_factor), math.floor(height / scale_factor))
        new_img = new_img.resize(scale_tuple)
        # refresh image dimensions
        width = new_img.width
        height = new_img.height
        print(f'Image has been resized to {width}px by {height}px.')
    
    # determine image type to ensure proper filename
    if type == "item":
        # save processed item image as new file (.jpg)
        if os.name == 'nt':
            new_img.save(path_values['dirPath'] + "\\" + path_values['filename'])
            print("IMG SAVED TO: " + path_values['dirPath'] + "\\" + path_values['filename'])
        elif os.name == 'posix':
            new_img.save(path_values['dirPath'] + "/" + path_values['filename'])
            print("IMG SAVED TO: "+ path_values['dirPath'] + "/" + path_values['filename'])