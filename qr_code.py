import pyqrcode
import png
from pyqrcode import QRCode
import matplotlib.pyplot as plt
import matplotlib.image as img
s="https://www.geeksforgeeks.org/problem-of-the-day"
url=pyqrcode.create(s)
url.svg("myqr.svg",scale=8)
url.png("myqr.png",scale=6)
im=img.imread("myqr.png")
plt.imshow(im)
plt.axis('off')
plt.show()
