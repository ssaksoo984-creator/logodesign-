import sys
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from pypdf.generic import RectangleObject
src,outdir=sys.argv[1],sys.argv[2]
B=9  # 0.125in in pt
W,H=414,630
# 1) printer PDF: bleed + TrimBox/BleedBox
r=PdfReader(src); w=PdfWriter()
for p in r.pages:
    p.trimbox=RectangleObject([B,B,W-B,H-B]); p.bleedbox=RectangleObject([0,0,W,H]); w.add_page(p)
w.add_metadata({'/Title':'RED Playbill – print (5.5x8.5 + 0.125 bleed)'}); w.write(f'{outdir}/RED_Playbill_PRINT_bleed.pdf')
# 2) proof: trimmed
r=PdfReader(src); w=PdfWriter()
for p in r.pages:
    p.mediabox=RectangleObject([B,B,W-B,H-B]); p.cropbox=RectangleObject([B,B,W-B,H-B]); w.add_page(p)
w.add_metadata({'/Title':'RED Playbill – proof'}); w.write(f'{outdir}/RED_Playbill_proof.pdf')
# 3) home booklet: letter landscape 2-up, duplex flip on short edge
r=PdfReader(src); n=len(r.pages); w=PdfWriter()
order=[]
for i in range(n//4):
    order+= [(n-2*i, 1+2*i), (2+2*i, n-1-2*i)]
for L,R in order:
    sheet=PageObject.create_blank_page(width=792,height=612)
    for k,(pn,x) in enumerate(((L,0),(R,396))):
        pg=r.pages[pn-1]
        sheet.merge_transformed_page(pg, Transformation().translate(x-B,-B))
    # clip each half: simple approach — pages already cropped visually by neighbouring placement; draw on top
    w.add_page(sheet)
w.write(f'{outdir}/RED_Playbill_HOME-PRINT_booklet_letter.pdf')
print(order)
