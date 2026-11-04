"""Split a layered SVG, cover-crop background, center intact foreground, export SVG/JPG."""
import argparse
import copy
import io
import json
import math
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

S = 'http://www.w3.org/2000/svg'
ET.register_namespace('', S)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
SIZES = [('WeChat',2350,1000),('WeChat',1000,1000),('WeChat',1080,1440),('X',2000,800),('X',1600,900)]
META = {'defs','style','title','desc','metadata'}
def tag(e): return e.tag.split('}')[-1]
def number(x): return float(str(x).removesuffix('px'))

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('--output', required=True, type=Path, help='New output directory; never overwrite')
    p.add_argument('--background-id', help='Explicit background element/group ID when auto split is ambiguous')
    p.add_argument('--python-path', action='append', default=[], help='Existing dependency directory; no automatic installation')
    p.add_argument('--max-bytes', type=int, default=1000000)
    a = p.parse_args()
    for path in a.python_path: sys.path.insert(0, path)
    from PIL import Image, ImageOps, ImageDraw
    import resvg_py
    if a.output.exists(): raise ValueError('Output already exists. Choose a new directory.')
    raw = a.source.read_text(encoding='utf-8-sig')
    if re.search(r'<!DOCTYPE|<!ENTITY|<script|<foreignObject', raw, re.I):
        raise ValueError('Unsupported active/external SVG content.')
    root = ET.fromstring(raw)
    for el in root.iter():
        if tag(el) == 'text': raise ValueError('Live text found: convert text to outlines to avoid font substitution.')
        for k,v in el.attrib.items():
            if k.split('}')[-1] == 'href' and not v.startswith(('#','data:image/')):
                raise ValueError('Embed external image references before exporting.')
    for value in re.findall(r'url[(](.*?)[)]', raw):
        if not value.strip().strip(chr(34)+chr(39)).startswith('#'): raise ValueError('External CSS URL is unsupported.')
    vb = [float(v) for v in root.get('viewBox','').replace(',',' ').split()]
    if not vb: vb = [0,0,number(root.get('width')),number(root.get('height'))]
    x,y,w,h = vb
    if min(w,h) <= 0 or max(w,h)>16000: raise ValueError('Invalid or oversized SVG canvas.')
    leaves=[]
    def walk(e):
        if tag(e) in META: return
        if tag(e) in {'svg','g'}:
            for child in e: walk(child)
        else: leaves.append(e)
    walk(root)
    if a.background_id:
        found=[e for e in root.iter() if e.get('id') == a.background_id]
        if len(found)!=1: raise ValueError('Background ID must identify exactly one element.')
        bg=found[0]
    else:
        bg=leaves[0] if leaves else None
        if bg is None or tag(bg) not in {'rect','image'}:
            raise ValueError('Cannot auto-detect background; inspect layers and use --background-id.')
        if abs(number(bg.get('x',0))-x)>2 or abs(number(bg.get('y',0))-y)>2 or number(bg.get('width',0))<w*.98 or number(bg.get('height',0))<h*.98:
            raise ValueError('First layer is not a full-canvas background. Use --background-id.')
    def split(e, mode):
        if e is bg: return copy.deepcopy(e) if mode=='bg' else None
        if tag(e) in META: return copy.deepcopy(e)
        if mode=='fg' and not any(c is bg for c in e.iter()): return copy.deepcopy(e)
        children=[v for c in e if (v:=split(c,mode)) is not None]
        if e is root or any(tag(c) not in META for c in children):
            out=copy.copy(e); out[:]=children; return out
        return None
    background, foreground = split(root,'bg'), split(root,'fg')
    def render(el,width,height):
        data=resvg_py.svg_to_bytes(svg_string=ET.tostring(el,encoding='unicode'),width=width,height=height)
        return Image.open(io.BytesIO(bytes(data))).convert('RGBA')
    mw,mh=math.ceil(w),math.ceil(h)
    alpha=render(foreground,mw,mh).getchannel('A')
    bounds=alpha.point(lambda v:255 if v>8 else 0).getbbox()
    if not bounds: raise ValueError('No separate foreground. Flattened SVG cannot be automatically rearranged.')
    bx0,by0,bx1,by1=bounds
    bx0,bx1=x+bx0*w/mw,x+bx1*w/mw
    by0,by1=y+by0*h/mh,y+by1*h/mh
    fw,fh=bx1-bx0,by1-by0
    results=[]; thumbs=[]; pending=[]
    for platform,tw,th in SIZES:
        name=f'{platform}_{tw}x{th}'
        # X 2000x800 uses the established project safe band (20%-85%), not a platform guarantee.
        top,bottom=(.20*th,.85*th) if (tw,th)==(2000,800) else (.07*th,.93*th)
        scale=min(1, .86*tw/fw,(bottom-top)/fh)
        cx,cy=tw/2,(top+bottom)/2
        tx,ty=cx-scale*(bx0+bx1)/2,cy-scale*(by0+by1)/2
        out=ET.Element('{'+S+'}svg',{'width':str(tw),'height':str(th),'viewBox':f'0 0 {tw} {th}'})
        b=copy.deepcopy(background); b.set('width',str(tw)); b.set('height',str(th)); b.set('preserveAspectRatio','xMidYMid slice'); b.set('overflow','hidden')
        out.append(b)
        g=ET.SubElement(out,'{'+S+'}g',{'transform':f'translate({tx} {ty}) scale({scale})'})
        f=copy.deepcopy(foreground); f.set('x',str(x)); f.set('y',str(y)); f.set('width',str(w)); f.set('height',str(h)); g.append(f)
        # Definitions are shared by both layers; remove duplicates in foreground.
        ids=set()
        def dedupe(e):
            for child in list(e):
                ident=child.get('id')
                if ident and ident in ids: e.remove(child); continue
                if ident: ids.add(ident)
                dedupe(child)
        dedupe(out)
        rgba=render(out,tw,th)
        im=Image.new('RGB',(tw,th),'black'); im.paste(rgba,mask=rgba.getchannel('A'))
        for q in range(95,44,-2):
            buf=io.BytesIO(); im.save(buf,'JPEG',quality=q,subsampling=0,optimize=True)
            if buf.tell()<=a.max_bytes: break
        else: raise ValueError(f'{name}: cannot meet byte limit at acceptable quality.')
        pending.append((name,ET.tostring(out,encoding='utf-8',xml_declaration=True),buf.getvalue()))
        bounds_out=[tx+scale*bx0,ty+scale*by0,tx+scale*bx1,ty+scale*by1]
        assert bounds_out[0]>=0 and bounds_out[1]>=0 and bounds_out[2]<=tw and bounds_out[3]<=th
        results.append(dict(file=name,width=tw,height=th,jpg_bytes=buf.tell(),quality=q,foreground_bounds=bounds_out))
        thumb=ImageOps.contain(im,(440,270)); panel=Image.new('RGB',(460,310),'#222222'); panel.paste(thumb,((460-thumb.width)//2,25)); ImageDraw.Draw(panel).text((10,290),name,fill='white'); thumbs.append(panel)
    a.output.mkdir(parents=True,exist_ok=False)
    for name,svg,jpg in pending:
        (a.output/(name+'.svg')).write_bytes(svg); (a.output/(name+'.jpg')).write_bytes(jpg)
    sheet=Image.new('RGB',(920,930),'#222222')
    for i,im in enumerate(thumbs): sheet.paste(im,((i%2)*460,(i//2)*310))
    sheet.save(a.output/'preview.jpg')
    (a.output/'report.json').write_text(json.dumps({'source':str(a.source.resolve()),'outputs':results},indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(f'Export failed: {exc}',file=sys.stderr); sys.exit(1)
