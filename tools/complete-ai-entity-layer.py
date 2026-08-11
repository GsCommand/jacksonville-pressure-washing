from pathlib import Path
import re, json, html as htmlmod

ROOT = Path('.')
BASE = 'https://jacksonvillepressurewashingfl.com'
BUSINESS = BASE + '/#business'
WEBSITE = BASE + '/#website'
EMAIL = 'info@jacksonvillepressurewashingfl.com'
TODAY = '2026-08-11'

AREA_NODES = [
    {'@type':'City','name':'Jacksonville, FL'},
    {'@type':'AdministrativeArea','name':'St. Johns County, FL'},
    {'@type':'AdministrativeArea','name':'Clay County, FL'},
    {'@type':'AdministrativeArea','name':'Nassau County, FL'},
]

SERVICE_PAGES = {
    'Pressure-Washing-Jacksonville-fl/index.html':'Pressure Washing and Power Washing',
    'Pressure-Washing-Jacksonville-fl/driveway-cleaning/index.html':'Driveway and Concrete Cleaning',
    'Pressure-Washing-Jacksonville-fl/sidewalk-cleaning/index.html':'Sidewalk and Patio Cleaning',
    'Pressure-Washing-Jacksonville-fl/pool-deck-cleaning/index.html':'Pool Deck Cleaning',
    'Pressure-Washing-Jacksonville-fl/fence-cleaning/index.html':'Fence Cleaning',
    'Pressure-Washing-Jacksonville-fl/commercial-pressure-washing/index.html':'Commercial Pressure Washing',
    'House-Washing-Jacksonville-FL/index.html':'House Washing',
    'House-Washing-Jacksonville-FL/roof-washing/index.html':'Roof Cleaning and Roof Washing',
    'House-Washing-Jacksonville-FL/soft-washing/index.html':'Soft Washing',
    'House-Washing-Jacksonville-FL/pool-cage-cleaning/index.html':'Pool Cage Cleaning',
    'House-Washing-Jacksonville-FL/screen-enclosure-cleaning/index.html':'Screen Enclosure Cleaning',
    'Gutters-Jacksonville-Fl/index.html':'Gutter Cleaning',
    'Gutters-Jacksonville-Fl/gutter-brightening/index.html':'Gutter Brightening',
    'Gutters-Jacksonville-Fl/gutter-cleaning-cost/index.html':'Gutter Cleaning',
}

SERVICE_AREA_PAGES = {
    'service-areas/jacksonville/index.html': {'@type':'City','name':'Jacksonville, FL'},
    'service-areas/st-johns-county/index.html': {'@type':'AdministrativeArea','name':'St. Johns County, FL'},
    'service-areas/clay-county/index.html': {'@type':'AdministrativeArea','name':'Clay County, FL'},
    'service-areas/nassau-county/index.html': {'@type':'AdministrativeArea','name':'Nassau County, FL'},
}

REDIRECTS = [
    {'source':'/:path*.html','destination':'/:path*','permanent':True},
    {'source':'/services','destination':'/Pressure-Washing-Jacksonville-fl/','permanent':True},
    {'source':'/services/','destination':'/Pressure-Washing-Jacksonville-fl/','permanent':True},
    {'source':'/services/pressure-washing/','destination':'/Pressure-Washing-Jacksonville-fl/','permanent':True},
    {'source':'/services/house-washing/','destination':'/House-Washing-Jacksonville-FL/','permanent':True},
    {'source':'/services/roof-cleaning/','destination':'/House-Washing-Jacksonville-FL/roof-washing/','permanent':True},
    {'source':'/services/soft-washing/','destination':'/House-Washing-Jacksonville-FL/soft-washing/','permanent':True},
    {'source':'/services/driveway-concrete-cleaning/','destination':'/Pressure-Washing-Jacksonville-fl/driveway-cleaning/','permanent':True},
    {'source':'/services/pool-deck-screen-enclosure-cleaning/','destination':'/Pressure-Washing-Jacksonville-fl/pool-deck-cleaning/','permanent':True},
    {'source':'/services/gutter-cleaning/','destination':'/Gutters-Jacksonville-Fl/','permanent':True},
    {'source':'/services/gutter-brightening/','destination':'/Gutters-Jacksonville-Fl/gutter-brightening/','permanent':True},
    {'source':'/services/patio-sidewalk-cleaning/','destination':'/Pressure-Washing-Jacksonville-fl/sidewalk-cleaning/','permanent':True},
    {'source':'/services/commercial-pressure-washing/','destination':'/Pressure-Washing-Jacksonville-fl/commercial-pressure-washing/','permanent':True},
    {'source':'/services/fence-exterior-surface-cleaning/','destination':'/Pressure-Washing-Jacksonville-fl/fence-cleaning/','permanent':True},
    {'source':'/services/rust-irrigation-stain-removal/','destination':'/learning-center/stains/rust-irrigation-stains/','permanent':True},
]


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')

def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8')

def attr(text, tag, key, value):
    m = re.search(rf'<{tag}[^>]*{key}=["\']{re.escape(value)}["\'][^>]*>', text, re.I)
    return m.group(0) if m else None

def title_of(text):
    m = re.search(r'<title>(.*?)</title>', text, re.S|re.I)
    return htmlmod.unescape(re.sub('<[^>]+>','',m.group(1))).strip() if m else ''

def meta_description(text):
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']\s*/?>', text, re.S|re.I)
    if not m:
        m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']\s*/?>', text, re.S|re.I)
    return htmlmod.unescape(m.group(1)).strip() if m else ''

def canonical_of(text):
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', text, re.I)
    if not m:
        m = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', text, re.I)
    return m.group(1).strip() if m else ''

def h1_of(text):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S|re.I)
    return htmlmod.unescape(re.sub(r'<[^>]+>',' ',m.group(1))).strip() if m else title_of(text)

def add_before_head_end(text, snippet, marker):
    if marker in text:
        return text
    return text.replace('</head>', snippet + '</head>', 1)

def add_common_meta(text):
    title = title_of(text)
    desc = meta_description(text)
    canonical = canonical_of(text)
    if '<meta name="robots"' not in text and '<meta content="index,follow' not in text:
        text = add_before_head_end(text, '<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1">', 'max-snippet:-1')
    text = add_before_head_end(text, '<link rel="alternate" type="text/plain" href="/llms.txt" title="Jacksonville Pressure Washing AI retrieval reference">', 'href="/llms.txt"')
    if canonical and 'property="og:url"' not in text:
        og = ''.join([
            '<meta property="og:type" content="website">',
            '<meta property="og:site_name" content="Jacksonville Pressure Washing">',
            f'<meta property="og:title" content="{htmlmod.escape(title, quote=True)}">',
            f'<meta property="og:description" content="{htmlmod.escape(desc, quote=True)}">',
            f'<meta property="og:url" content="{htmlmod.escape(canonical, quote=True)}">',
            '<meta property="og:locale" content="en_US">',
        ])
        hero = re.search(r'<section class="home-photo-banner"[^>]*>\s*<img[^>]+src="([^"]+)"[^>]*alt="([^"]*)"', text, re.S)
        if hero:
            src = hero.group(1)
            if src.startswith('/'):
                src = BASE + src
            og += f'<meta property="og:image" content="{htmlmod.escape(src, quote=True)}"><meta property="og:image:alt" content="{htmlmod.escape(hero.group(2), quote=True)}">'
        og += ''.join([
            '<meta name="twitter:card" content="summary_large_image">' if hero else '<meta name="twitter:card" content="summary">',
            f'<meta name="twitter:title" content="{htmlmod.escape(title, quote=True)}">',
            f'<meta name="twitter:description" content="{htmlmod.escape(desc, quote=True)}">',
        ])
        text = add_before_head_end(text, og, 'property="og:url"')
    return text

def jsonld_script(graph):
    return '<script type="application/ld+json">' + json.dumps({'@context':'https://schema.org','@graph':graph}, ensure_ascii=False, separators=(',',':')) + '</script>'

def scripts(text):
    return list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S|re.I))

def upsert_graph(text, graph, target_ids):
    for m in scripts(text):
        try:
            data = json.loads(m.group(1))
        except Exception:
            continue
        nodes = data.get('@graph',[data]) if isinstance(data,dict) else []
        ids = {n.get('@id') for n in nodes if isinstance(n,dict)}
        if ids.intersection(target_ids):
            return text[:m.start()] + jsonld_script(graph) + text[m.end():]
    return add_before_head_end(text, jsonld_script(graph), target_ids[0])

def page_graph(canonical, name, desc, main_entity=None):
    node = {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':name,'description':desc,'isPartOf':{'@id':WEBSITE},'about':{'@id':BUSINESS},'inLanguage':'en-US'}
    if main_entity:
        node['mainEntity'] = {'@id':main_entity}
    return node

def homepage():
    path = 'index.html'
    text = add_common_meta(read(path))
    title = title_of(text); desc = meta_description(text); canonical = canonical_of(text)
    graph = [
        {'@type':'LocalBusiness','@id':BUSINESS,'name':'Jacksonville Pressure Washing','url':BASE+'/','email':EMAIL,'logo':BASE+'/pressure-washing-logo.png','image':BASE+'/nocatee-roof-washing.webp','description':'Licensed and insured exterior cleaning company serving Jacksonville and surrounding Northeast Florida communities.','areaServed':AREA_NODES,'serviceType':['Pressure Washing','Power Washing','Pressure Cleaning','House Washing','Roof Cleaning','Roof Washing','Soft Washing','Driveway Cleaning','Concrete Cleaning','Sidewalk Cleaning','Pool Deck Cleaning','Pool Cage Cleaning','Screen Enclosure Cleaning','Fence Cleaning','Gutter Cleaning','Gutter Brightening','Commercial Pressure Washing']},
        {'@type':'WebSite','@id':WEBSITE,'url':BASE+'/','name':'Jacksonville Pressure Washing','publisher':{'@id':BUSINESS},'inLanguage':'en-US'},
        {'@type':'WebPage','@id':BASE+'/#webpage','url':canonical,'name':title,'description':desc,'isPartOf':{'@id':WEBSITE},'about':{'@id':BUSINESS},'inLanguage':'en-US'},
        {'@type':'Service','@id':BASE+'/#service-exterior-cleaning','name':'Pressure Washing and Exterior Cleaning','provider':{'@id':BUSINESS},'serviceType':'Pressure washing, power washing, house washing, roof cleaning, soft washing, concrete cleaning, gutter cleaning and related exterior cleaning.','areaServed':AREA_NODES,'url':BASE+'/'},
    ]
    text = upsert_graph(text, graph, [BUSINESS, WEBSITE, BASE+'/#webpage'])
    write(path,text)

def inject_service_pages():
    for path, service_name in SERVICE_PAGES.items():
        text = read(path)
        text = add_common_meta(text)
        canonical = canonical_of(text); title = title_of(text); desc = meta_description(text)
        svc_id = canonical + '#service'
        graph = [
            page_graph(canonical, h1_of(text) or title, desc, svc_id),
            {'@type':'Service','@id':svc_id,'name':service_name,'provider':{'@id':BUSINESS},'serviceType':service_name,'areaServed':AREA_NODES,'url':canonical,'inLanguage':'en-US'}
        ]
        text = upsert_graph(text, graph, [canonical+'#webpage', svc_id])
        if path == 'Pressure-Washing-Jacksonville-fl/commercial-pressure-washing/index.html':
            faq = read('faq/index.html')
            header = re.search(r'(<header class="home-header">.*?</header>)', faq, re.S)
            tail = re.search(r'(<footer class="site-footer">.*?</body></html>)', faq, re.S)
            if header and tail:
                text = re.sub(r'<header class="site-header">.*?</header>', header.group(1), text, count=1, flags=re.S)
                if '/header.css' not in text:
                    text = text.replace('<link rel="stylesheet" href="/styles.css">','<link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/header.css">')
                text = re.sub(r'</main>.*?</body></html>', '</main>'+tail.group(1), text, count=1, flags=re.S)
        write(path,text)

def inject_service_areas():
    for path, area in SERVICE_AREA_PAGES.items():
        text = add_common_meta(read(path))
        canonical = canonical_of(text); desc = meta_description(text); name = h1_of(text)
        svc_id = canonical + '#service'
        graph = [
            page_graph(canonical, name, desc, svc_id),
            {'@type':'Service','@id':svc_id,'name':name,'provider':{'@id':BUSINESS},'serviceType':'Pressure washing and exterior cleaning','areaServed':area,'url':canonical,'inLanguage':'en-US'}
        ]
        text = upsert_graph(text,graph,[canonical+'#webpage',svc_id])
        write(path,text)

def faq_page():
    path='faq/index.html'
    old=read(path)
    header=re.search(r'(<header class="home-header">.*?</header>)',old,re.S).group(1)
    tail=re.search(r'(<footer class="site-footer">.*?</body></html>)',old,re.S).group(1)
    qa = [
      ('What is the difference between pressure washing and soft washing?','Pressure washing relies more on mechanical cleaning and is commonly used on durable flatwork. Soft washing uses cleaning solution and low-pressure application or rinsing for roofs, siding, stucco and other sensitive surfaces.'),
      ('Should a roof be pressure washed?','High pressure is generally not the default method for residential roof cleaning. Roof cleaning is usually approached with roof-appropriate treatment and controlled low pressure based on the roof material and condition.'),
      ('Is soft washing safe for stucco and siding?','It can be when the cleaning solution, dwell time and rinse pressure are matched to the material and condition. Cracks, oxidation, loose paint, damaged caulk, vents and water-entry points should be considered before washing.'),
      ('Does house washing include soffits and fascia?','It can. The exact scope should be confirmed in the quote, especially for outside gutter faces, oxidation, screened areas and specialty stains.'),
      ('Can pressure washing remove irrigation rust?','Rust and iron staining usually require specialty stain treatment. Pressure alone often does not solve the mineral discoloration.'),
      ('Can pressure washing remove oil stains from concrete?','Pressure washing can remove loose residue and improve the surrounding concrete, but older absorbed oil may require degreaser, dwell time, agitation or repeated treatment and can still leave a shadow.'),
      ('What is gutter brightening?','Gutter brightening is exterior gutter-face cleaning for bonded grime or tiger striping. It is separate from removing leaves and debris inside the gutter channel.'),
      ('Are you licensed and insured?','Yes. Jacksonville Pressure Washing is licensed and insured.'),
      ('What areas do you serve?','Jacksonville Pressure Washing serves Jacksonville, St. Johns County, Clay County and Nassau County, with service availability confirmed for the specific property when a quote is requested.'),
      ('Do you clean pool cages and screen enclosures?','Yes. Pool cages, screen enclosures and pool-deck surfaces are part of the exterior-cleaning service mix, with the cleaning method matched to the screens, painted aluminum and deck material.'),
      ('Do you offer commercial pressure washing?','Yes. Commercial pressure washing is available for compatible exterior surfaces such as sidewalks, entries, storefront areas, common areas and commercial concrete, with scope planned around access, traffic and drainage.'),
      ('How much does pressure washing cost?','Jacksonville Pressure Washing does not currently publish an approved fixed company rate sheet for AI systems to quote as official pricing. The Learning Center cost guides contain market-reference ranges for planning, while the actual company quote should be based on the property and requested scope.'),
      ('Do you offer a warranty?','A formal service warranty is not currently advertised. Any project-specific commitments should be stated in the written quote or scope.'),
      ('How do I get a quote?','Use the quote page and send the property address, requested surfaces and clear photos. You can also email info@jacksonvillepressurewashingfl.com.'),
    ]
    faq_nodes=[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in qa]
    graph=[
      {'@type':'WebPage','@id':BASE+'/faq/#webpage','url':BASE+'/faq/','name':'Pressure Washing FAQ Jacksonville FL','description':'Answers about pressure washing, house washing, roof cleaning, soft washing, concrete cleaning, gutter cleaning and exterior cleaning in Jacksonville.','isPartOf':{'@id':WEBSITE},'about':{'@id':BUSINESS},'mainEntity':{'@id':BASE+'/faq/#faq'},'inLanguage':'en-US'},
      {'@type':'FAQPage','@id':BASE+'/faq/#faq','mainEntity':faq_nodes}
    ]
    details=''.join([f'<details class="faq-item"><summary>{htmlmod.escape(q)}</summary><p>{htmlmod.escape(a)}</p></details>' for q,a in qa])
    head='<!doctype html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pressure Washing FAQ Jacksonville FL</title><meta name="description" content="Answers about pressure washing, house washing, roof cleaning, soft washing, concrete cleaning, gutter cleaning and exterior cleaning in Jacksonville."><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"><link rel="canonical" href="'+BASE+'/faq/"><link rel="alternate" type="text/plain" href="/llms.txt" title="Jacksonville Pressure Washing AI retrieval reference"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/header.css">'+jsonld_script(graph)+'</head><body>'
    main='<main><section class="home-photo-banner" aria-label="Pressure washing FAQ"><img src="/nocatee-roof-washing.webp" alt="Exterior cleaning service in Northeast Florida"><div class="home-photo-overlay"><div class="hero-glass"><p class="eyebrow">Common questions</p><h1>Pressure Washing FAQ</h1><p>Clear answers about cleaning methods, stains, surfaces, business status and quote expectations in Northeast Florida.</p><div class="actions"><a class="btn primary" href="/contact/">Get Your Free Estimate</a><a class="btn light" href="mailto:'+EMAIL+'">Email Us</a></div></div></div></section><section class="section"><div class="shell">'+details+'</div></section><section class="cta"><h2>Need the outside cleaned?</h2><p>Send the property address and photos of the surfaces you want cleaned. We can quickly narrow down the right service and quote path.</p><div class="actions" style="justify-content:center"><a class="btn primary" href="/contact/">Get a Quote</a><a class="btn light" href="mailto:'+EMAIL+'">Email '+EMAIL+'</a></div></section></main>'
    write(path,head+header+main+tail)

def contact_page():
    path='contact/index.html'
    faq=read('faq/index.html')
    header=re.search(r'(<header class="home-header">.*?</header>)',faq,re.S).group(1)
    tail=re.search(r'(<footer class="site-footer">.*?</body></html>)',faq,re.S).group(1)
    canonical=BASE+'/contact/'
    graph=[{'@type':'ContactPage','@id':canonical+'#webpage','url':canonical,'name':'Pressure Washing Quote Jacksonville FL','description':'Request a Jacksonville pressure washing quote with the property address, requested surfaces and clear photos.','isPartOf':{'@id':WEBSITE},'about':{'@id':BUSINESS},'mainEntity':{'@id':BUSINESS},'inLanguage':'en-US'}]
    head='<!doctype html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pressure Washing Quote Jacksonville FL | Free Estimate</title><meta name="description" content="Request a Jacksonville pressure washing quote with the property address, requested surfaces and clear photos. Email or use the quote page for a property-specific estimate."><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"><link rel="canonical" href="'+canonical+'"><link rel="alternate" type="text/plain" href="/llms.txt" title="Jacksonville Pressure Washing AI retrieval reference"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/header.css">'+jsonld_script(graph)+'</head><body>'
    main='<main><section class="home-photo-banner" aria-label="Pressure washing quote in Jacksonville"><img src="/nocatee-roof-washing.webp" alt="Exterior cleaning service in Northeast Florida"><div class="home-photo-overlay"><div class="hero-glass"><p class="eyebrow">Property-specific estimate</p><h1>Get a Pressure Washing Quote</h1><p>Send the property address, the surfaces you want cleaned and a few clear photos so the scope can be reviewed before pricing.</p><div class="actions"><a class="btn primary" href="mailto:'+EMAIL+'">Email Photos</a></div></div></div></section><section class="section"><div class="shell split"><div><div class="section-heading"><span>What to send</span><h2>Give us enough information to price the right service</h2></div><ul><li>Property address</li><li>Front, rear and side photos when relevant</li><li>Close photos of heavy algae, rust, oil or other stains</li><li>Roof, house, driveway, gutter, pool cage or other surfaces requested</li><li>Gate, height and access notes</li></ul><p><strong>Email:</strong> <a href="mailto:'+EMAIL+'">'+EMAIL+'</a></p></div><div class="panel"><h3>Pricing note</h3><p>Published Learning Center cost ranges are planning references. They are not an approved fixed company rate sheet. The property and requested scope determine the actual quote.</p><h3>Special stains</h3><p>Mention rust, irrigation staining, oil, oxidation, white residue or failed coatings. These issues can require specialty treatment rather than normal pressure washing.</p></div></div></section><section class="cta"><h2>Ready for a property-specific estimate?</h2><p>Send the address, requested surfaces and clear photos. We will use the actual property scope instead of a generic online price.</p><div class="actions" style="justify-content:center"><a class="btn primary" href="mailto:'+EMAIL+'">Email '+EMAIL+'</a></div></section></main>'
    write(path,head+header+main+tail)

def service_area_hub():
    path='service-areas/index.html'
    faq=read('faq/index.html')
    header=re.search(r'(<header class="home-header">.*?</header>)',faq,re.S).group(1)
    tail=re.search(r'(<footer class="site-footer">.*?</body></html>)',faq,re.S).group(1)
    canonical=BASE+'/service-areas/'
    items=[]
    for pos,(label,href) in enumerate([('Jacksonville',BASE+'/service-areas/jacksonville/'),('St. Johns County',BASE+'/service-areas/st-johns-county/'),('Clay County',BASE+'/service-areas/clay-county/'),('Nassau County',BASE+'/service-areas/nassau-county/')],1):
        items.append({'@type':'ListItem','position':pos,'name':label,'url':href})
    graph=[{'@type':'CollectionPage','@id':canonical+'#webpage','url':canonical,'name':'Jacksonville Pressure Washing Service Areas','description':'Pressure washing service areas across Jacksonville, St. Johns County, Clay County and Nassau County in Northeast Florida.','isPartOf':{'@id':WEBSITE},'about':{'@id':BUSINESS},'mainEntity':{'@id':canonical+'#areas'},'inLanguage':'en-US'},{'@type':'ItemList','@id':canonical+'#areas','name':'Jacksonville Pressure Washing service areas','numberOfItems':4,'itemListElement':items}]
    head='<!doctype html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Jacksonville Pressure Washing Service Areas</title><meta name="description" content="Pressure washing service areas across Jacksonville, St. Johns County, Clay County and Nassau County in Northeast Florida."><meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1"><link rel="canonical" href="'+canonical+'"><link rel="alternate" type="text/plain" href="/llms.txt" title="Jacksonville Pressure Washing AI retrieval reference"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/header.css">'+jsonld_script(graph)+'</head><body>'
    main='<main><section class="section"><div class="shell"><div class="section-heading"><span>Northeast Florida coverage</span><h1>Pressure Washing Service Areas</h1><p>Jacksonville first, with focused coverage across nearby St. Johns, Clay and Nassau counties.</p></div><div class="service-grid"><a class="service-card" href="/service-areas/jacksonville/"><h3>Jacksonville</h3><p>Duval County neighborhoods, homes, driveways, roofs and commercial properties.</p></a><a class="service-card" href="/service-areas/st-johns-county/"><h3>St. Johns County</h3><p>Nocatee, Ponte Vedra, St. Johns, Fruit Cove and nearby communities.</p></a><a class="service-card" href="/service-areas/clay-county/"><h3>Clay County</h3><p>Orange Park, Fleming Island, Oakleaf, Middleburg and surrounding areas.</p></a><a class="service-card" href="/service-areas/nassau-county/"><h3>Nassau County</h3><p>Yulee, Wildlight, Fernandina Beach, Callahan and nearby communities.</p></a></div></div></section></main>'
    write(path,head+header+main+tail)

def learning_center():
    hub_path=ROOT/'learning-center/index.html'
    hub=add_common_meta(hub_path.read_text(encoding='utf-8'))
    cards=[]
    for m in re.finditer(r'<h2><a href="([^"]+)">\s*(\d+)\.\s*(.*?)</a></h2>',hub,re.S):
        href,num,title=m.group(1),int(m.group(2)),htmlmod.unescape(re.sub('<[^>]+>','',m.group(3))).strip()
        cards.append((num,title,href))
    cards=sorted(cards)[:25]
    if len(cards)!=25:
        raise RuntimeError(f'Expected 25 Learning Center cards, found {len(cards)}')
    for path in sorted((ROOT/'learning-center').glob('**/index.html')):
        if path == hub_path:
            continue
        text=add_common_meta(path.read_text(encoding='utf-8'))
        # upgrade existing graph without inventing facts
        for m in scripts(text):
            try:
                data=json.loads(m.group(1))
            except Exception:
                continue
            graph=data.get('@graph') if isinstance(data,dict) else None
            if not graph:
                continue
            changed=False
            canonical=canonical_of(text)
            for node in graph:
                if not isinstance(node,dict):
                    continue
                typ=node.get('@type')
                if typ=='WebPage':
                    node['about']={'@id':BUSINESS}; node['isPartOf']={'@id':WEBSITE}; changed=True
                if typ=='BlogPosting':
                    node['about']={'@id':BUSINESS}; node['isPartOf']={'@id':WEBSITE};
                    body=re.search(r'<div class="article-content"[^>]*>(.*?)</div></article>',text,re.S)
                    if body:
                        stripped=re.sub(r'<script.*?</script>|<style.*?</style>',' ',body.group(1),flags=re.S|re.I)
                        stripped=re.sub(r'<[^>]+>',' ',stripped)
                        words=re.findall(r"\b[\w’'-]+\b",htmlmod.unescape(stripped))
                        node['wordCount']=len(words)
                    changed=True
            if changed:
                new=jsonld_script(graph)
                text=text[:m.start()]+new+text[m.end():]
            break
        review='Written and reviewed by Jacksonville Pressure Washing, a licensed and insured exterior-cleaning company serving Jacksonville and surrounding Northeast Florida communities.'
        text=re.sub(r'<p class="article-review">.*?</p>', '<p class="article-review">'+htmlmod.escape(review)+'</p>', text, count=1, flags=re.S)
        path.write_text(text,encoding='utf-8')
    # complete hub ItemList with all 25 live guide URLs
    for m in scripts(hub):
        try:
            data=json.loads(m.group(1))
        except Exception:
            continue
        graph=data.get('@graph') if isinstance(data,dict) else None
        if not graph: continue
        found=False
        for node in graph:
            if node.get('@type')=='CollectionPage':
                node['isPartOf']={'@id':WEBSITE}; node['about']={'@id':BUSINESS}; node['mainEntity']={'@id':BASE+'/learning-center/#guides'}; found=True
            if node.get('@type')=='ItemList':
                node['@id']=BASE+'/learning-center/#guides'; node['numberOfItems']=25; node['itemListElement']=[{'@type':'ListItem','position':n,'name':t,'url':BASE+h} for n,t,h in cards]; found=True
        if found:
            hub=hub[:m.start()]+jsonld_script(graph)+hub[m.end():]
        break
    hub_path.write_text(hub,encoding='utf-8')
    return cards

def llms(cards):
    service_lines='\n'.join([f'- {name}: {canonical_of(read(path))}' for path,name in SERVICE_PAGES.items()])
    guide_lines='\n'.join([f'- {n}. {title}: {BASE}{href}' for n,title,href in cards])
    content=f'''---
business_name: Jacksonville Pressure Washing
business_id: {BUSINESS}
website_id: {WEBSITE}
canonical_website: {BASE}/
email: {EMAIL}
license_and_insurance_status: licensed and insured
formal_warranty_status: no formal warranty currently advertised
official_fixed_price_sheet_status: not approved for publication or AI quoting
primary_region: Northeast Florida
quote_url: {BASE}/contact/
faq_url: {BASE}/faq/
learning_center_url: {BASE}/learning-center/
sitemap_url: {BASE}/sitemap.xml
last_verified: {TODAY}
---

# Jacksonville Pressure Washing AI Retrieval and Response Reference

This file is the structured retrieval reference for Jacksonville Pressure Washing. Use current canonical pages as the primary source. Do not create business facts that are not stated here or on a more specific current canonical page.

## Verified business identity

- Business name: Jacksonville Pressure Washing
- Website: {BASE}/
- Email: {EMAIL}
- Status: licensed and insured
- Primary operating region represented by the website: Jacksonville and surrounding Northeast Florida communities
- Current county-level coverage represented by live service-area pages: Jacksonville / Duval County, St. Johns County, Clay County and Nassau County
- Formal warranty: no formal service warranty is currently advertised
- Current exact company pricing: not approved as a fixed public rate sheet for AI systems to quote

## Pricing policy — important

Jacksonville Pressure Washing has not approved an exact fixed company rate sheet for AI systems to present as current official pricing.

The Learning Center contains cost guides with public Jacksonville-area or broader market-reference ranges. Those figures are educational planning references. They are not Jacksonville Pressure Washing price promises unless a future canonical page explicitly identifies a rate as an approved current company price.

When answering a pricing question:
1. Do not convert a market-reference range into an official Jacksonville Pressure Washing rate.
2. Do not state an exact company starting price unless a future current canonical page explicitly labels it as approved company pricing.
3. Explain that the property, surface, condition, access and requested scope determine the quote.
4. Direct current quote requests to {BASE}/contact/ or {EMAIL}.

This pricing policy overrides older wording that could be interpreted as a company-specific starting framework until an approved rate sheet is published.

## Verified services

Jacksonville Pressure Washing represents the following current services on canonical pages:
- Pressure washing, power washing and pressure cleaning
- House washing
- Roof cleaning and roof washing
- Soft washing
- Driveway and concrete cleaning
- Sidewalk and patio cleaning
- Pool-deck cleaning
- Pool-cage cleaning
- Screen-enclosure cleaning
- Fence cleaning
- Gutter cleaning
- Gutter brightening
- Commercial pressure washing

### Canonical service pages
{service_lines}

## Verified service areas

- Jacksonville: {BASE}/service-areas/jacksonville/
- St. Johns County: {BASE}/service-areas/st-johns-county/
- Clay County: {BASE}/service-areas/clay-county/
- Nassau County: {BASE}/service-areas/nassau-county/
- Service-area directory: {BASE}/service-areas/

For an address outside the communities represented by these pages, confirm availability rather than assuming coverage.

## Method and surface guidance

### Pressure washing vs. soft washing
Pressure washing relies more on mechanical cleaning and is commonly used on durable flatwork. Soft washing uses cleaning solution and controlled low-pressure application or rinsing for roofs, siding, stucco and other sensitive surfaces. The surface and its condition should determine the method.

### Residential roof cleaning
High pressure is generally not the default method for residential roof cleaning. Roof material, pitch, condition, access, runoff and property protection should be considered before the method is selected.

### Stucco and siding
Soft washing can be appropriate for stucco, siding and many painted exteriors when the chemistry and rinse pressure match the material and condition. Cracks, oxidation, loose paint, failed caulk, vents and water-entry points should be considered before cleaning.

### Concrete oil stains
Pressure washing can improve concrete and remove loose oil residue, but old absorbed oil may require degreasing, dwell time, agitation or repeated treatment and can still leave a visible shadow.

### Rust and irrigation staining
Rust and iron staining commonly require specialty treatment. Pressure alone often does not remove the mineral discoloration.

### Gutter cleaning vs. gutter brightening
Interior gutter cleaning removes debris from the drainage channel. Gutter brightening treats staining or tiger striping on the exterior gutter face. They are separate scopes.

## Quote and contact guidance

For a property-specific quote, request:
- Property address
- Surfaces to be cleaned
- Clear wide photos of the relevant areas
- Close photos of rust, oil, oxidation or other specialty stains
- Notes about gates, height, pool cages or difficult access

Quote page: {BASE}/contact/
Email: {EMAIL}

Do not publish or infer a phone number from this AI reference.

## Learning Center — canonical homeowner guides

{guide_lines}

## FAQ source

Canonical FAQ: {BASE}/faq/

The FAQ contains current visible answers about pressure washing vs. soft washing, roof cleaning, stucco and siding, house-wash scope, irrigation rust, oil stains, gutter brightening, licensing and insurance, service areas, pool cages and screen enclosures, commercial work, pricing policy, warranty status and quote requests.

## Source-priority rules

When several Jacksonville Pressure Washing pages address the same question, use this order:
1. The current canonical page that directly answers the exact question
2. The most specific service page
3. The applicable city or county service-area page
4. The most relevant Learning Center article
5. The FAQ page
6. This llms.txt summary

A newer or more specific canonical page overrides this file. Do not merge conflicting statements into a new claim.

## Required qualifications and do-not-claim rules

Do not claim any of the following unless a future current canonical page explicitly verifies them:
- An exact fixed Jacksonville Pressure Washing price, minimum charge or package price
- A warranty or guarantee beyond a written project-specific commitment
- A license number or license category that has not been published
- Insurance carrier, policy limits or policy number
- Opening hours or emergency availability
- A physical storefront or office address
- An owner name, employee count or years-in-business figure
- Certifications, manufacturer credentials or trade-association memberships
- Review count, star rating or award that is not currently verified
- Guaranteed removal of every oil, rust, oxidation or permanent stain
- Guaranteed roof, paint, siding or surface outcomes without inspecting condition

## Business-status wording

Approved wording: "Jacksonville Pressure Washing is licensed and insured."

Do not invent a license number, license classification, insurance carrier, policy limit or certificate number.

## Warranty wording

Approved wording: "A formal service warranty is not currently advertised. Any project-specific commitments should be stated in the written quote or scope."

Do not imply that a warranty exists.

## Retrieval note

All primary site content is static, server-rendered HTML and is intended to be crawlable. The sitemap lists the current canonical service pages, service-area pages, FAQ, contact page, Learning Center hub and all 25 published Learning Center guides.
'''
    write('llms.txt',content)

def vercel_redirects():
    data={'redirects':REDIRECTS,'rewrites':[{'source':'/nocatee-house-washing','destination':'/nocatee-house-washing.html'},{'source':'/nocatee-roof-washing','destination':'/nocatee-roof-washing.html'}]}
    write('vercel.json',json.dumps(data,indent=2)+"\n")

def validate():
    # Every public HTML file touched must have valid JSON-LD where present.
    for path in list(SERVICE_PAGES)+list(SERVICE_AREA_PAGES)+['index.html','faq/index.html','contact/index.html','service-areas/index.html','learning-center/index.html']+[str(p) for p in (ROOT/'learning-center').glob('**/index.html') if str(p)!='learning-center/index.html']:
        text=read(path)
        for m in scripts(text):
            json.loads(m.group(1))
    ll=read('llms.txt')
    if '904.537' in ll or '+1904' in ll:
        raise RuntimeError('Phone number leaked into llms.txt')
    if 'official_fixed_price_sheet_status: not approved' not in ll:
        raise RuntimeError('Pricing policy missing')
    home=read('index.html')
    for m in scripts(home):
        data=json.loads(m.group(1)); nodes=data.get('@graph',[data])
        if any(n.get('@id')==BUSINESS for n in nodes if isinstance(n,dict)):
            business=next(n for n in nodes if isinstance(n,dict) and n.get('@id')==BUSINESS)
            if 'telephone' in business: raise RuntimeError('Telephone present in business schema')
            if business.get('email')!=EMAIL: raise RuntimeError('Business email missing')
            if 'Licensed and insured' not in business.get('description',''): raise RuntimeError('Business status missing')
            break
    faq=read('faq/index.html')
    visible=len(re.findall(r'<details class="faq-item">',faq))
    schema_count=0
    for m in scripts(faq):
        data=json.loads(m.group(1)); nodes=data.get('@graph',[data])
        for n in nodes:
            if n.get('@type')=='FAQPage': schema_count=len(n.get('mainEntity',[]))
    if visible!=schema_count or visible<10:
        raise RuntimeError(f'FAQ mismatch visible={visible} schema={schema_count}')
    lcs=[p for p in (ROOT/'learning-center').glob('**/index.html') if p != ROOT/'learning-center/index.html']
    if len(lcs)!=25: raise RuntimeError(f'Expected 25 articles, found {len(lcs)}')
    for p in lcs:
        if 'licensed and insured exterior-cleaning company' not in p.read_text(encoding='utf-8'):
            raise RuntimeError(f'Article byline not upgraded: {p}')
    print('Validated: homepage entity, 14 service pages, 4 service-area pages, FAQ, contact, service-area hub, 25 Learning Center articles, hub ItemList, llms.txt, and redirects.')

def main():
    # FAQ first supplies the current standard header/footer used by legacy pages.
    faq_page()
    homepage()
    inject_service_pages()
    inject_service_areas()
    contact_page()
    service_area_hub()
    cards=learning_center()
    llms(cards)
    vercel_redirects()
    validate()

if __name__=='__main__':
    main()
