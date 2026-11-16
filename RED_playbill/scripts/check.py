import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file://'+sys.argv[1]); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
    print(pg.evaluate("""()=>{const o=[];document.querySelectorAll('.page').forEach((s,i)=>{s.querySelectorAll('.b,.body,.lc,.row').forEach(e=>{const r=e.getBoundingClientRect();let m=r.bottom;e.querySelectorAll('*').forEach(c=>{const q=c.getBoundingClientRect();if(q.height>0)m=Math.max(m,q.bottom)});if(m>r.bottom+1.5)o.push([i+1,e.className,Math.round(m-r.bottom)])})});return o}"""))
    b.close()
