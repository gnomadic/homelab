from inky import InkyWHAT
from PIL import Image

inky = InkyWHAT("yellow")  # Or "red" / "black"
inky.set_border(inky.WHITE)

img = Image.new("P", inky.resolution, color=inky.WHITE)
inky.set_image(img)
inky.show()