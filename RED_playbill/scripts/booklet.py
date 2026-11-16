import sys, fitz
src,out=sys.argv[1],sys.argv[2]
d=fitz.open(src); o=fitz.open(); n=len(d); B=9
order=[]
for i in range(n//4): order+=[(n-2*i,1+2*i),(2+2*i,n-1-2*i)]
clip=fitz.Rect(B,B,414-B,630-B)
for L,R in order:
    pg=o.new_page(width=792,height=612)
    for pn,x in ((L,0),(R,396)):
        pg.show_pdf_page(fitz.Rect(x,0,x+396,612),d,pn-1,clip=clip)
o.save(out,garbage=3,deflate=True)
