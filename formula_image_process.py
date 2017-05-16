import numpy as np
import re
from PIL import Image
import PIL

PAD_TOP, PAD_LEFT, PAD_BOTTOM, PAD_RIGHT = 8,8,8,8
buckets = [[240,100], [320,80], [400,80],[400,100], [480,80], [480,100],\
           [560,80], [560,100], [640,80],[640,100], [720,80], [720,100], \
           [720,120], [720, 200], [800,100],[800,320], [1000,200]]

old_im = Image.open('./test.png').convert('L')
old_size = (old_im.size[0]+PAD_LEFT+PAD_RIGHT, old_im.size[1]+PAD_TOP+PAD_BOTTOM)

print old_size
img_data = np.asarray(old_im, dtype=np.uint8) # height, width
nnz_inds = np.where(img_data!=255)      
y_min = np.min(nnz_inds[0])
y_max = np.max(nnz_inds[0])
x_min = np.min(nnz_inds[1])
x_max = np.max(nnz_inds[1])
old_im = old_im.crop((x_min, y_min, x_max+1, y_max+1))
old_size = (old_im.size[0]+PAD_LEFT+PAD_RIGHT, old_im.size[1]+PAD_TOP+PAD_BOTTOM)
j = -1
for i in range(len(buckets)):
    if old_size[0]<=buckets[i][0] and old_size[1]<=buckets[i][1]:
        j = i
        break
if j < 0:
    new_size = old_size
    new_im = Image.new("RGB", new_size, (255,255,255))
    new_im.paste(old_im, (PAD_LEFT,PAD_TOP))       
new_size = buckets[j]
print new_size
new_im = Image.new("RGB", new_size, (255,255,255))
new_im.paste(old_im, (PAD_LEFT,PAD_TOP))

ratio = 2
assert ratio>=1, ratio
old_size = new_im.size
new_size = (int(old_size[0]/ratio), int(old_size[1]/ratio))
new_im = new_im.resize(new_size, PIL.Image.LANCZOS)
new_im.save('./test.png')