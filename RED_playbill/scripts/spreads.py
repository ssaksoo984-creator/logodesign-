import sys, pymupdf, cv2, numpy as np
src,pdf_out,jpg_out=sys.argv[1:4]
d=pymupdf.open(src); n=len(d); B=9
pairs=[(n,1)]+[(i,i+1) for i in range(2,n,2)]
clip=pymupdf.Rect(B,B,414-B,630-B)
o=pymupdf.open()
for L,R in pairs:
    pg=o.new_page(width=792,height=612)
    for pn,x in ((L,0),(R,396)): pg.show_pdf_page(pymupdf.Rect(x,0,x+396,612),d,pn-1,clip=clip)
o.save(pdf_out,garbage=3,deflate=True)
ims=[]
for i,p in enumerate(o):
    p.get_pixmap(dpi=95).save('/tmp/s.png'); im=cv2.imread('/tmp/s.png')
    cv2.line(im,(im.shape[1]//2,0),(im.shape[1]//2,im.shape[0]),(120,120,120),1)
    ims.append(cv2.copyMakeBorder(im,24,24,24,24,cv2.BORDER_CONSTANT,value=(60,60,60)))
rows=[np.hstack(ims[k:k+2]) for k in range(0,len(ims),2)]
cv2.imwrite(jpg_out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,88]); print(pairs)
