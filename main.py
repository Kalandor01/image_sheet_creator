from sys import argv
from PIL import Image


a4_aspect_ratio:float = 297 / 210


def make_img_sheet(image_name="img.png", target_image_name="target_image.png" , tile_amount:tuple[int, int]=None, aspect_ratio:float=a4_aspect_ratio):
    """
    Tiles an image x * y times.
    """
    
    if aspect_ratio <= 0:
        input(f"Aspect ratio is not large enough: ({aspect_ratio[0]} <= 0")
        return
    
    if tile_amount[0] < 1 or tile_amount[1] < 1:
        input(f"Tile amount is too small: ({tile_amount[0]}, {tile_amount[1]}) < (1, 1)")
        return
    
    try:
        image = Image.open(image_name)
    except FileNotFoundError:
        input(f"\"{image_name}\" not found!")
        return
    
    # calculate sizes    
    img_size = image.size
    
    final_width = img_size[0] * tile_amount[0]
    final_height = img_size[1] * tile_amount[1]
    
    raw_aspect_ratio = final_height / final_width
    
    if raw_aspect_ratio != aspect_ratio:
        corrected_size:tuple[int, int] = (1, 1)
        if raw_aspect_ratio > aspect_ratio:
            corrected_size = (img_size[0], round(img_size[1] / (raw_aspect_ratio / aspect_ratio)))
        else:    
            corrected_size = (round(img_size[0] / (aspect_ratio / raw_aspect_ratio)), img_size[1])
        image = image.resize(corrected_size)
        
        img_size = image.size
        final_width = img_size[0] * tile_amount[0]
        final_height = img_size[1] * tile_amount[1]
    
    # make img
    tiled_image = Image.new('RGBA', (final_width, final_height))
    for y in range(tile_amount[1]):
        for x in range(tile_amount[0]):
            tiled_image.paste(im=image, box=(x * img_size[0], y * img_size[1]))
    
    tiled_image.save(target_image_name)



if __name__ == "__main__":
    image_name = "img.png"
    target_image_name = "target_img.png"
    tile_amount:tuple[int, int] = (3, 10)
    aspect_ratio:float = a4_aspect_ratio
    
    args = argv
    if len(args) < 2:
        input("Open an image with this app.")
        exit()
    
    image_name = args[1]
    tile_amount_x = int(input("How many images in a row: "))
    tile_amount_y = int(input("How many images in a column: "))
    tile_amount = (tile_amount_x, tile_amount_y)
    try:
        aspect_ratio = float(input("Aspect ratio (A4 by default): "))
    except ValueError:
        pass
    is_landscape = input("Flip aspect ratio (Y/N): ").upper() == "Y"
    
    if is_landscape:
        aspect_ratio = 1 / aspect_ratio
    
    make_img_sheet(image_name, target_image_name, tile_amount, aspect_ratio)
    