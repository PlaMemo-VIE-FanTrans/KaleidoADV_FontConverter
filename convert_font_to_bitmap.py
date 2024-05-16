import json
from PIL import Image, ImageDraw, ImageFont

def convert_font(ttf_path, font_size, output_image_prefix="font_bitmap",
    chars=" ! \" # $ % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~ À Á Â Ã È É Ê Ì Í Ò Ó Ô Õ Ù Ú Ý à á â ã è é ê ì í ò ó ô õ ù ú ý Ă ă Đ đ Ĩ ĩ Ũ ũ Ơ ơ Ư ư Ạ ạ Ả ả Ấ ấ Ầ ầ Ẩ ẩ Ẫ ẫ Ậ ậ Ắ ắ Ằ ằ Ẳ ẳ Ẵ ẵ Ặ ặ Ẹ ẹ Ẻ ẻ Ẽ ẽ Ế ế Ề ề Ể ể Ễ ễ Ệ ệ Ỉ ỉ Ị ị Ọ ọ Ỏ ỏ Ố ố Ồ ồ Ổ ổ Ỗ ỗ Ộ ộ Ớ ớ Ờ ờ Ở ở Ỡ ỡ Ợ ợ Ụ ụ Ủ ủ Ứ ứ Ừ ừ Ử ử Ữ ữ Ự ự Ỳ ỳ Ỵ ỵ Ỷ ỷ Ỹ ỹ ?",
    output_json="font_mapping.json"):

    font = ImageFont.truetype(ttf_path, font_size)
    char_images = {}
    current_image_id = 0
    current_image = None
    current_x = 0
    current_y = 0

    for char in chars:
        char_bbox = font.getbbox(char)
        char_width = char_bbox[2] - char_bbox[0]
        char_height = char_bbox[3] - char_bbox[1]
        char_image = Image.new("RGBA", (char_width, char_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(char_image)
        draw.text((-char_bbox[0], -char_bbox[1]), char, font=font, fill=(255, 255, 255, 255))

        char_image = char_image.crop(char_image.getbbox())

        char_width, char_height = char_image.size
        ascend, descend = font.getmetrics()

        if current_image is None or current_x + char_width > current_image.width:
            if current_image:
                current_image.save(f"{output_image_prefix}_{current_image_id}.png")
            current_image_id += 1
            current_image = Image.new("RGBA", (8192, 1024), (0, 0, 0, 0))
            # if you want to move the glyphs, change it here
            current_x = 10
            current_y = 10

        char_y = current_y + (ascend + char_bbox[1])
        current_image.paste(char_image, (current_x, char_y))

        char_images[char] = {
            "a": ascend - char_bbox[1] - font_size,
            "b": char_height,
            "d": descend,
            "h": char_height,
            "height": font_size,
            "id": current_image_id,
            "w": char_width,
            "width": char_width,
            "x": current_x,
            "y": char_y,
        }

        current_x += char_width

    if current_image:
        current_image.save(f"{output_image_prefix}_{current_image_id}.png")

    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(char_images, json_file, ensure_ascii=False, indent=2)

    return char_images

font_mapping = convert_font("NewCinemaAStd-D_0.otf", 24)
print(font_mapping) # if i fuck up something, use " > " in cmd to export the mapping instead
