from markup import markup
from Color_Thresholding import ImgCapture

im = ImgCapture()
im.file_IO()
im.run()
mk = markup()
mk.file_IO()
mk.run()
mk.save_markup()
