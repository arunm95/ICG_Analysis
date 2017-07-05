from markup import markup
from Color_Thresholding import ImgCapture

while (raw_input("continue? (y/n)") == 'y'):
    im = ImgCapture()
    im.file_IO()
    im.run()
    mk = markup()
    mk.file_IO()
    mk.run()
    mk.save_markup()
