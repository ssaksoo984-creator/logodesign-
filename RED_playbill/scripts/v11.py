import re
B='/home/claude/build'
src=open(f'{B}/playbill_v1.html').read()
bios={}
for m in re.finditer(r'<img src="img/hs_(\w+)\.jpg" alt="">\s*<div><h3>(.*?)</h3><div class="role">(.*?)</div>\s*<div class="txt">(.*?)</div></div>',src,re.S):
    bios[m.group(1)]=(m.group(2),m.group(3),m.group(4))
R='#c8191e'; K='#16191b'; W='#ecebe7'
FONTS=''.join(f'@font-face{{font-family:{f};font-weight:{wt};font-style:{st};src:url(fonts/{fn})}}' for f,wt,st,fn in [
 ('Ds',400,'normal','instrument-serif-latin-400-normal.woff2'),('Ds',400,'italic','instrument-serif-latin-400-italic.woff2'),
 ('Sn',400,'normal','inter-latin-400-normal.woff2'),('Sn',500,'normal','inter-latin-500-normal.woff2'),('Sn',600,'normal','inter-latin-600-normal.woff2'),
 ('Pt',400,'normal','Pretendard-Regular.woff2'),('Pt',500,'normal','Pretendard-Medium.woff2'),('Pt',600,'normal','Pretendard-SemiBold.woff2'),
 ('Tx',400,'normal','source-serif-4-latin-400-normal.woff2'),('Tx',400,'italic','source-serif-4-latin-400-italic.woff2'),
 ('Tx',600,'normal','source-serif-4-latin-600-normal.woff2'),('Tx',400,'normal','source-serif-4-latin-ext-400-normal.woff2')])
CSS=f'''{FONTS}
@page{{size:5.75in 8.75in;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
html{{background:#555}}body{{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:Pt,sans-serif;font-size:7pt;line-height:1.6;letter-spacing:-.005em;word-break:keep-all;font-kerning:normal}}
@media screen{{body{{display:grid;grid-template-columns:repeat(2,5.75in);justify-content:center;row-gap:.5in;padding:.5in 0}}.page{{order:1;box-shadow:0 2px 14px rgba(0,0,0,.35)}}.page.back{{order:0}}}}
.page{{width:5.75in;height:8.75in;position:relative;overflow:hidden;break-after:page;--ink:#333;--line:rgba(51,51,51,.13);color:var(--ink)}}
.page::after{{content:"";position:absolute;inset:0;background:url(img4/grain.png) 0 0/1.6in;pointer-events:none;z-index:50}}
.wht{{background:{W} url(img6/paper.jpg) center/cover}} .wht::after{{mix-blend-mode:multiply;opacity:.13}}
.red{{background:{R};--ink:#fff;--line:rgba(0,0,0,.14)}} .red::after{{background-image:url(img6/grain_soft.png);mix-blend-mode:multiply;opacity:.6}}
.blk{{background:{K};--ink:#e6e4df;--line:rgba(236,235,231,.13)}} .blk::after{{mix-blend-mode:screen;opacity:.07}}
.cov::after{{background-image:url(img6/grain_soft.png);mix-blend-mode:multiply;opacity:.45}}
.a{{position:absolute}}
/* running head / foot */
.rh,.rf{{position:absolute;left:.6in;right:.6in;display:flex;justify-content:space-between;font-family:Sn;font-weight:500;font-size:5.2pt;letter-spacing:.2em;text-transform:uppercase;z-index:8}}
.rh{{top:.48in}} .rf{{bottom:.4in;padding-top:.09in;border-top:.5pt solid var(--line)}}
.rf .n{{font-family:Ds;font-size:8.5pt;letter-spacing:.02em;line-height:.7}}
.body{{position:absolute;left:.6in;right:.6in;top:.95in;bottom:.78in;display:flex;flex-direction:column;z-index:5}}
.cap{{font-family:Sn;font-weight:500;font-size:5.4pt;letter-spacing:.2em;text-transform:uppercase}}
.acc{{color:{R}}} .red .acc{{color:#fff}}
.th{{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:.16in;border-bottom:.5pt solid var(--line)}}
.th h1{{font-family:Ds;font-weight:400;font-size:25pt;line-height:.95;letter-spacing:-.012em}}
.th h1 i{{font-style:italic;font-family:Ds}}
.sq{{display:inline-block;width:.075in;height:.075in;background:{R};margin-left:.07in}} .red .sq{{background:#fff}}
.ic{{width:.36in;height:.36in;flex:none;color:{R}}} .red .ic{{color:#fbf3ee}}
.ic svg{{width:100%;height:100%;fill:none;stroke:currentColor;stroke-width:1.15;stroke-linecap:round;stroke-linejoin:round}}
.row{{display:grid;grid-template-columns:1.25in 1fr;padding:.1in 0;border-bottom:.5pt solid var(--line)}}
.ld{{display:flex;justify-content:space-between;align-items:baseline;line-height:1.8}}
.ld span:first-child{{font-size:6.8pt}} .ld span:last-child{{font-family:Ds;font-size:10.5pt}}
.chip{{display:inline-block;font-family:Sn;font-weight:500;font-size:5pt;letter-spacing:.14em;text-transform:uppercase;line-height:1.5;color:#6d5300;background:#f6e7a9;padding:.035in .07in;position:relative;z-index:6}}
.ph{{}}
/* bios: rows share the height equally */
.rows{{flex:1;display:grid;min-height:0}}
.b{{display:grid;gap:.22in;padding-top:.17in;border-top:.5pt solid var(--line);min-height:0}}
.rows .b:first-child{{border-top:0}}
.b img{{width:100%;aspect-ratio:3/4;object-fit:cover;display:block;filter:grayscale(1) contrast(1.04)}}
.b .nm{{font-family:Ds;font-size:16pt;line-height:1;margin:.06in 0 .09in;letter-spacing:-.005em}}
.b .tx{{text-align:left}} .b .tx i,.body i:not(h1 i){{font-style:normal}}
.r2 .b{{grid-template-columns:1.3in 1fr}} .r2 .tx{{font-size:6.6pt;line-height:1.55}}
.r3 .b{{grid-template-columns:1in 1fr;gap:.2in;padding-top:.14in}} .r3 .tx{{font-size:6.1pt;line-height:1.48}} .r3 .b .nm{{font-size:13.5pt;margin:.04in 0 .05in}}
/* v9: chapter tag, bands that cross the gutter */
.tag{{display:inline-block;background:{R};color:#fff;border-radius:99px;padding:.012in .075in .006in;margin-right:.08in;font-weight:600;letter-spacing:.1em}}
.red .tag{{background:#fff;color:{R}}}
.band{{position:absolute;left:0;right:0;bottom:0;top:3.75in;z-index:3}} .band.half{{top:4.375in}}
.rf.on-red{{color:#fff;border-top-color:rgba(0,0,0,.14);z-index:9}} .rf.on-dark{{color:#e6e4df;border-top-color:rgba(236,235,231,.24);z-index:9}}
.cols2{{columns:2;column-gap:.26in;font-size:6.8pt;line-height:1.62}}
/* v10 */
.col{{display:flex;flex-direction:column;min-height:0}}
.col .ph{{width:100%;aspect-ratio:5/6;object-fit:cover;display:block;filter:grayscale(1) contrast(1.04)}}
.col .nm{{font-family:Ds;font-size:13pt;line-height:1.05;margin:.04in 0 .08in}}
.col .tx{{font-size:6.2pt;line-height:1.5}} .col .tx i{{font-style:normal}}
.hr{{border-top:.5pt solid var(--line)}}
/* v11 — editorial index layout */
.xl{{font-family:Ds;font-size:38pt;line-height:.9;letter-spacing:-.022em}} .xl i{{font-style:italic}}
.pill{{display:inline-block;border:.5pt solid var(--line);border-radius:99px;padding:.028in .085in .018in;font-family:Sn;font-weight:500;font-size:4.8pt;letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}}
.mk{{width:.09in;height:.09in;background:{R};display:block}}
.lx{{display:grid;grid-template-columns:.95in 1fr;gap:.18in}}
.lrow{{display:grid;grid-template-columns:.4in 1fr auto;gap:.12in;align-items:baseline;padding:.058in 0;border-bottom:.5pt solid var(--line)}}
.lrow:first-child{{border-top:.5pt solid var(--line)}}
.idx{{font-family:Sn;font-weight:500;font-size:5.6pt;letter-spacing:.04em;color:{R}}}
.lrow .rt{{font-family:Ds;font-size:10.5pt;line-height:1}}
.spd{{display:flex;justify-content:space-between;font-family:Sn;font-weight:500;font-size:5.2pt;letter-spacing:.2em;text-transform:uppercase;padding-top:.1in;border-top:.5pt solid var(--line)}}
.stmt{{font-family:Ds;font-size:13pt;line-height:1.18;letter-spacing:-.005em}}
'''
IC={
'record':'<circle cx="24" cy="24" r="19"/><circle cx="24" cy="24" r="13.5"/><circle cx="24" cy="24" r="6"/><circle cx="24" cy="24" r=".6"/>',
'brush':'<path d="M21 4h6v17h-6z"/><path d="M19 21h10v6H19z"/><path d="M19 27c0 6-1 11-2 16h14c-1-5-2-10-2-16"/><path d="M22 31v8M26 31v8"/>',
'can':'<ellipse cx="24" cy="15" rx="14" ry="4.5"/><path d="M10 15v24c0 2.5 6.3 4.5 14 4.5s14-2 14-4.5V15"/><path d="M10 17C7 6 41 6 38 17"/><path d="M19 19.3v9a2 2 0 0 0 4 0v-8.8"/>',
'glass':'<path d="M11 8h26l-3.5 33h-19z"/><path d="M12.6 23h22.8"/><path d="M19 27h7v7h-7z" transform="rotate(-12 22 30)"/>',
'bulb':'<path d="M24 3v12"/><path d="M20.5 15h7v5h-7z"/><path d="M20.5 20c-5 3-7 7-7 11a10.5 10.5 0 0 0 21 0c0-4-2-8-7-11"/><path d="M21 33l3-4 3 4"/>'}
ic=lambda k:f'<div class="ic"><svg viewBox="0 0 48 48">{IC[k]}</svg></div>'
def rh(ch,sec,style=''): return f'<div class="rh" style="{style}"><span>Red — John Logan</span><span><span class="tag">{ch}</span>{sec}</span></div>'
def rf(n,side,cls='',style=''):
    num=f'<span class="n">{n:02d}</span>'; t='<span>Triple M Productions</span>'
    return f'<div class="rf {cls}" style="{style}">{num+t if side=="verso" else t+num}</div>'
def frame(n,ch,sec,side): return rh(ch,sec)+rf(n,side)
def th(title,icon): return f'<div class="th"><h1>{title}<span class="sq"></span></h1>{ic(icon)}</div>'
def bio(k):
    nm,rl,tx=bios[k]; return f'<div class="b"><img src="img4/hs_{k}.jpg"><div><div class="cap acc">{rl}</div><div class="nm">{nm}</div><div class="tx">{tx}</div></div></div>'
def rows(keys): return f'<div class="rows r{len(keys)}" style="grid-template-rows:repeat({len(keys)},1fr)">{"".join(bio(k) for k in keys)}</div>'
CAST=[('Mark Rothko','Rob LaBelle*'),('Ken','Mozi Mayaleh*')]
TEAM=[('Director','Jennifer Copping'),('Producer','Rhonda Dent'),('Production Designer','Starlynn Chen'),('Lighting Designer','Sam Cheng'),('Sound Designer','Ben Elliott'),('Stage Manager','Gerri Torres'),('Assistant Stage Manager','Lucas Nasu Nielsen'),('Publicity &amp; Social Media','Elizabeth McCarthy Meek')]
ld=lambda rs:''.join(f'<div class="ld"><span>{a}</span><span>{b}</span></div>' for a,b in rs)
LOR='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante venenatis dapibus posuere velit aliquet. Donec ullamcorper nulla non metus auctor fringilla. Maecenas faucibus mollis interdum. Cras mattis consectetur purus sit amet fermentum. Vestibulum id ligula porta felis euismod semper. '
P=[]
BIO_ROTHKO='<p>Born Marcus Rothkowitz in Dvinsk, in the Russian Empire (today Daugavpils, Latvia), Rothko emigrated with his family to Portland, Oregon, at the age of ten. After two years at Yale he left for New York, studied at the Art Students League and began painting city scenes and figures.</p><p style="margin-top:.06in">By 1950 he had arrived at the image he is known for: soft-edged rectangles of colour floating on vast canvases, meant to be seen up close. He rejected the label of Abstract Expressionist and insisted his paintings were about human emotion. In 1958 he accepted a commission to paint murals for the Four Seasons restaurant in New York’s Seagram Building; he later withdrew and returned the fee.</p>'
ABOUT_RED='<p>John Logan’s <i>Red</i> premiered at London’s Donmar Warehouse in December 2009 and transferred to Broadway the following year, where it won six Tony Awards, including Best Play.</p><p style="margin-top:.06in">Logan, screenwriter of <i>Gladiator</i>, <i>Hugo</i> and <i>Skyfall</i>, imagines Rothko at work on the Seagram murals with Ken, a young (fictional) assistant. What begins as a job becomes a fierce argument about art, commerce, mortality, and the generation that will one day take the master’s place.</p>'
P.append('<section class="page cov" style="background:#b8161a url(img4/cover_poster.jpg) center/100% 100% no-repeat"></section>')

# 2 credits — index layout
def cl(rows,start):
    return ''.join(f'<div class="lrow"><span class="idx">[{start+i:02d}]</span><span>{a}</span><span class="rt">{b}</span></div>' for i,(a,b) in enumerate(rows))
P.append(f"""<section class="page wht verso">{rh('01','The Company')}
 <div class="body">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
   <div class="xl">Cast <i>&amp;</i><br>Creative</div>{ic('record')}</div>
  <div style="height:.34in"></div>
  <div class="lx"><div><span class="pill">The Cast</span></div><div>{cl(CAST,1)}</div></div>
  <img src="img6/band_hands_red.jpg" style="display:block;margin:.2in 0 .2in 1.13in;width:3.42in;height:1.02in;object-fit:cover">
  <div class="lx"><div><span class="pill">Creative Team</span></div><div>{cl(TEAM,3)}</div></div>
  <div style="flex:1;min-height:.1in"></div>
  <div class="lx" style="padding-top:.14in;border-top:.5pt solid var(--line)">
   <div class="cap acc">Time &amp;<br>Place</div>
   <div style="font-size:7pt">Mark Rothko’s studio on the Bowery, New York City. 1958–1959.</div></div>
  <div class="lx" style="padding-top:.13in">
   <div class="cap acc">Land<br>Acknowledgement</div>
   <div style="font-size:6.1pt;line-height:1.5">We gratefully acknowledge that this production takes place on the unceded traditional territories of the xʷməθkʷəy̓əm (Musqueam), Sḵwx̱wú7mesh (Squamish) and səlilwətaɨ (Tsleil-Waututh) Nations. <span class="chip">Draft</span>
    <div style="font-size:5.8pt;margin-top:.06in">*Member of Canadian Actors’ Equity Association. A Canadian Actors’ Equity Association production under the Artists’ Collective Policy.</div></div></div>
 </div>{rf(2,'verso')}
</section>""")

# 3 Rothko + the play — two bracketing headlines
BIO_ROTHKO='<p>Born Marcus Rothkowitz in Dvinsk, in the Russian Empire (today Daugavpils, Latvia), Rothko emigrated with his family to Portland, Oregon, at the age of ten. After two years at Yale he left for New York, studied at the Art Students League and began painting city scenes and figures.</p><p style="margin-top:.07in">Through the 1940s his work moved from myth and surrealism toward pure abstraction. He became a central figure of Abstract Expressionism, though he rejected the label and insisted his paintings were about human emotion.</p><p style="margin-top:.07in">In 1958 he accepted a commission to paint murals for the Four Seasons restaurant in New York’s Seagram Building. He later withdrew and returned the fee.</p>'
ABOUT_RED='<p>John Logan’s <i>Red</i> premiered at London’s Donmar Warehouse in December 2009 and transferred to Broadway the following year, where it won six Tony Awards, including Best Play.</p><p style="margin-top:.07in">Logan, screenwriter of <i>Gladiator</i>, <i>Hugo</i> and <i>Skyfall</i>, imagines Rothko at work on the Seagram murals with Ken, a young assistant of the playwright’s invention. Over two years in the studio the two men circle each other through argument, labour and silence.</p>'
P.append(f"""<section class="page wht recto">{rh('02','The Painter &amp; The Play')}
 <div class="body" style="bottom:auto;height:3.75in">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
   <div class="xl">Mark<br>Rothko</div>{ic('brush')}</div>
  <div style="flex:1;min-height:.2in"></div>
  <div class="lx">
   <div><span class="mk"></span><div class="cap acc" style="margin-top:.1in">The<br>Painter</div></div>
   <div class="stmt">Soft-edged rectangles of colour floating on vast canvases, meant to be seen up close.</div></div>
  <div class="spd" style="margin:.17in 0 .14in"><span>1903</span><span>Dvinsk — New York</span><span>1970</span></div>
  <div class="cols2" style="font-size:6.6pt;line-height:1.6">{BIO_ROTHKO}</div>
 </div>
 <div class="band" style="top:4.95in;background:url(img6/paint_red.jpg) center/cover;color:#fff;padding:.42in .6in 0">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
   <div class="xl">The Play</div><div class="ic" style="color:#fff"><svg viewBox="0 0 48 48">{IC['glass']}</svg></div></div>
  <div style="height:.22in"></div>
  <div class="lx">
   <div><span class="mk" style="background:#fff"></span><div class="cap" style="margin-top:.1in">John<br>Logan</div><div style="margin-top:.14in"><span class="chip">Draft texts<br>please review</span></div></div>
   <div class="stmt">A fierce argument about art, commerce, mortality, and the generation that will one day take the master’s place.</div></div>
  <div class="spd" style="margin:.17in 0 .14in;border-top-color:rgba(0,0,0,.18)"><span>Donmar 2009</span><span>Broadway 2010</span><span>Six Tonys</span></div>
  <div class="cols2" style="font-size:6.6pt;line-height:1.6">{ABOUT_RED}</div>
 </div>{rf(3,'recto','on-red')}
</section>""")

# 4 cast — both actors on one page, two equal columns
def actor(img,bg,tex,role,name,who,pos):
    return f"""<div class="col">
   <div style="position:relative;height:3.45in;background:{bg} url(img6/{tex}.jpg) center/cover;overflow:hidden"><img src="img4/{img}.png" style="position:absolute;bottom:0;left:50%;transform:translateX(-{pos}%);height:100%"></div>
   <div class="cap acc" style="margin-top:.16in">as {role}</div>
   <div style="font-family:Ds;font-size:17pt;line-height:1;margin:.05in 0 .1in">{name}</div>
   <div><span class="chip">Bio to come from {who}</span></div>
   <div style="font-size:6.6pt;line-height:1.55;margin-top:.08in;flex:1;overflow:hidden">{LOR}{LOR}</div></div>"""
P.append(f"""<section class="page wht verso">{frame(4,'03','The Cast','verso')}
 <div class="body">{th('The Cast','glass')}
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:.24in;padding-top:.2in;min-height:0">
   {actor('rob',R,'paint_red','Mark Rothko','Rob LaBelle','Rob',58)}{actor('mozi',K,'paint_dark','Ken','Mozi Mayaleh','Mozi',50)}
  </div></div></section>""")
# 5 in rehearsal
P.append(f"""<section class="page wht recto">
 <img class="a" src="img6/reh_a.jpg" style="left:0;top:0;width:100%;height:4.6in;object-fit:cover">
 {rh('04','In Rehearsal','color:#fff')}
 <div class="body" style="top:4.88in">
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:.24in;min-height:0">
   <img src="img6/reh_b.jpg" style="width:100%;height:100%;object-fit:cover;min-height:0"><img src="img6/reh_c.jpg" style="width:100%;height:100%;object-fit:cover;min-height:0"></div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:.12in"><span class="cap acc">In Rehearsal</span><span class="chip">Placeholder images · rehearsal photos to come</span></div>
 </div>{rf(5,'recto')}
</section>""")

# 6|7 director / producer — photos meet at the gutter
def lead(n,side,ch,sec,k,ttl):
    nm,rl,tx=bios[k]; fs='7.3pt' if len(tx)>900 else '8.2pt'
    ph=f'<img class="a" src="img4/hs_{k}.jpg" style="top:.85in;{"right:0" if side=="verso" else "left:0"};width:3.25in;height:4.15in;object-fit:cover;object-position:50% 22%;filter:grayscale(1) contrast(1.04)">'
    side_box=f'<div class="a" style="top:1.0in;bottom:3.75in;{"left:.6in" if side=="verso" else "right:.6in"};width:1.6in;display:flex;flex-direction:column;justify-content:flex-end;{"" if side=="verso" else "text-align:right"}"><div class="cap acc">{rl}</div><div style="font-family:Ds;font-size:24pt;line-height:.98;margin-top:.08in">{nm.replace(" ","<br>")}</div></div>'
    return f"""<section class="page wht {side}">{ph}{rh(ch,sec)}{side_box}
 <div class="body" style="top:5.25in"><div class="hr" style="padding-top:.2in;flex:1;min-height:0"><div class="cols2" style="font-size:{fs};line-height:1.72">{tx}</div></div></div>{rf(n,side)}</section>"""
P.append(lead(6,'verso','05','Direction','jennifer','Director'))
P.append(lead(7,'recto','05','Direction','rhonda','Producer'))

# 8|9 team — photo row on top, title band, text columns (Garden-lounge layout)
def person(k):
    nm,rl,tx=bios[k]
    return f'<div class="col"><img class="ph" src="img4/hs_{k}.jpg"></div>', f'<div class="col"><div class="cap acc">{rl}</div><div class="nm">{nm}</div><div class="tx">{tx}</div></div>'
def team(n,side,keys,title):
    ps=[person(k) for k in keys]
    grid=lambda cells,st='':f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.2in;{st}">{"".join(cells)}</div>'
    return f"""<section class="page wht {side}">{rh('06','The Team')}
 <div class="body">
  {grid([p[0] for p in ps])}
  <div style="height:.78in;display:flex;justify-content:space-between;align-items:center">{title}</div>
  {grid([p[1] for p in ps],'flex:1;min-height:0;padding-top:.14in;border-top:.5pt solid var(--line)')}
 </div>{rf(n,side)}</section>"""
P.append(team(8,'verso',['starlynn','sam','ben'],'<div style="font-family:Ds;font-size:32pt;line-height:1;letter-spacing:-.01em">Design<span class="sq"></span></div><div style="font-family:Ds;font-size:22pt">06</div>'))
P.append(team(9,'recto',['gerri','lucas','liz'],'<div style="font-family:Ds;font-size:32pt;line-height:1;letter-spacing:-.01em">Production<span class="sq"></span></div><div class="ic">'+f'<svg viewBox="0 0 48 48">{IC["record"]}</svg></div>'))

# 10 thank you + ad
names=''.join('<div style="padding:.055in 0;border-bottom:.5pt solid var(--line)">Name Surname</div>' for _ in range(16))
P.append(f"""<section class="page wht verso">{rh('07','With Gratitude')}
 <div class="body" style="bottom:4.6in">{th('Thank You','glass')}
  <div style="flex:1;display:grid;grid-template-columns:1fr 1.22in;gap:.22in;padding-top:.16in;min-height:0">
   <div><span class="chip">List to come from Jennifer &amp; Rhonda</span><div style="columns:2;column-gap:.2in;margin-top:.08in;font-size:7.3pt">{names}</div></div>
   <img src="img6/can.jpg" style="width:100%;height:100%;object-fit:cover;min-height:0"></div></div>
 <div class="a" style="left:0;right:0;bottom:0;height:4.375in;background:#dcdad5;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;z-index:6">
  <div class="cap">Half-page advertisement</div><div style="font-family:Ds;font-size:24pt;margin:.08in 0"><i>Eureka Day</i></div>
  <div class="cap" style="line-height:1.9">Mitch &amp; Murray Productions<br>5.5 × 4.25 in + 0.125 in bleed · PDF or 300 dpi JPG</div></div>
</section>""")
# 11 supporters — full page
logos=['tbirdlogo1000','logonic3positi','rhondadentlogo','alcantarassoci','eplsocialmarke']
cells=''.join(f'<div class="lc{" wide" if i==4 else ""}"><img class="{"sq" if l in ("alcantarassoci","eplsocialmarke") else ""}" src="img/logo_{l}.png"></div>' for i,l in enumerate(logos))
P.append(f"""<section class="page wht recto">{frame(11,'08','Supporters','recto')}
 <style>.lg{{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);min-height:0}}.lc{{display:flex;align-items:center;justify-content:center;padding:.2in;min-height:0;border-top:.5pt solid var(--line)}}.lc:nth-child(odd):not(.wide){{border-right:.5pt solid var(--line)}}.lc.wide{{grid-column:1/3}}.lc img{{max-width:100%;height:.7in;width:auto;object-fit:contain}}.lc img.sq{{height:1.05in}}</style>
 <div class="body">{th('Our Supporters','brush')}
  <div style="padding:.16in 0;display:grid;grid-template-columns:1.25in 1fr"><div class="cap acc" style="padding-top:.03in">With thanks</div><div>Triple M Productions gratefully acknowledges the partners and sponsors whose generosity brought <i>Red</i> to the stage.</div></div>
  <div class="lg">{cells}</div></div></section>""")
# 12 back
P.append(f'''<section class="page blk back" style="background:#070908">
 <img class="a" src="img6/brush.jpg" style="left:0;top:-.5in;width:100%">
 <div class="a" style="left:0;right:0;top:4.6in;bottom:0;background:linear-gradient(rgba(7,9,8,0),#070908 55%);z-index:2"></div>
 <div class="a" style="left:.6in;right:.6in;bottom:.5in;z-index:6">
  <div style="font-family:Ds;font-style:italic;font-size:19pt;color:{R};line-height:1">“What do you see?”</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:.3in;margin-top:.28in;padding-top:.16in;border-top:.5pt solid var(--line)">
   <div><div style="font-family:Ds;font-size:15pt;line-height:1">Triple M Productions</div><div class="cap" style="margin-top:.1in;line-height:1.9;opacity:.8">Red by John Logan<br>Dec 8–12, 2026 · 8 PM<br>The Nest, Granville Island</div></div>
   <div><div class="cap" style="line-height:1.9;opacity:.8">Website<br>Instagram / Facebook<br>Email</div><div style="margin-top:.07in"><span class="chip">Contact details to confirm</span></div></div></div></div>
</section>''')
open(f'{B}/playbill_v11.html','w').write(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>RED — Playbill</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print(len(P),len(bios))
