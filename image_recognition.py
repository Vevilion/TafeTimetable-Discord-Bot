from PIL import Image, ImageChops, ImageOps

def compare_images():
    img1, img2 = Image.open('timetable.png') , Image.open('compare_timetable.png')
    grey1 = ImageOps.grayscale(img1) 
    grey2 = ImageOps.grayscale(img2)
    diff = ImageChops.difference(grey1, grey2)
    
    return str(diff.getbbox())

    

