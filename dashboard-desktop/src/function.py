# FUNCTION FILE 
from PIL import Image

def resize_image(path_image, w, h):
  img = Image.open(str(path_image))
  new_size = (w, h)
  resized_img = img.resize(new_size)
  resized_img.save("E:\\2024\\My Projects\\continues\\teachora-classes\\dashboard-desktop\\resources\\images\\backgroundlogin.jpg")

resize_image("E:\\2024\\My Projects\\continues\\teachora-classes\\dashboard-desktop\\resources\\images\\backgroundlogin.jpg", 922, 713)