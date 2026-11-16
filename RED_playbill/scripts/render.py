import sys
from playwright.sync_api import sync_playwright
src,out=sys.argv[1],sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto('file://'+src); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
    pg.pdf(path=out,prefer_css_page_size=True,print_background=True)
    b.close()
