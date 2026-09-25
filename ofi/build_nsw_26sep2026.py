#!/usr/bin/env python3
"""Build the Saturday 26 September 2026 OFI email — Lower North Shore, Southern Highlands, Byron Bay.

Source template: template_Property_Campaign_Weekly_OFI.html (Stripo export).
Data: Notion MASTER Property Marketing Database, Date = 2026-09-26 (Brisbane excluded).
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = glob.glob('/root/.claude/skills/**/atlas-email/scripts', recursive=True)
sys.path.insert(0, SKILL[0] if SKILL else HERE)
from xhtml_pass import xhtml_pass

DATE = '26sep2026'
DAY = 'Saturday'
TITLE = '26 September Weekly OFI Email'
CDN = ('https://imagesv1.asteroidcdn.com/___imageconnV2/eyJ1IjoiaHR0cHM6Ly9hZ2VudGJveGNkbi5jb20uYXUvIiwiZSI6MzE1MzYwMDAwMH0.'
       '7vD7u29jibRAITaQ9rp6xQP_aV3PNNwnIiXc_xsiNP0/clients-data/26319/public_html/media/lt/1/')
OFFICE = {'lns': 'N0c5XYyhTX2LH2o7pcWCGQ', 'sth': 'cgmYO6KbRWmUGd4EXAMmTQ', 'byb': 'eBJrsZ7fQgy8xQweUgV2ng'}
INSPECTIONS = 'https://www.atlas.com.au/upcoming-inspections?queryType=inspection&forType=sale&office={}&sort=earliestInspectionDateTime_ASC&page=1'
BYRON_TILE_IMG = ('https://www.datocms-assets.com/190151/1782283165-shutterstock_1940576656.jpg'
                  '?fm=jpg&w=530&h=170&fit=crop&crop=focalpoint&fp-y=0.55')

# street, suburb, bed, bath, car, start, end, id, slug, image (after CDN prefix)
# bed as a string -> used verbatim as the spec line (land size etc). car '-' -> CAR dropped.
LNS = [
    ('3/7 Warringah Road', 'Mosman', 3, 2, '2', '09:00', '09:30', '1P11088', '3-7-warringah-road-mosman-nsw-1p110883', '1P11088/178695921520668526-rsd.jpg'),
    ('2304/168 Walker Street', 'North Sydney', 4, 3, '2', '09:00', '09:30', '1P11127', '2304-168-walker-street-north-sydney-nsw-1p111273', '1P11127/178658708409866867-rsd.jpg'),
    ('18 Baringa Road', 'Northbridge', '5 BED &nbsp;5 BATH &nbsp;2 CAR &nbsp;645SQM', None, '-', '09:30', '10:00', '1P11269', '18-baringa-road-northbridge-nsw-1p112693', '1P11269/1790144099719818097878657-rsd.jpg'),
    ('201/171-179 Avenue Road', 'Mosman', 2, 2, '2', '09:45', '10:15', '1P10076', '201-171-179-avenue-road-mosman-nsw-1p100763', '1P10076/1788417897827688437238296-rsd.jpg'),
    ('26 Kirkoswald Avenue', 'Mosman', 4, 3, '2', '10:00', '10:30', '1P9267', '26-kirkoswald-avenue-mosman-nsw-1p92673', '1P9267/177016557964902528-rsd.jpg'),
    ('34 Willowie Road', 'Castle Cove', 5, 5, '4', '10:30', '11:00', '1P11087', '34-willowie-road-castle-cove-nsw-1p110873', '1P11087/1788245496747925967281019-rsd.jpg'),
    ('1/155 Middle Head Road', 'Mosman', 2, 2, '1', '10:30', '11:00', '1P10972', '1-155-middle-head-road-mosman-nsw-1p109723', '1P10972/1776298468829469855841918-rsd.jpg'),
    ('21 Hopetoun Avenue', 'Mosman', 5, 5, '4', '10:45', '11:15', '1P11277', '21-hopetoun-avenue-mosman-nsw-1p112773', '1P11277/178830458362255028-rsd.jpg'),
    ('18 Stanton Road', 'Mosman', 5, 3, '-', '11:00', '11:30', '1P11264', '18-stanton-road-mosman-nsw-1p112643', '1P11264/178823596185497936-rsd.jpg'),
    ('2 Lodge Road', 'Cremorne', 4, 3, '2', '11:00', '11:30', '1P11177', '2-lodge-road-cremorne-nsw-1p111773', '1P11177/178728006760021954-rsd.jpg'),
    ('20 Stanton Road', 'Mosman', '763SQM', None, '-', '11:00', '11:30', '1P11239', '20-stanton-road-mosman-nsw-1p112393', '1P11239/178831389698827247-rsd.jpg'),
    ('16 Redan Street', 'Mosman', 4, 4, '2', '11:15', '11:45', '1P10981', '16-redan-street-mosman-nsw-1p109813', '1P10981/178832618570662508-rsd.jpg'),
    ('9 Sirius Avenue', 'Mosman', 5, 6, '4', '11:45', '12:15', '1P8796', '9-sirius-avenue-mosman-nsw-1p87963', '1P8796/1770768943159263626307684-rsd.jpg'),
    ('73 Minimbah Road', 'Northbridge', 4, 2, '2', '11:45', '12:15', '1P10268', '73-minimbah-road-northbridge-nsw-1p102683', '1P10268/1771925121410736862587853-rsd.jpg'),
    ('5 Churchill Crescent', 'Cammeray', 5, 3, '4', '11:45', '12:15', '1P10469', '5-churchill-crescent-cammeray-nsw-1p104693', '1P10469/178660470842838282-rsd.jpg'),
    ('106 Raglan Street', 'Mosman', 4, 2, '1', '12:00', '12:30', '1P11002', '106-raglan-street-mosman-nsw-1p110023', '1P11002/178651521967437178-rsd.jpg'),
    ('8 Prince Albert Street', 'Mosman', 6, 5, '4', '12:30', '13:00', '1P10388', '8-prince-albert-street-mosman-nsw-1p103883', '1P10388/178649565094760368-rsd.jpg'),
    ('42 Jeffreys Street', 'Kirribilli', 4, 4, '-', '12:45', '13:15', '1P11051', '42-jeffreys-street-kirribilli-nsw-1p110513', '1P11051/178581991527892270-rsd.jpg'),
    ('4D/46-48 Muston Street', 'Mosman', 3, 2, '2', '13:00', '13:30', '1P10692', '4d-46-48-muston-street-mosman-nsw-1p106923', '1P10692/178530983874451256-rsd.jpg'),
    ('2a Cross Street', 'Mosman', 5, 5, '4', '13:00', '13:30', '1P11251', '2a-cross-street-mosman-nsw-1p112513', '1P11251/178823760909918252-rsd.jpg'),
    ('1 Buena Vista Avenue', 'Mosman', 6, 3, '4', '13:30', '14:00', '1P10213', '1-buena-vista-avenue-mosman-nsw-1p102133', '1P10213/178780873615940024-rsd.jpg'),
    ('23A Kardinia Road', 'Mosman', 5, 4, '4', '14:00', '14:30', '1P10386', '23a-kardinia-road-mosman-nsw-1p103863', '1P10386/177561411354182210-rsd.jpg'),
    ('6 Coolawin Road', 'Northbridge', 5, 4, '2', '14:45', '15:15', '1P10600', '6-coolawin-road-northbridge-nsw-1p106003', '1P10600/178640430559003465-rsd.jpg'),
]
STH = [
    ('8 College Place', 'Bowral', 4, 2, '1', '09:00', '09:30', '1P11201', '8-college-place-bowral-nsw-1p112013', '1P11201/178944362065324957-rsd.jpg'),
    ('1A Burradoo Road', 'Burradoo', 4, 2, '2', '10:00', '10:30', '1P11161', '1a-burradoo-road-burradoo-nsw-1p111613', '1P11161/178901997231221643-rsd.jpg'),
    ('15 Middle Road', 'Exeter', 3, 2, '1', '10:00', '10:30', '1P11148', '15-middle-road-exeter-nsw-1p111483', '1P11148/178401206647354877-rsd.jpg'),
    ('34 Victoria Street', 'Bowral', 4, 3, '2', '10:00', '10:30', '1P11055', '34-victoria-street-bowral-nsw-1p110553', '1P11055/178951578066831096-rsd.jpg'),
    ('19 Elm Street', 'Bowral', 4, 2, '1', '11:00', '11:30', '1P11044', '19-elm-street-bowral-nsw-1p110443', '1P11044/178720339700508756-rsd.jpg'),
    ('60 Lytton Road', 'Moss Vale', 3, 1, '-', '11:00', '11:30', '1P11139', '60-lytton-road-moss-vale-nsw-1p111393', '1P11139/178409496970148247-rsd.jpg'),
    ('11/18 Kangaloon Road', 'Bowral', 4, 3, '2', '11:00', '11:30', '1P11116', '11-18-kangaloon-road-bowral-nsw-1p111163', '1P11116/178660224473443223-rsd.jpg'),
    ('17 Gibraltar Road', 'Bowral', 4, 2, '2', '11:00', '11:30', '1P11208', '17-gibraltar-road-bowral-nsw-1p112083', '1P11208/178588978627706012-rsd.jpg'),
    ('3 Centennial Road', 'Bowral', 4, 2, '2', '12:00', '12:30', '1P11199', '3-centennial-road-bowral-nsw-1p111993', '1P11199/178658406718052571-rsd.jpg'),
    ('6 Kimberley Drive', 'Bowral', 6, 3, '2', '12:00', '12:30', '1P11151', '6-kimberley-drive-bowral-nsw-1p111513', '1P11151/178400484355107746-rsd.jpg'),
    ('16 Gibraltar Road', 'Bowral', 4, 3, '6', '12:00', '12:30', '1P10828', '16-gibraltar-road-bowral-nsw-1p108283', '1P10828/178330217295919559-rsd.jpg'),
    ('127 Bowral Street', 'Bowral', 3, 2, '2', '12:00', '12:30', '1P11241', '127-bowral-street-bowral-nsw-1p112413', '1P11241/178901923559341011-rsd.jpg'),
    ('19 Eliza Street', 'Moss Vale', 4, 2, '2', '12:30', '13:00', '1P11290', '19-eliza-street-moss-vale-nsw-1p112903', '1P11290/179012125056476297-rsd.jpg'),
    ('13 Clearview Street', 'Bowral', 3, 2, '1', '13:00', '13:30', '1P11054', '13-clearview-street-bowral-nsw-1p110543', '1P11054/178183010248293621-rsd.jpg'),
    ('112-116 Shepherd Street', 'Bowral', 3, 3, '3', '13:00', '13:30', '1P10756', '112-116-shepherd-street-bowral-nsw-1p107563', '1P10756/177914942199525437-rsd.jpg'),
    ('28 Windeyer Street', 'Renwick', 4, 2, '2', '14:00', '14:30', '1P10714', '28-windeyer-street-renwick-nsw-1p107143', '1P10714/178833176841335493-rsd.jpg'),
    ('11 Lavis Road', 'Bowral', 4, 2, '2', '14:00', '14:30', '1P10300', '11-lavis-road-bowral-nsw-1p103003', '1P10300/178901177726689110-rsd.jpg'),
]
BYB = [
    ('296 Tyagarah Road', 'Myocum', 3, 3, '3', '12:00', '12:30', '1P9718', '296-tyagarah-road-myocum-nsw-1p97183', '1P9718/178901845684490376-rsd.jpg'),
]


def t12(hhmm):
    h, m = map(int, hhmm.split(':'))
    return f"{(h - 1) % 12 + 1}:{m:02d}{'am' if h < 12 else 'pm'}"


def specs(bed, bath, car):
    if isinstance(bed, str):
        return bed
    s = f'{bed} BED &nbsp;{bath} BATH'
    return s + (f' &nbsp;{car} CAR' if car.strip() not in ('', '-', '0') else '')


def one(pattern, repl, s, count=1):
    new, n = re.subn(pattern, repl, s, count=count)
    assert n == count, f'expected {count} match(es) for {pattern!r}, got {n}'
    return new


def tr_end(d, i):
    depth = 0
    for m in re.finditer(r'<tr[\s>]|</tr>', d[i:]):
        depth += -1 if m.group().startswith('</') else 1
        if depth == 0:
            return i + m.end()
    raise ValueError('unbalanced <tr>')


def balanced(seg):
    return seg.count('<table') == seg.count('</table>') and seg.count('<tr') == seg.count('</tr>')


CARD_RE = re.compile(
    r'(<a target="_blank" href=")https://www\.atlas\.com\.au/property/[^"]+(".*?<img[^>]*?src=")[^"]+(".*?font-size:18px">)[^<]+'
    r'(</p>.*?font-size:11px">)[^<]+(</p>.*?font-size:11px">)[^<]*(</p>.*?OPEN INSPECTION</strong></p>.*?font-size:12px">)[^<]+(</p>)',
    re.S)


def fill_cards(html, cards, region):
    it = iter(cards)

    def f(m):
        street, suburb, bed, bath, car, s, e, pid, slug, img = next(it)
        href = (f'https://www.atlas.com.au/property/{slug}?utm_source=ofi_edm&utm_medium=email'
                f'&utm_campaign=weekly_ofi_{region}_{DATE}&utm_content={pid}')
        return (m.group(1) + href + m.group(2) + CDN + img + '?nf_fm=jpg&nf_q=70&nf_w=800' + m.group(3) + street
                + m.group(4) + suburb.upper() + ' NSW' + m.group(5) + specs(bed, bath, car) + m.group(6)
                + f'{DAY} {t12(s)} – {t12(e)}' + m.group(7))

    out, n = CARD_RE.subn(f, html)
    assert n == len(cards), (n, len(cards))
    return out


src = open(os.path.join(HERE, 'template_Property_Campaign_Weekly_OFI.html'), encoding='utf-8').read()
d = src

# --- Row templates, taken from the Lower North Shore section of the template
row_starts = [m.start() for m in re.finditer(r'<tr>\s*<td align="left" class="es-m-p25r es-m-p25l es-m-p10t', d)]
ROW_FULL = d[row_starts[0]:tr_end(d, row_starts[0])]                      # 2 cards, 15px 30px
ROW_SINGLE_FINAL = d[row_starts[5]:tr_end(d, row_starts[5])]              # 1 card, 15px 30px 60px
assert 'es-module-8275' in ROW_FULL and 'es-module-9157' in ROW_SINGLE_FINAL
ROW_FULL_FINAL = one(r'es-m-p25b es-module-8275" style="Margin:0;padding:15px 30px"',
                     'es-m-p50b es-module-9157" style="Margin:0;padding:15px 30px 60px"', ROW_FULL)
for r in (ROW_FULL, ROW_SINGLE_FINAL, ROW_FULL_FINAL):
    assert balanced(r)


def build_rows(cards, region):
    out = []
    pairs = [cards[i:i + 2] for i in range(0, len(cards), 2)]
    for k, pair in enumerate(pairs):
        last = k == len(pairs) - 1
        tpl = (ROW_FULL_FINAL if len(pair) == 2 else ROW_SINGLE_FINAL) if last else ROW_FULL
        out.append(fill_cards(tpl, pair, region))
    return ' '.join(out)


def section_bounds(d, heading):
    h = d.find(f'font-size:22px">{heading}</p>')
    assert h > 0, heading
    s = d.rfind('<table', 0, d.rfind('class="es-content"', 0, h))
    # section ends where the next es-content / es-footer table opens
    nxt = re.compile(r'<table[^>]*class="es-(content|footer)"')
    e = nxt.search(d, h).start()
    assert balanced(d[s:e]), heading
    return s, e


def rebuild_section(sec, cards, region):
    starts = [m.start() for m in re.finditer(r'<tr>\s*<td align="left" class="es-m-p25r es-m-p25l es-m-p10t', sec)]
    a, b = starts[0], tr_end(sec, starts[-1])
    return sec[:a] + build_rows(cards, region) + sec[b:]


# --- Title
d = one(r'<title>.*?</title>', f'<title>{TITLE}</title>', d)

# --- Region sections
ls, le = section_bounds(d, 'Lower North Shore')
lns_sec = d[ls:le]
ss, se = section_bounds(d, 'Southern Highlands')
assert se > ls and ss == le
sth_sec = d[ss:se]

byb_sec = lns_sec.replace('font-size:22px">Lower North Shore</p>', 'font-size:22px">Byron Bay</p>', 1)
byb_sec = byb_sec.replace(f'office={OFFICE["lns"]}', f'office={OFFICE["byb"]}', 1)
assert 'Byron Bay' in byb_sec and OFFICE['byb'] in byb_sec

new_sections = (rebuild_section(lns_sec, LNS, 'lns') + rebuild_section(sth_sec, STH, 'sth')
                + rebuild_section(byb_sec, BYB, 'byb'))
d = d[:ls] + new_sections + d[se:]

# --- Hero tiles: Lower North Shore | Southern Highlands / Byron Bay | All Regions
hero = d.find('>Plan your Saturday<')
row1 = d.find('<td align="left" class="es-m-p25" style="padding:30px;Margin:0">', hero)
lns_tile_s = d.find('<table cellspacing="0" cellpadding="0" align="left" class="es-left es-m-p25b"', row1)
lns_tile_e = d.find('</table></td></tr></tbody></table>', lns_tile_s) + len('</table></td></tr></tbody></table>')
lns_tile = d[lns_tile_s:lns_tile_e]
assert 'Lower North Shore' in lns_tile and balanced(lns_tile)
byb_tile = (lns_tile.replace('https://www.atlas.com.au/office/lower-north-shore', 'https://www.atlas.com.au/office/byron-bay')
            .replace('>Lower North Shore<', '>Byron Bay<').replace(f'office={OFFICE["lns"]}', f'office={OFFICE["byb"]}'))
byb_tile = re.sub(r'(<img src=")[^"]+(")', r'\g<1>' + BYRON_TILE_IMG + r'\g<2>', byb_tile, count=1)

row2 = d.find('<tr><td align="left" class="es-m-p50b es-m-p25l es-m-p25r" style="padding:0 30px 60px;Margin:0">', row1)
ar_s = d.find('<table cellspacing="0" cellpadding="0" align="left" class="es-left es-m-p25b"', row2)
ar_e = d.find('</table></td>\n</tr></tbody></table>', ar_s) + len('</table></td>\n</tr></tbody></table>')
all_regions = d[ar_s:ar_e]
assert 'All Regions' in all_regions and balanced(all_regions)
sp_s = d.find('<table cellspacing="0" align="right"', ar_e)
sp_e = d.find('</table></td></tr></tbody></table>', sp_s) + len('</table></td></tr></tbody></table>')
spacer = d[sp_s:sp_e]
assert 'es-mobile-hidden' in spacer and balanced(spacer)
all_regions = (all_regions.replace('align="left" class="es-left es-m-p25b"', 'align="right" class="es-right"', 1)
               .replace('float:left', 'float:right', 1)
               .replace('https://www.atlas.com.au/office/brisbane',
                        'https://www.atlas.com.au/upcoming-inspections?queryType=inspection&forType=sale&sort=earliestInspectionDateTime_ASC'))
d = d[:ar_s] + byb_tile + d[ar_e:sp_s] + all_regions + d[sp_e:]

# --- Footer OUR LOCATIONS: drop Brisbane, keep Byron Bay
bal = d.find('209 Riding Road')
cell_s = d.rfind('<td align="left" class="es-m-p10b es-m-text"', 0, bal)
cell_e = d.find('</tbody></table></td></tr></tbody></table>', bal)
assert '1300 898 597' in d[cell_s:cell_e]
d = d[:cell_s] + '<td align="center" style="padding:0;Margin:0;display:none"></td></tr>' + d[cell_e:]

# --- Brand baseline fixes
d = one(r'class="es-wrapper-color" lang="en" style="background-color:transparent"',
        'class="es-wrapper-color" lang="en" style="background-color:#F6F6F6"', d)
d = re.sub(r'#2cb543', 'transparent', d, flags=re.I)

# --- Guards
for gone in ('Balmoral QLD', 'office/brisbane', 'fm=avif'):
    assert gone not in d, f'leftover: {gone}'
assert d.count('OPEN INSPECTION</strong>') == len(LNS) + len(STH) + len(BYB)
assert len(re.findall(r'padding:15px 30px 60px', d)) == 3
assert d.count('<table') == d.count('</table>') and d.count('<tr') == d.count('</tr>')

d = xhtml_pass(d)  # final step, always
out = os.path.join(HERE, f'OFI_NSW_26Sep2026.html')
open(out, 'w', encoding='utf-8').write(d)
print('wrote', out, len(d.encode()), 'bytes;', len(LNS), len(STH), len(BYB), 'cards')
