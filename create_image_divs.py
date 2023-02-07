import glob, os
path = '/Users/mathewalex/Documents/GitHub/letallbewell.github.io/images/Photographs/'
images = glob.glob(path+'*.jpg') + glob.glob(path+'*.jpeg')

IMG_DIVS = ''

IMG_DIV = '''
<div class="responsive">
  <div class="gallery">
    <a target="_blank" href="PATH">
      <img src="PATH" width="600" height="400">
    </a>
  </div>
</div> 
'''
IMG_DIVS = '\n'

for img in images:
 
    path = '/'.join(img.split('/')[6:])
    caption = img.split('/')[-1]
    IMG_DIVS += IMG_DIV.replace('PATH', path) + '\n'


print(IMG_DIVS)