#!/usr/bin/env python3
"""Builds index.html for the audit-journey site. Every number comes from the Arise & Shine audit
(public data, 11-12 Oct 2026) or from the casebook; models are labelled Illustrative."""
import html, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from qa import QA
OUT = os.path.join(os.path.dirname(__file__), '..', 'index.html')
e = lambda s: html.escape(s, quote=False)
EV = {'v': ('m', 'Verified'), 'o': ('c', 'Observation'), 'i': ('e', 'Inference'), 'u': ('u', 'Unknown'), 'x': ('a', 'Illustrative'), 'r': ('c', 'Reconstruction')}
def ev(k): c, t = EV[k]; return f'<span class="ev {c}">{t}</span>'

STAGES = [
 ('ask', 'The ask'), ('market', 'Market research'), ('audience', 'Audience'), ('web', 'Web design'),
 ('seo', 'SEO & AEO'), ('content', 'Content'), ('paid', 'Paid media'), ('booking', 'Booking'),
 ('journey', 'The journey'), ('choose', 'Choosing the fixes'), ('layers', 'Marketing vs pre-marketing'),
 ('revenue', 'Growth → revenue'), ('plan', '90-day plan'), ('monthly', 'Monthly data'),
 ('data', 'Data control'), ('ai', 'AI in the work'), ('proof', 'Done before'), ('qa', '61 questions'), ('docs', 'Documents'),
]
NUM = {k: f'{i + 1:02d}' for i, (k, _) in enumerate(STAGES)}

def sec(k, h2, lede, inner, cls='', eyebrow=None):
    return (f'<section class="sec wrap j-sec {cls}" id="{k}" aria-labelledby="{k}-h">'
            f'<div class="j-head"><span class="j-n">{NUM[k]}</span><div><p class="eyebrow">{eyebrow or dict(STAGES)[k]}</p>'
            f'<h2 id="{k}-h">{h2}</h2>{f"<p class=j-lede>{lede}</p>" if lede else ""}</div></div>{inner}</section>')

# ---------------- data from the audit ----------------
SALONS = [  # name, area, dist m, rating, reviews, closes (24h), type
 ('Adorn & Admire', 'CMR Main Rd', 360, 4.9, 3580, 21, 'Independent'),
 ('Toni&Guy Essensuals', 'CMR Main Rd', 340, 4.5, 2206, 21, 'Franchise'),
 ('Toni&Guy · HRBR 1st Block', 'HRBR 1st Block', 850, 4.7, 1688, 22, 'Franchise'),
 ('Lakmé Salon · Hennur', 'Hennur', 780, 4.7, 1235, 20, 'Franchise'),
 ('Boon Salon', 'Kammanahalli', 1210, 4.9, 1071, 20, 'Chain'),
 ('Arha Salon & Spa', 'Kammanahalli', 1030, 4.6, 871, 21, 'Independent'),
 ('Spin Salon · Hennur Cross', 'Hennur', 670, 4.8, 830, 20.5, 'Chain'),
 ('Femina Flaunt Studio', 'HRBR 3rd Block', 510, 4.9, 523, 21, 'Independent'),
 ('Studio 11 Family Salon', 'HRBR 2nd Block', 390, 4.6, 493, 21, 'Franchise'),
 ('Vista Salon', 'HRBR 2nd Block', 390, 4.8, 433, 22, 'Independent'),
 ('Grace & Glamour', 'HBR 4th Block', 700, 4.8, 408, 22, 'Independent'),
 ('Spin Salon · Kammanahalli', 'Kammanahalli', 1420, 4.9, 406, None, 'Chain'),
 ('Purple Lounge', 'HBR Layout', 1130, 4.1, 158, None, ''),
 ('Mr. Barber', 'Kammanahalli', 1030, 4.4, 68, None, ''),
 ('Arise & Shine', 'HRBR 2nd Block', 0, 4.9, 35, 22, 'Independent'),
 ('Bebold Salon & Academy', 'HRBR 3rd Block', 470, 5.0, 34, None, ''),
 ('Beauty f Salon', 'HBR 1st Stage', 730, 4.9, 31, None, ''),
 ('Royal Streax', 'HRBR 2nd Block', 660, 5.0, 28, None, ''),
]
data = {
 'reviews': [{'label': n, 'value': r, 'color': 'move' if n == 'Arise & Shine' else 'mute'} for n, a, d, rt, r, h, t in SALONS],
 'hours': [{'label': n + (' (weekends)' if 'HRBR 1st' in n else ''), 'value': h, 'color': 'move' if n == 'Arise & Shine' else 'mute'} for n, a, d, rt, r, h, t in sorted([x for x in SALONS if x[5]], key=lambda x: -x[5])],
 'score': [{'label': a, 'value': v} for a, v in [('In-salon experience', 5), ('Local / Google', 3), ('Reviews & reputation', 3), ('Offers & pricing', 3), ('Website', 2), ('Booking', 2), ('SEO', 1), ('Measurement', 1)]],
}

# ---------------- hero ----------------
hero = f'''
<section class="band hhero j-hero"><div class="wrap">
 <p class="eyebrow">Audit method · live example · proposal stage, contract not signed</p>
 <h1>How I audit a business, <em>from the first conversation to revenue.</em></h1>
 <p class="lede">One real prospect, end to end: Arise &amp; Shine Unisex Salon, Kalyan Nagar, Bengaluru. Market research, audience, web design, SEO, content, paid media, booking, retention, the monthly numbers and the budget. Every step shows what I checked, what I found, what I'd do, and how it reaches revenue.</p>
 <div class="acts"><a class="btn" href="#ask">Start the journey</a><a class="btn ghost" href="docs/arise-shine-growth-audit.pdf">Open the 27-page audit (PDF)</a></div>
 <div class="j-trio">
  <div><small>The chair</small><b class="flow">4.9★</b><span>from 35 Google reviews. Clients love the service.</span>{ev('v')}</div>
  <div><small>The website</small><b class="leak">noindex</b><span>the homepage tells Google not to list it.</span>{ev('v')}</div>
  <div><small>The street</small><b>17</b><span>salons within 1.5 km. One has 3,580 reviews, 360 m away.</span>{ev('v')}</div>
 </div>
 <ol class="j-path" aria-label="The client path I audit"><li>Found</li><li>Chosen</li><li>Booked</li><li>Rebooked</li><li>Recommended</li></ol>
</div></section>'''

nav = '<nav class="subnav j-nav" aria-label="Stages"><div class="wrap"><div class="sn">' + ''.join(f'<a href="#{k}"><span>{NUM[k]}</span>{t}</a>' for k, t in STAGES) + '</div></div></nav>'

# ---------------- 01 the ask ----------------
s_ask = sec('ask', 'Day 0: the owner asks for help.', 'The salon is opening new branches and wants marketing help. Before I quote anything, I audit from public data, so the first conversation is about their numbers, not my services.',
 '''<ol class="j-days">
  <li><small>Sat 10 Oct</small><b>Visit &amp; first conversation</b><p>Owner explains: new salon, more branches planned, wants marketing help.</p></li>
  <li><small>Sun 11 Oct</small><b>Public research</b><p>Website source, Google listing, reviews, prices, offers, 17 competitors, search results.</p></li>
  <li><small>Mon 12 Oct</small><b>Audit + proposal</b><p>27-page audit, real phone screenshots, before/after designs, live proposal site.</p></li>
  <li class="next"><small>Next</small><b>30-minute walkthrough</b><p>At the salon. The noindex fix done free, the same day.</p></li>
 </ol>
 <div class="two j-two">
  <div class="panel"><h3>What I ask in the first conversation</h3><ol class="j-list">
   <li>What does a good month look like: revenue, bookings, new clients?</li><li>Which services make the most money, and which do you want to sell more?</li>
   <li>Where do clients come from today: walk-in, Google, Instagram, referral?</li><li>How do bookings happen: call, WhatsApp, walk-in, software?</li>
   <li>Do clients come back? How do you know?</li><li>What have you spent on marketing, and what came back?</li>
   <li>What is fixed: hours, prices, staff, branches?</li><li>What would make the next 90 days a success for you?</li></ol></div>
  <div class="panel"><h3>What I check before I reply</h3><ul class="j-checks">
   <li><b>Website</b> page source, title, robots tag, speed, every link</li><li><b>Google listing</b> rating, reviews, hours, categories, photos</li>
   <li><b>Prices &amp; offers</b> the ticket ladder and contradictions</li><li><b>Competition</b> every salon within 1.5 km</li>
   <li><b>Search</b> who wins the brand, "best salon" and treatment searches</li><li><b>Social &amp; booking</b> Instagram, WhatsApp, booking platforms</li>
   <li><b>Consistency</b> phone numbers, addresses, hours everywhere</li></ul>
   <p class="cap">No logins needed for the first pass. Access comes only if we work together.</p></div>
 </div>''')

# ---------------- 02 market ----------------
s_market = sec('market', 'The street: 17 salons inside 1.5 km.', 'I map every competitor a client could choose instead: distance, rating, review volume, closing time and what their reviews praise.',
 f'''<div class="j-map"><figure class="panel j-mapfig"><img src="img/street-map.svg" alt="Map of Arise &amp; Shine and 17 salons within 1.5 km in Kalyan Nagar, Bengaluru" loading="lazy"><figcaption class="cap">Google Places listings, 11 Oct 2026 · rings 500 m / 1 km / 1.5 km {ev('v')}</figcaption></figure>
 <div class="j-mapside"><div class="j-stat"><b class="leak">35</b><span>Arise &amp; Shine reviews</span></div><div class="j-stat"><b>3,580</b><span>Adorn &amp; Admire, 360 m away</span></div><div class="j-stat"><b>6</b><span>salons within 400 m</span></div><div class="j-stat"><b class="flow">10 pm</b><span>Arise &amp; Shine closes. Most rivals close at 8–9 pm.</span></div></div></div>
 <div class="charts"><div class="panel"><h3>Review volume, every salon in the circle</h3><div class="chart" id="c-reviews"></div><p class="cap">Arise &amp; Shine in indigo. Rating is near the top; volume is near the bottom. {ev('v')}</p></div>
 <div class="panel"><h3>Closing time on Google</h3><div class="chart" id="c-hours"></div><p class="cap">The late-evening gap is the clearest opening on the street. {ev('v')}</p></div></div>
 <div class="j-cards4">
  <div class="card"><small>Biggest threat</small><b>Adorn &amp; Admire</b><p>3,580 reviews, 360 m away; every review names a stylist.</p></div>
  <div class="card"><small>Strongest brands</small><b>Toni&amp;Guy ×2 · Lakmé</b><p>1,200–2,200 reviews each; some reviews mention price shocks.</p></div>
  <div class="card"><small>Best booking journey</small><b>Spin Salon</b><p>WhatsApp booking pages and bills on WhatsApp.</p></div>
  <div class="card"><small>Most useful to learn from</small><b>Boon Salon</b><p>One stylist became the reason to visit; reviews read like referrals.</p></div>
 </div>
 <p class="j-insight"><b>The pattern:</b> the leaders sell named stylists and hair botox. Arise &amp; Shine has both, and says neither on its website. {ev('i')}</p>''')

# ---------------- 03 audience ----------------
SEG = [
 ('Evening professionals', 'Haircut or grooming after work', '"salon open now", "salon near me" after 7 pm', 'Open till 10 pm daily with valet parking. Most rivals close at 8–9 pm.', 'Google near-me after 7 pm · Maps'),
 ('Frizz-treatment clients', 'Hair botox, nanoplastia, keratin at ₹6,000–12,000', '"hair botox price Kalyan Nagar"', 'Davines &amp; Olaplex, a published price list, offers from ₹3,999. The street\'s most-reviewed service.', 'Treatment pages · reels · search'),
 ('Bridal &amp; pre-bridal', 'Packages, trials, family bookings', 'WeddingWire, Instagram, referrals', 'Premium room, private pedicure station; season runs Oct–Feb.', 'Bridal page · WeddingWire · Instagram'),
 ('Men\'s grooming', 'Packages ₹780–1,500 on weekday evenings', '"men\'s salon near me"', 'Packages already exist; Baxter of California on the shelf.', 'Search · Meta, weekday evenings'),
 ('Lapsed &amp; regular clients', 'The second, third and tenth visit', 'WhatsApp, the counter', 'Clients bring mothers, sisters, daughters (from reviews).', 'Reminders · membership · refer-a-friend'),
]
s_aud = sec('audience', 'Who to win, chosen from evidence.', 'Audiences come from what the business already does well and where rivals are weak, not from a persona template.',
 '<div class="j-seg">' + ''.join(f'<article class="card"><small>Audience {i + 1}</small><h3>{a}</h3><dl><div><dt>What they want</dt><dd>{b}</dd></div><div><dt>Where they look</dt><dd>{c}</dd></div><div><dt>Why Arise &amp; Shine wins</dt><dd>{d}</dd></div><div><dt>Channel</dt><dd>{f}</dd></div></dl></article>' for i, (a, b, c, d, f) in enumerate(SEG)) +
 f'</div><p class="j-insight leakb"><b>Who I would not chase:</b> bargain hunters through deep discounting. They leave for the next offer and train regulars to wait for one. {ev("i")}</p>')

# ---------------- 04 web design ----------------
GRID = [  # client, lands, explained, price, stylist, ba, reviews, slot, whatsapp, next
 ('"Is hair botox worth it?"', 'Pricing page', 'n', 'y', 'n', 'n', 'p', 'n', 'y', 'n'),
 ('"Haircut tonight after work."', 'Home', 'p', 'p', 'n', 'n', 'p', 'n', 'y', 'n'),
 ('"Bridal &amp; pre-bridal."', 'FAQ', 'n', 'p', 'n', 'n', 'n', 'n', 'y', 'n'),
 ('"Nail extensions with art."', 'Offers', 'n', 'y', 'n', 'q', 'n', 'n', 'y', 'n'),
 ('"Men\'s grooming package."', 'Offers', 'p', 'y', 'n', 'n', 'n', 'n', 'y', 'n'),
 ('"Salon near me, Kalyan Nagar."', 'Google listing', 'p', 'n', 'p', 'q', 'y', 'q', 'p', 'n'),
]
cols = ['Service explained', 'Price shown', 'Stylist named', 'Before / after', 'Reviews', 'Book a slot', 'WhatsApp', 'Told what happens next']
sym = {'y': ('ok', '✓', 'Works'), 'p': ('pt', '~', 'Partly'), 'n': ('no', '✕', 'Missing'), 'q': ('q', '?', 'Not verifiable')}
grid = '<div class="tw"><table class="j-grid"><thead><tr><th>The client says…</th><th>Lands on</th>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr></thead><tbody>' + ''.join(
 f'<tr><th scope="row">{r[0]}</th><td class="land">{r[1]}</td>' + ''.join(f'<td><span class="g-{sym[x][0]}" title="{sym[x][2]}">{sym[x][1]}</span></td>' for x in r[2:]) + '</tr>' for r in GRID) + '</tbody></table></div>'
gchk = [('Fix this week', 'leak', ['Robots meta "noindex, nofollow" on the homepage', 'Title is only the domain; no meta description', 'Contact URL ends in "/v"', 'Facebook &amp; YouTube icons link to "#"']),
        ('High', 'est', ['No H1; section titles are plain text', 'No page per treatment', 'Counters render "0 +"', 'No salon schema seen', 'FAQ points to a "Book Now" section that doesn\'t exist']),
        ('Medium', 'move', ['Images without alt text', 'Typos: "Men- Services"', 'Ten testimonials with no source or date', 'No analytics or pixel visible', 'Speed to be measured']),
        ('In place', 'flow', ['A full price list (+GST stated)', 'Offers page with fixed-price deals', 'Men\'s / women\'s split', 'WhatsApp booking link', 'Policy pages'])]
BA = [('home', 'Homepage', 'The first screen: a generic line, "0 +" counters and a chat pop-up over the headline, rebuilt around ★4.9, open till 10 pm, need-based buttons and the stylists.'),
      ('menu', 'Menu card', 'The price list reorganised as a ticket ladder: entry, trade-up and hero treatments, with the saving shown.'),
      ('offers', 'Offers', 'Offers that show the list price and the saving ("save ₹2,001"), on the first screen instead of two pages away.')]
def ba_tabs(items, name):
    tabs = ''.join(f'<button role="tab" type="button" data-t="{k}" aria-selected="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}">{t}</button>' for i, (k, t, _) in enumerate(items))
    panes = ''.join(f'<figure class="j-ba" data-p="{k}"{"" if i == 0 else " hidden"}><p class="cap">{c}</p><a href="img/ba-{k}.jpg" target="_blank" rel="noopener"><img src="img/ba-{k}.jpg" alt="Before and after: {t}" loading="lazy"></a><figcaption class="cap">Left: live screenshot, 12 Oct 2026 {ev("v")} · Right: design preview {ev("x")} · Tap the image to open it full size.</figcaption></figure>' for i, (k, t, c) in enumerate(items))
    return f'<div class="j-tabs" data-tabs><div class="j-tabbar" role="tablist" aria-label="{name}">{tabs}</div>{panes}</div>'
s_web = sec('web', 'The website, read two ways: by Google and by a client.', 'A good-looking site with a real price list, held back by settings and a first screen that doesn\'t sell.',
 f'''<div class="j-phones"><figure><img src="img/live-home-m-fold.jpg" alt="Live homepage on a phone" loading="lazy"><figcaption class="cap">Homepage today {ev('v')}</figcaption></figure><figure><img src="img/live-offers-m-fold.jpg" alt="Live offers page on a phone" loading="lazy"><figcaption class="cap">Offers page today {ev('v')}</figcaption></figure><figure><img src="img/live-contact-m-fold.jpg" alt="Live contact page on a phone" loading="lazy"><figcaption class="cap">Contact page today {ev('v')}</figcaption></figure>
 <div class="j-phoneside"><h3>As Google reads it</h3><div class="j-gchk">''' + ''.join(f'<div class="gc"><p><b class="{c}">{len(items)}</b>{t}</p><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>' for t, c, items in gchk) + f'''</div></div></div>
 <h3 class="j-h3">As a client experiences it: six people try to book</h3>{grid}
 <p class="cap">✓ works · ~ partly · ✕ missing · ? not verifiable. Tested 11 Oct 2026 {ev('o')}</p>
 <h3 class="j-h3">Web design: before → after</h3>{ba_tabs(BA, 'Web design screens')}
 <div class="j-cards3"><div class="card"><small>If there is no website</small><b>Profile first, site second</b><p>Google Business Profile with priced services and a booking link in week 1; a fast one-page site with WhatsApp booking in week 2; treatment pages after.</p></div>
 <div class="card"><small>First-screen rule</small><b>Ten seconds to decide</b><p>What you're best at, proof (★4.9), why you (open till 10, valet), one way to book.</p></div>
 <div class="card"><small>What I keep</small><b>The brand</b><p>Logo, colours and tone stay. Order, clarity and proof change.</p></div></div>''')

# ---------------- 05 SEO & AEO ----------------
s_seo = sec('seo', 'Search: switched off, then won treatment by treatment.', 'The biggest finding of the audit was one line of code. Then: who owns each search today, and how to take it.',
 f'''<div class="j-code"><pre><code>&lt;!-- ariseandshinesalon.com · homepage source, 11 Oct 2026 --&gt;
&lt;title&gt;ariseandshinesalon.com&lt;/title&gt;
&lt;meta name="robots" content="<mark>noindex, nofollow</mark>"&gt;
&lt;!-- no meta description · no H1 --&gt;
&lt;span class="counter"&gt;0&lt;/span&gt;+ Happy Clients</code></pre>
 <ol class="j-chain"><li><small>Evidence</small>Robots tag says noindex, nofollow</li><li><small>Business impact</small>Prices, offers and services invisible to search</li><li><small>Action</small>Remove the tag, real title, sitemap · day 1</li><li><small>KPI</small>Pages indexed · search impressions</li><li class="rev"><small>Revenue</small>New clients from search at no media cost</li></ol></div>
 <h3 class="j-h3">Who owns each search today</h3>
 <div class="j-serps">
  <div class="card"><small>Brand search</small><b>"arise and shine unisex salon kalyan nagar"</b><p>Returned Spin Salon booking pages and directories. The salon's own site was not returned.</p>{ev('o')}</div>
  <div class="card"><small>"Best" search</small><b>"best unisex salon kalyan nagar bangalore"</b><p>WeddingWire, Salonist, Fresha, magicpin. Platforms own it.</p>{ev('o')}</div>
  <div class="card"><small>Treatment + price</small><b>"hair botox kalyan nagar bangalore price"</b><p>magicpin, a finance cost guide, Fresha. <b>No salon owns it.</b> The price page could.</p>{ev('o')}</div>
 </div>
 {ba_tabs([('serp', 'Google search', 'Search result today vs a treatment page result with price, before/after and booking.'), ('gbp', 'Google profile', 'Business Profile today vs consistent hours, priced services, real photos and a booking link.')], 'Search screens')}
 <div class="two j-two"><div class="panel"><h3>SEO plan</h3><ol class="j-list"><li>Remove noindex, real title and description, Search Console + sitemap</li><li>One name, address, phone and set of hours everywhere</li><li>Six treatment pages: botox, nanoplastia, keratin, colour, nails, bridal, each with price, before/after and stylist</li><li>HairSalon schema, alt text, H1s, fixed dead links</li><li>Business Profile: 20 real photos, weekly posts, priced services</li></ol></div>
 <div class="panel"><h3>AEO &amp; GEO: being the answer in AI search</h3><ol class="j-list"><li>Answer-first treatment pages: price, duration and aftercare in the first lines</li><li>FAQ blocks per treatment from real client questions, with FAQ schema</li><li>Consistent entity details across site, Google, Instagram and directories</li><li>Original facts others can quote: the price ladder, open till 10, valet</li><li>Monthly check of what Google AI, ChatGPT, Gemini and Perplexity say for "best salon Kalyan Nagar" and "hair botox price"</li></ol></div></div>''')

# ---------------- 06 content ----------------
WEEK = [('Mon', 'Before / after', 'Botox, nanoplastia, colour, with the stylist\'s name'), ('Wed', 'Stylist spotlight', 'Adil, Monica, the team: a 30-second intro'),
        ('Fri', 'Weekend slots', 'Real availability: "slots left Sat after 7 pm"'), ('Sat', 'Client reel', 'With consent: the reveal moment'), ('Monthly', 'Offer of the month', 'One hero treatment, the saving shown')]
s_content = sec('content', 'Content that sells chairs, not likes.', 'Reviews name Deepa and Adil. Clients book people. The content plan makes the stylists and the results the brand.',
 '<div class="j-week">' + ''.join(f'<div><small>{d}</small><b>{t}</b><p>{x}</p></div>' for d, t, x in WEEK) + '</div>' +
 f'''<div class="j-cards3"><div class="card"><small>Shot list</small><b>20 real photos</b><p>Street entrance, the second-floor sign, chairs, raised wash area, private pedicure station, team, products.</p></div>
 <div class="card"><small>Instagram profile</small><b>Shop window</b><p>Bio with "Kalyan Nagar · 9am–10pm · valet · ★4.9", highlights for Prices, Botox, Colour, Nails, Team; WhatsApp booking button.</p></div>
 <div class="card"><small>Every post answers</small><b>Who, what, how much</b><p>Stylist, service, price or offer, and how to book. No post without a next step.</p></div></div>
 <p class="j-insight">Instagram activity couldn't be read from public data, so week 1 starts with a 90-day content audit: how many posts show a named stylist, a before/after, a price? {ev('u')}</p>''')

# ---------------- 07 paid ----------------
CAMP = [('Hero treatments', 'Botox, nanoplastia, keratin', 'Reels + Search', 'Bookings of ₹4k+ tickets'), ('Near me · after 7 pm', 'Evening professionals within 3 km', 'Search + Maps', 'The hours rivals don\'t cover'),
        ('Brand defence', 'People searching the salon\'s name', 'Search', 'Own the name while SEO catches up'), ('Men\'s grooming', 'Packages ₹780–1,500', 'Search + Meta, weekday evenings', 'Fill weekday slots'),
        ('Bridal season', 'Pre-bridal packages, Oct–Feb', 'Instagram + WeddingWire', 'High-ticket, long lead time'), ('Win-back', 'Clients 60+ days since last visit', 'WhatsApp + Meta custom audience', 'Cheapest revenue there is')]
s_paid = sec('paid', 'Paid media: designed before, measured after.', 'Ads couldn\'t be verified publicly, so the audit shows what I would run, how it would look, and how spend turns into bookings.',
 f'''<div class="j-ads"><div class="j-phone"><p class="ph-top">Google · "hair botox near me"</p><div class="ad-s"><small>Sponsored</small><p class="u">ariseandshinesalon.com › hair-botox</p><b>Hair Botox in Kalyan Nagar | Davines &amp; Olaplex</b><p>Frizz-free in one sitting. Open till 10 pm, valet parking. ★4.9 on Google.</p><p class="sl">Prices · Before / after · Book a slot</p></div></div>
 <div class="j-phone dark"><p class="ph-top">Instagram reel · 3 km radius</p><div class="ad-r"><small>Sponsored</small><b>"Frizz to glass hair in one sitting"</b><p>Nanoplastia by our stylists · Kalyan Nagar. This month ₹4,999 (list from ₹6,000). Open till 10 pm, valet parking.</p><span class="wa">Send WhatsApp message</span></div></div>
 <div class="j-adnote"><h3>Before → after for ads</h3><dl><div><dt>Before</dt><dd>No landing page per treatment, site noindexed, no pixel or analytics visible. {ev('v')}</dd></div><div><dt>After</dt><dd>One ad per intent, one page per treatment, a tracked WhatsApp link per campaign, bookings counted by source.</dd></div><div><dt>Rule</dt><dd>No ads before the site is indexed and tracking works.</dd></div></dl><p class="cap">Ad concepts use the salon's published prices; every offer confirmed by the owner before it runs. {ev('x')}</p></div></div>
 <h3 class="j-h3">Six campaigns</h3><div class="tw"><table class="j-tbl"><thead><tr><th>Campaign</th><th>Who</th><th>Where</th><th>Why</th></tr></thead><tbody>''' +
 ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in CAMP) + f'''</tbody></table></div>
 <h3 class="j-h3" id="budget">Budget explorer: spend → enquiries → bookings → revenue</h3>
 <div class="j-model"><div class="j-sliders">
  <label>Monthly ad budget <output id="bbO"></output><input type="range" id="bb" min="10000" max="150000" step="5000" value="30000"></label>
  <label>Cost per enquiry <output id="bcO"></output><input type="range" id="bc" min="20" max="250" step="5" value="90"></label>
  <label>Enquiries that become bookings <output id="brO"></output><input type="range" id="br" min="5" max="60" value="25"></label>
  <label>Average first-visit bill <output id="bvO"></output><input type="range" id="bv" min="700" max="6000" step="100" value="2000"></label>
  <label>Clients who come back within 60 days <output id="bkO"></output><input type="range" id="bk" min="0" max="80" value="35"></label>
 </div><div class="j-out" id="bOut"></div></div>
 <p class="cap">Every figure is an adjustable assumption, not a forecast {ev('x')}. For scale: across a 16-location Bengaluru salon network I ran in July 2026, a Google enquiry cost ₹22 and a Meta lead ₹50. A single salon starting fresh pays more at first, so the default here is ₹90. The test budget is the owner's to set; the rule is mine: spend follows booked chairs.</p>''')

# ---------------- 08 booking ----------------
s_book = sec('booking', 'Booking: from an open chat to a confirmed slot.', '"Message us" is not booking. The audit traced what happens between a client\'s first message and the chair.',
 f'''{ba_tabs([('wa', 'WhatsApp booking', 'An open chat to a second number vs service → stylist → slot → confirmation → reminder.')], 'Booking screens')}
 <ol class="j-flow"><li><small>1</small><b>Pick the service</b><p>Haircut, frizz-free, colour, nails, bridal</p></li><li><small>2</small><b>Pick the stylist</b><p>Named, with a photo</p></li><li><small>3</small><b>Pick the slot</b><p>Real availability, evenings shown</p></li><li><small>4</small><b>Confirmed</b><p>"Sat 4:30 pm · Hair spa · Monica ✓"</p></li><li><small>5</small><b>Reminder</b><p>Day before, with the valet note</p></li><li class="rev"><small>6</small><b>Rebooked</b><p>At the counter, before they leave</p></li></ol>
 <div class="j-cards4"><div class="card"><small>Today</small><b class="leak">2 numbers</b><p>Header 081237 29873; WhatsApp 090352 44813. {ev('v')}</p></div><div class="card"><small>Today</small><b class="leak">3 sets of hours</b><p>9–10 (Google), 10–8 (FAQ), "10.00–9.00" (site). {ev('v')}</p></div><div class="card"><small>Measure</small><b>Enquiry → booked %</b><p>Plus reply time, no-shows and bookings by day and hour.</p></div><div class="card"><small>Appointment impact</small><b>Fill empty weekday slots first</b><p>They cost nothing to sell. Chair utilisation by hour shows where.</p></div></div>''')

# ---------------- 09 journey ----------------
J = [('Discovery', '"Good salon near me?"', 'Google listing only; site noindexed', 'Website can\'t be found', 'l', 'Indexed treatment pages + strong Maps profile', 'Search &amp; Maps views'),
     ('First look', '"Is it nice? Is it pricey?"', 'Generic hero, "0 +" counters', 'Premium room not shown', 'l', 'The room, the brands, ★4.9, "open till 10"', 'Profile → site clicks'),
     ('Consideration', '"Who\'ll do it? Will it suit me?"', 'Prices yes; no stylists, no before/after', 'Leaves to compare on Instagram', 'l', 'Before/after + stylist + price per treatment', 'Page → enquiry %'),
     ('Enquiry', '"Let me just message"', 'WhatsApp + 2 numbers', 'Which number? Which hours?', 'l', 'One number, one WhatsApp, same hours everywhere', 'Chats &amp; calls by source'),
     ('Booking', '"Saturday 7 pm?"', 'Back-and-forth chat', 'Reply time unknown', 'm', 'Service, stylist, slot, confirmed instantly', 'Enquiry → booked %'),
     ('Reminder', '"Don\'t let me forget"', 'Not visible', 'No-shows likely untracked', 'm', 'WhatsApp reminder + valet note', 'No-show %'),
     ('Visit', '"Treat me well"', 'Valet, tea, premium space', 'Strength', 'o', 'Keep; add a 2-minute consultation', 'Wait time'),
     ('Upgrade', '"What else should I do?"', 'Offers exist', 'Consultation not visible', 'm', 'Stylist recommends the right treatment', 'Ticket size'),
     ('Review', '"That was great"', '35 reviews', 'Most happy clients never asked', 'l', 'Thank-you message with review link', 'Reviews / month'),
     ('Rebook', '"I\'ll come back… sometime"', 'No reminder or membership seen', 'Clients drift to the next salon', 'l', 'Booked at the counter + reminder at the right interval', '60-day return rate')]
s_jour = sec('journey', 'Ten steps from "I need a cut" to "I\'ll be back".', 'Each step: what the client thinks, what happens today, where it leaks, what changes, and the number that proves it.',
 '<ol class="j-journey">' + ''.join(f'<li class="s-{lv}"><span class="jnum">{i + 1:02d}</span><div class="jtitle"><b>{st}</b><em>{th}</em></div><div><small>Today</small><p>{td}</p></div><div><small>Leak</small><p>{lk}</p></div><div><small>Better version</small><p>{bt}</p></div><div><small>Measure</small><p>{ms}</p></div></li>' for i, (st, th, td, lk, lv, bt, ms) in enumerate(J)) +
 f'</ol><p class="cap"><span class="j-key l"></span>visible leak {ev("v")} <span class="j-key m"></span>likely leak {ev("i")} <span class="j-key o"></span>strength (from reviews)</p>')

# ---------------- 10 choosing ----------------
ACT = [  # n, action, impact 1-5, effort 1-5, phase, priority
 (1, 'Remove noindex, title, Search Console', 5, 1, 1, 'P1'), (2, 'One number, address, hours', 4.3, 1.0, 1, 'P1'), (3, 'Fix the homepage', 4.4, 2.3, 1, 'P1'),
 (4, 'Review engine', 3.8, 1.4, 1, 'P1'), (5, 'Tracking + "how did you hear"', 4.1, 1.9, 1, 'P1'), (6, 'Treatment pages', 5, 3, 2, 'P1'),
 (7, 'Google profile: photos, posts, services', 3.7, 2.2, 2, 'P1'), (8, 'One booking flow', 4.5, 3.2, 2, 'P1'), (9, 'Instagram rhythm', 3, 3, 2, 'P2'),
 (10, 'Ads test: hero treatments, after 7 pm', 3.5, 3, 2, 'P2'), (11, 'Rebooking reminders', 4.6, 2.6, 3, 'P1'), (12, 'Membership / prepaid card', 3.6, 3.4, 3, 'P2'),
 (13, 'Refer-a-friend + win-back', 3, 2, 3, 'P2'), (14, 'Monthly growth report', 3.4, 1.2, 3, 'P1')]
data['acts'] = [{'n': n, 't': t, 'i': i, 'f': f, 'p': p, 'pr': pr} for n, t, i, f, p, pr in ACT]
BIG = [('Biggest leak', 'A website Google is told to skip'), ('Biggest threat', 'Adorn &amp; Admire, 360 m, 3,580 reviews'), ('Biggest revenue lever', 'Clients who come back every 5–8 weeks'),
       ('Biggest quick win', 'Untick one setting · day 1'), ('Long-term play', 'Stylists as the brand on Instagram'), ('What I would not do', 'Buy reviews · deep discounting · ads before the site is indexed')]
s_choose = sec('choose', 'Choosing what to fix, and in what order.', 'Everything found is scored on impact and effort. Cheap fixes that unblock revenue go first; anything that needs the site visible waits until it is.',
 f'''<div class="charts"><div class="panel"><h3>Priority matrix: 14 actions</h3><div class="chart" id="c-matrix"></div><p class="cap">Hover a dot. Numbers match the 90-day plan {ev('i')}</p></div>
 <div class="panel"><h3>Today's scorecard, from public evidence</h3><div class="chart" id="c-score"></div><p class="cap">Scored 1–5. Instagram, paid media and retention can't be scored without the salon's data {ev('u')}</p></div></div>
 <div class="j-big">''' + ''.join(f'<div><small>{a}</small><b>{b}</b></div>' for a, b in BIG) + '</div>')

# ---------------- 11 layers ----------------
LAY = [('pre', 'Pre-marketing', 'Fix the foundation. Marketing on a broken base wastes money.', ['Remove noindex, real title', 'One phone number, address, hours', 'Consistent prices; no duplicate packages', 'Tracking and "how did you hear"', 'Booking flow that confirms']),
       ('mkt', 'Marketing', 'Create and capture demand, then convert it.', ['Treatment pages, SEO, AEO', 'Google profile, review engine', 'Instagram rhythm, stylists as brand', 'Ads: hero treatments, after 7 pm, bridal', 'WhatsApp reminders and win-back']),
       ('ops', 'The salon floor', 'What only the business can do. Marketing can support it, not replace it.', ['Rebook at the counter', '2-minute consultation in the chair', 'Membership terms and pricing', 'Service quality and wait time', 'Staffing the evening slots'])]
s_layers = sec('layers', 'What marketing can move, and what it can\'t.', 'Three layers. Pre-marketing fixes come first; marketing creates and converts demand; the salon floor turns visits into regulars. In the model, marketing alone moves roughly 45–75% of the growth.',
 '<div class="j-layers">' + ''.join(f'<div class="ly ly-{k}"><small>Layer {i + 1}</small><h3>{t}</h3><p>{d}</p><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>' for i, (k, t, d, items) in enumerate(LAY)) + '</div>' +
 f'''<h3 class="j-h3">How much of the growth is marketing's? Set it yourself.</h3>
 <div class="j-model"><div class="j-sliders">
  <p class="cap">The growth in the revenue model (next stage) splits across four levers. New clients are marketing's. The other three are shared. Set marketing's share of each:</p>
  <label>Return rate: marketing's share <output id="aRo"></output><input type="range" id="aR" min="0" max="100" step="5" value="60"></label>
  <label>Visits a year: marketing's share <output id="aVo"></output><input type="range" id="aV" min="0" max="100" step="5" value="50"></label>
  <label>Average bill: marketing's share <output id="aBo"></output><input type="range" id="aB" min="0" max="100" step="5" value="20"></label>
  <div class="j-presets"><button type="button" data-pre="low">Cautious</button><button type="button" data-pre="mid">Middle</button><button type="button" data-pre="high">Generous</button></div>
 </div><div class="j-out" id="aOut"></div></div>
 <p class="cap">Lever shares come from a Shapley split of the illustrative model below: new clients 27%, return rate 31%, visits a year 29%, average bill 13% of the uplift. The marketing share is an assumption you set {ev('x')}</p>''')

# ---------------- 12 revenue ----------------
RET = [("Men's haircut", 3, 5), ("Women's haircut", 6, 10), ('Gel / nail refills', 2, 3), ('Root touch-up / colour', 5, 8), ('Hair spa', 4, 6), ('Botox / nanoplastia / keratin', 12, 20)]
data['ret'] = [{'label': a, 'a': b, 'b': c} for a, b, c in RET]
s_rev = sec('revenue', 'From growth to retention to revenue.', 'Salons grow on the second visit. Revenue = new clients × return rate × visits a year × average bill. Small moves in each multiply.',
 f'''<div class="charts"><div class="panel wide"><h3>When each client should come back</h3><div class="chart" id="c-ret"></div><p class="cap">Industry rule of thumb, to be set with the stylists. This is when each reminder goes out.</p></div></div>
 <div class="j-model"><div class="j-sliders">
  <label>New clients a month <output id="m1O"></output><input type="range" id="m1" min="20" max="200" value="60"></label>
  <label>Come back within 60 days <output id="m2O"></output><input type="range" id="m2" min="10" max="80" value="35"></label>
  <label>Visits a year (returners) <output id="m3O"></output><input type="range" id="m3" min="2" max="12" value="6"></label>
  <label>Average bill <output id="m4O"></output><input type="range" id="m4" min="800" max="5000" step="100" value="1800"></label>
  <div class="j-presets"><button type="button" data-rv="today">Today (assumed)</button><button type="button" data-rv="after">After fixes (assumed)</button></div>
 </div><div class="j-out" id="mOut"></div></div>
 <div class="charts"><div class="panel"><h3>Where the ×2.3 comes from</h3><div class="chart" id="c-shap"></div><p class="cap">Today 60 / 35% / 6 / ₹1,800 → after 75 / 50% / 8 / ₹2,000: ₹3.0 L → ₹6.8 L yearly value of one month's new clients. Every input invented for arithmetic only, not Arise &amp; Shine data {ev('x')}</p></div>
 <div class="panel"><h3>To make it real, I'd need</h3><ul class="j-checks"><li><b>New vs returning</b> clients per month, from billing</li><li><b>Average bill</b> by service and stylist</li><li><b>Chair utilisation</b> by day and hour</li><li><b>No-shows</b> and late cancellations</li><li><b>Where clients heard</b> of you, asked for 30 days</li><li><b>Marketing spend</b> and any platform fees</li></ul></div></div>''')

# ---------------- 13 plan ----------------
s_plan = sec('plan', 'The 90-day plan: switch on, win the street, fill the diary.', 'Fourteen actions in three phases, each with the KPI that proves it.',
 f'''<div class="panel"><div class="chart" id="c-gantt"></div><p class="cap">P1 = do first. Phases: weeks 1–4, 5–8, 9–12.</p></div>
 <div class="j-phases"><div><small>Weeks 1–4</small><b>Switch on</b><p>You see: the site in Google, reviews growing, first numbers.</p></div><div><small>Weeks 5–8</small><b>Win the street</b><p>You see: bookings by source, cost per booking.</p></div><div><small>Weeks 9–12</small><b>Fill the diary</b><p>You see: return rate, members, revenue by channel.</p></div></div>''')

# ---------------- 14 monthly ----------------
PAGES = [('Page 1', 'The month', 'Sales and marketing together', ['Revenue vs target and vs last year', 'Bills, new vs returning clients', 'Average bill by service', 'Bookings by source (Google, Maps, Instagram, WhatsApp, walk-in, referral)', 'Marketing spend, cost per booking, revenue per ₹ spent', 'Reviews this month, rating']),
         ('Page 2', 'The year', 'Is the trend real?', ['Revenue and bills, month by month vs last year', 'Return rate within 60 days, by month', 'Search impressions and profile actions', 'Spend vs bookings, month by month']),
         ('Page 3', 'The breakdowns', 'Where to act next', ['By service: volume, ticket, growth', 'By stylist: bookings, rebook %, reviews named', 'By channel: cost per booking, booking rate', 'By day and hour: empty chairs to fill'])]
RULES = [('Scale', 'Cost per booking under target and bookings rising', 'flow'), ('Hold', 'On target; not enough data to move', 'move'), ('Fix', 'Clicks fine, bookings not: the page or the desk', 'est'), ('Cut', 'No bookings after a fair test', 'leak')]
s_month = sec('monthly', 'Every month: what I read, in what order, and what I decide.', 'The report reads the month first (sales and marketing), then the year, then the breakdowns. Every number has a source and a label.',
 '<div class="j-pages">' + ''.join(f'<div class="card"><small>{a}</small><h3>{b}</h3><p class="cap">{c}</p><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul></div>' for a, b, c, items in PAGES) + '</div>' +
 '<h3 class="j-h3">Every month, each campaign gets a verdict</h3><div class="j-rules">' + ''.join(f'<div class="r-{c}"><b>{a}</b><p>{b}</p></div>' for a, b, c in RULES) + '</div>' +
 '<div class="j-cards3"><div class="card"><small>Data sources</small><b>Joined, not guessed</b><p>Billing/POS export, Google Ads, Meta, GA4, Search Console, Business Profile, WhatsApp click tracking, the counter question.</p></div><div class="card"><small>Scoreboard</small><b>Four numbers</b><p>Reviews a month · bookings by source · 60-day return rate · revenue by channel.</p></div><div class="card"><small>A real example</small><b>Monthly salon report</b><p>The format I used for a 16-salon network: <a href="https://dannygrowthmarketing.github.io/toniguy-august-2026-report/">August 2026 report →</a></p></div></div>')

# ---------------- 15 data control ----------------
LABELS = [('v', 'Read directly from a public source on a date'), ('o', 'Seen when tested; may change'), ('i', 'A reasoned conclusion, not a fact'), ('u', 'Needs the business\'s data or access'), ('x', 'Hypothetical example, never the client\'s numbers'), ('r', 'Redrawn from live content, not a screenshot')]
s_data = sec('data', 'Data control: nothing enters a report without a source.', 'The audit uses six evidence labels. Reports after the contract use the same discipline with the client\'s own data.',
 '<div class="j-labels">' + ''.join(f'<div>{ev(k)}<p>{d}</p></div>' for k, d in LABELS) + '</div>' +
 '''<div class="two j-two"><div class="panel"><h3>Rules I work by</h3><ol class="j-list"><li>Every number has a source and a date.</li><li>Platform numbers are checked against billing before they are believed.</li><li>Where data doesn't exist, the report says so; nothing is filled in.</li><li>Models are labelled illustrative and every input is adjustable.</li><li>The client owns every account; I work as a user.</li></ol></div>
 <div class="panel"><h3>Tracking I set up in month 1</h3><ul class="j-checks"><li><b>GA4</b> events: WhatsApp click, call click, booking started, booking confirmed</li><li><b>Search Console</b> indexing, queries, pages</li><li><b>Tagged links</b> one WhatsApp link per campaign and channel</li><li><b>Counter question</b> "how did you hear of us?" for 30 days</li><li><b>One sheet</b> bookings, source, service, stylist, bill, returned?</li></ul></div></div>
 <p class="cap">Limits of this audit: no internal data. Client numbers, revenue, spend and booking rates are not claimed. Instagram, the Meta Ad Library and Google profile photos couldn't be read automatically and are marked Unknown.</p>''')

# ---------------- 16 AI ----------------
AI = [('Market research', 'Gemini · Perplexity · Claude', 'Pull every salon in 1.5 km, hours, ratings, review samples; summarise what reviews praise', 'Which rivals matter and why'),
      ('Website audit', 'Claude · ChatGPT', 'Read page source, list SEO issues, test six client journeys, find contradictions in prices and hours', 'What to fix first'),
      ('Audience &amp; offers', 'ChatGPT · Claude', 'Group review language and the price ladder into segments and hooks', 'Who to win, who to skip'),
      ('Design', 'Claude · ComfyUI / Krea', 'Before/after screens, ad concepts, image concepts', 'What ships and what stays the brand'),
      ('Build', 'Claude · Antigravity · GitHub', 'Proposal site, pages, charts, models', 'Final copy and every claim'),
      ('Automation', 'n8n · GitHub Models', 'Reminders, win-back, lead routing, report pulls', 'Rules, timing, tone'),
      ('Reporting', 'Claude · ChatGPT', 'Join exports, draft the monthly read, check numbers against billing', 'The verdict: scale, hold, fix, cut')]
s_ai = sec('ai', 'AI in every stage. Judgement in every decision.', 'I use several AI tools as an execution layer. They speed up research, analysis, design and build. They never pick the strategy or sign off a number.',
 '<div class="tw"><table class="j-tbl j-ai"><thead><tr><th>Stage</th><th>Tools</th><th>What AI does</th><th>What I decide</th></tr></thead><tbody>' +
 ''.join(f'<tr><th scope="row">{a}</th><td><span class="chip">{b}</span></td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in AI) + '</tbody></table></div>' +
 '<div class="j-cards3"><div class="card"><small>Speed</small><b>Two days, not two weeks</b><p>The Arise &amp; Shine audit, 27 pages with a 17-salon map, was researched and built in two days after the first visit.</p></div><div class="card"><small>Checks</small><b>Every claim verified</b><p>AI output is checked against the source and labelled before it reaches a client.</p></div><div class="card"><small>Never</small><b>No invented numbers</b><p>Where evidence stops, the page says "Unknown" or "Illustrative".</p></div></div>')

# ---------------- 17 proof ----------------
PROOF = [('Market research', 'Gold Coins Resort', 'Joined 6 sources; bookings fell on sales conversion (24% → 14%), not on ads', 'resort.html'),
         ('Web &amp; booking', 'TONI&amp;GUY Bangalore', 'Site moved to Netlify, booking app built; revenue +14.7% on last year from March', 'toni-and-guy.html'),
         ('SEO', 'Foremost Public Adjusters', '19 crawl issues fixed, 24 pages rewritten, 140 keywords mapped', 'foremost-pa.html'),
         ('Local / Google profile', 'Elites Dental Care', '300 stuffed profile services cut to 121, tracked booking link', 'elites-dental.html'),
         ('Paid media', 'MR Jewels', 'Showroom cost per click ₹38.60 → ₹13.13 after one goal fix', 'mr-jewels.html'),
         ('Content &amp; scale', 'EveryWatch', 'Monthly new users 9,113 → 182,782 in 17 months', 'everywatch.html'),
         ('No web presence', 'Swift Restoration', '0 service or location pages; pages planned before ad spend', 'swift-restoration.html')]
s_proof = sec('proof', 'Each stage, done before for a real business.', 'This journey combines what I did across seven projects. Each stage links to the case where it happened.',
 '<div class="j-proof">' + ''.join(f'<a class="card" href="https://dannygrowthmarketing.github.io/revenue-casebook/{u}"><small>{a}</small><b>{b}</b><p>{c}</p><span>Open the case →</span></a>' for a, b, c, u in PROOF) + '</div>')

# ---------------- 18 QA ----------------
total = sum(len(x[1]) for x in QA)
qa_btn = '<button type="button" data-f="all" aria-pressed="true">All <span>' + str(total) + '</span></button>' + ''.join(f'<button type="button" data-f="{i}" aria-pressed="false">{g} <span>{len(items)}</span></button>' for i, (g, items) in enumerate(QA))
qa_items = ''.join(f'<details class="j-q" data-g="{i}"><summary><small>{g}</small>{e(q)}</summary><p>{e(a)}</p></details>' for i, (g, items) in enumerate(QA) for q, a in items)
s_qa = sec('qa', f'{total} questions owners and teams ask, and how I answer.', 'From "why should we let you audit us?" to "what if it doesn\'t work?". Search or filter by stage.',
 f'<div class="j-qa"><input class="j-qs" type="search" placeholder="Search: ads, booking, AI, budget, reviews…" aria-label="Search questions"><p class="cap"><b id="qn">{total}</b> shown</p><div class="fchips j-qf" role="group" aria-label="Filter questions">{qa_btn}</div><div class="j-ql">{qa_items}</div><p class="j-qe cap" hidden>No question matches.</p></div>')
faq_ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for g, items in QA for q, a in items]}, ensure_ascii=False)

# ---------------- 19 docs ----------------
s_docs = sec('docs', 'The reference documents.', 'Everything this journey is built from, in the form the prospect received it.',
 '''<div class="j-docs"><a class="card" href="docs/arise-shine-growth-audit.pdf"><small>PDF · 27 pages</small><b>Growth Audit &amp; Proposal</b><p>Website, pricing, Google profile, 17-salon competition, journey, retention, revenue model, 30/60/90 plan, scorecard.</p><span>Open →</span></a>
 <a class="card" href="docs/arise-shine-marketing-psychology-playbook.pdf"><small>PDF</small><b>Marketing Psychology Playbook</b><p>60 concepts applied to the salon, each with where to use it and the honest limit.</p><span>Open →</span></a>
 <a class="card" href="https://dannygrowthmarketing.github.io/arise-shine-growth-plan/"><small>Live site</small><b>Interactive proposal</b><p>Real before/after screenshots, budget and revenue models, new-branch playbook.</p><span>Open →</span></a>
 <a class="card" href="https://dannygrowthmarketing.github.io/revenue-casebook/"><small>Live site</small><b>Revenue Casebook</b><p>Seven businesses traced from first search to the till, every number labelled.</p><span>Open →</span></a></div>''')

cta = '''<section class="band ctab" id="contact"><div class="wrap"><div><p class="eyebrow">Work with me</p><h2>Want this journey run on your business?</h2><p>Send me your website and city. The first pass uses public data only, and you'll see what I'd fix first.</p></div>
<div class="acts"><span class="copybox"><span>danieldeepak3519@gmail.com</span><button type="button" data-copy="danieldeepak3519@gmail.com">Copy</button></span><a class="btn ghost" href="https://linkedin.com/in/danny-ai-marketing">LinkedIn</a><a class="btn ghost" href="https://dannygrowthmarketing.github.io/revenue-casebook/">Casebook</a></div></div></section>'''

head = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>How I audit · from first conversation to revenue · Danny Deepak</title>
<meta name="description" content="Danny Deepak's audit method, run end to end on a real prospect: market research, audience, web design, SEO and AEO, content, paid media, booking, retention, monthly data, budget and revenue.">
<meta property="og:title" content="How I audit · from first conversation to revenue"><meta property="og:description" content="One real prospect, end to end: every stage of the audit, what it found, and how each fix reaches revenue.">
<meta name="theme-color" content="#0C1222"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/base.css"><link rel="stylesheet" href="assets/journey.css">
<script type="application/ld+json">{faq_ld}</script></head>'''
top = '''<header class="top"><div class="wrap"><a class="brand" href="https://dannygrowthmarketing.github.io/revenue-casebook/"><i></i>Danny Deepak</a><nav class="nav" aria-label="Main"><a href="https://dannygrowthmarketing.github.io/revenue-casebook/#cases">Cases</a><a href="#qa" class="hide-sm">Questions</a><a href="#docs" class="hide-sm">Documents</a><a class="cta" href="#contact">Contact</a></nav></div></header>'''
foot = f'''<footer class="foot"><div class="wrap"><span>© 2026 Daniel Deepak · Bengaluru · Growth &amp; revenue consulting</span><span>Example: Arise &amp; Shine Unisex Salon, proposal stage, built from public data checked 11–12 Oct 2026. Not a client result.</span></div></footer>'''
body = ('<body>' + top + '<main>' + hero + nav + s_ask + s_market + s_aud + s_web + s_seo + s_content + s_paid + s_book + s_jour + s_choose + s_layers + s_rev + s_plan + s_month + s_data + s_ai + s_proof + s_qa + s_docs + '</main>' + cta + foot +
        f'<script>window.J={json.dumps(data, ensure_ascii=False)};</script><script src="assets/kit.js"></script><script src="assets/journey.js"></script></body></html>')
open(OUT, 'w').write(head + body)
print('ok', len(head + body), 'questions', total)
