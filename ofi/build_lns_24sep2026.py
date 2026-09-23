#!/usr/bin/env python3
"""Build the Thursday 24 September 2026 Lower North Shore OFI email.

Source template: template_Property_Campaign_Weekly_OFI.html (Stripo export).
Data: Notion MASTER Property Marketing Database, Office ID = LNS, Date = 2026-09-24.
"""
import os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = glob.glob('/root/.claude/skills/**/atlas-email/scripts', recursive=True)
sys.path.insert(0, SKILL[0] if SKILL else HERE)
from xhtml_pass import xhtml_pass

CAMPAIGN = 'weekly_ofi_lns_24sep2026'
DAY = 'Thursday'
DATE_LABEL = 'THURSDAY 24 SEPTEMBER'
TITLE = '24 September Weekly OFI Email'
CDN = ('https://imagesv1.asteroidcdn.com/___imageconnV2/eyJ1IjoiaHR0cHM6Ly9hZ2VudGJveGNkbi5jb20uYXUvIiwiZSI6MzE1MzYwMDAwMH0.'
       '7vD7u29jibRAITaQ9rp6xQP_aV3PNNwnIiXc_xsiNP0/clients-data/26319/public_html/media/lt/1/')

# street, suburb, bed, bath, car, start, end, id, slug, image path (after CDN prefix)
CARDS = [
    ('34 Willowie Road', 'Castle Cove', 5, 5, '4', '10:30', '11:00', '1P11087', '34-willowie-road-castle-cove-nsw-1p110873', '1P11087/1788245496747925967281019-rsd.jpg'),
    ('16 Redan Street', 'Mosman', 4, 4, '2', '11:15', '11:45', '1P10981', '16-redan-street-mosman-nsw-1p109813', '1P10981/178832618570662508-rsd.jpg'),
    ('9 Sirius Avenue', 'Mosman', 5, 6, '4', '11:45', '12:15', '1P8796', '9-sirius-avenue-mosman-nsw-1p87963', '1P8796/1770768943159263626307684-rsd.jpg'),
    ('5 Churchill Crescent', 'Cammeray', 5, 3, '4', '11:45', '12:15', '1P10469', '5-churchill-crescent-cammeray-nsw-1p104693', '1P10469/178660470842838282-rsd.jpg'),
    ('8 Prince Albert Street', 'Mosman', 6, 5, '4', '12:30', '13:00', '1P10388', '8-prince-albert-street-mosman-nsw-1p103883', '1P10388/178649565094760368-rsd.jpg'),
    ('42 Jeffreys Street', 'Kirribilli', 4, 4, '-', '12:45', '13:15', '1P11051', '42-jeffreys-street-kirribilli-nsw-1p110513', '1P11051/178581991527892270-rsd.jpg'),
    ('4D/46-48 Muston Street', 'Mosman', 3, 2, '2', '13:00', '13:30', '1P10692', '4d-46-48-muston-street-mosman-nsw-1p106923', '1P10692/178530983874451256-rsd.jpg'),
    ('2a Cross Street', 'Mosman', 5, 5, '4', '13:00', '13:30', '1P11251', '2a-cross-street-mosman-nsw-1p112513', '1P11251/178823760909918252-rsd.jpg'),
    ('21 Hopetoun Avenue', 'Mosman', 5, 5, '4', '13:30', '14:00', '1P11277', '21-hopetoun-avenue-mosman-nsw-1p112773', '1P11277/178830458362255028-rsd.jpg'),
    ('2 Lodge Road', 'Cremorne', 4, 3, '2', '14:15', '14:45', '1P11177', '2-lodge-road-cremorne-nsw-1p111773', '1P11177/178728006760021954-rsd.jpg'),
    ('6 Coolawin Road', 'Northbridge', 5, 4, '2', '14:45', '15:15', '1P10600', '6-coolawin-road-northbridge-nsw-1p106003', '1P10600/178640430559003465-rsd.jpg'),
]


def t12(hhmm):
    h, m = map(int, hhmm.split(':'))
    return f"{(h - 1) % 12 + 1}:{m:02d}{'am' if h < 12 else 'pm'}"


def specs(bed, bath, car):
    s = f'{bed} BED &nbsp;{bath} BATH'
    return s + (f' &nbsp;{car} CAR' if car.strip() not in ('', '-', '0') else '')


def one(pattern, repl, s, count=1, flags=0):
    new, n = re.subn(pattern, repl, s, count=count, flags=flags)
    assert n == count, f'expected {count} match(es) for {pattern!r}, got {n}'
    return new


src = open(os.path.join(HERE, 'template_Property_Campaign_Weekly_OFI.html'), encoding='utf-8').read()
d = src

# --- Title, date block, hero heading
d = one(r'<title>.*?</title>', f'<title>{TITLE}</title>', d)
d = one(r'>THIS WEEKEND<', f'>{DATE_LABEL}<', d)
d = one(r'>Plan your Saturday<', '>Today’s Open Homes<', d)

# --- Hero tiles: LNS | All Regions on one row, Southern Highlands tile removed
hero_start = d.find('>Today’s Open Homes<')
row1 = d.find('<td align="left" class="es-m-p25" style="padding:30px;Margin:0">', hero_start)
row2 = d.find('<tr><td align="left" class="es-m-p50b es-m-p25l es-m-p25r" style="padding:0 30px 60px;Margin:0">', row1)
row2_end = d.find('</td></tr></tbody></table></td></tr></tbody></table>', row2)
assert -1 not in (row1, row2, row2_end)
sh_tile_s = d.find('<table cellspacing="0" align="right"', row1)
sh_tile_e = d.find('</table></td></tr></tbody></table>', sh_tile_s) + len('</table></td></tr></tbody></table>')
assert sh_tile_s < row2 and sh_tile_e < row2 and 'Southern Highlands' in d[sh_tile_s:sh_tile_e]
ar_s = d.find('<table cellspacing="0" cellpadding="0" align="left" class="es-left es-m-p25b"', row2)
ar_e = d.find('</table></td>\n</tr></tbody></table>', ar_s) + len('</table></td>\n</tr></tbody></table>')
all_regions = d[ar_s:ar_e]
assert 'All Regions' in all_regions and 'VIEW ALL OPEN TIMES' in all_regions
all_regions = all_regions.replace('align="left" class="es-left es-m-p25b"', 'align="right" class="es-right"', 1)
all_regions = all_regions.replace('float:left', 'float:right', 1)
all_regions = all_regions.replace('https://www.atlas.com.au/office/brisbane',
                                  'https://www.atlas.com.au/upcoming-inspections?queryType=inspection&forType=sale&sort=earliestInspectionDateTime_ASC')
# remove row 2 (All Regions + spacer); it ends at the mso wrapper close after the spacer
row2_stop = d.find('<!--[if mso]></td></tr></table><![endif]--></td></tr>', ar_e) + len('<!--[if mso]></td></tr></table><![endif]--></td></tr>')
seg = d[row2:row2_stop]
assert seg.count('<table') == seg.count('</table>'), 'row 2 slice unbalanced'
d = d[:sh_tile_s] + all_regions + d[sh_tile_e:row2] + d[row2_stop:]
d = one(r'<td align="left" class="es-m-p25" style="padding:30px;Margin:0">',
        '<td align="left" class="es-m-p25 es-m-p50b" style="padding:30px 30px 60px;Margin:0">', d)

# --- Remove Southern Highlands card section (one balanced es-content table)
sh_head = d.find('font-size:22px">Southern Highlands</p>')
sh_s = d.rfind('<table align="center" cellspacing="0" cellpadding="0" class="es-content"', 0, sh_head)
foot_s = d.find('<table cellspacing="0" cellpadding="0" align="center" class="es-footer"', sh_head)
seg = d[sh_s:foot_s]
assert seg.count('<table') == seg.count('</table>'), 'SH section slice unbalanced'
d = d[:sh_s] + d[foot_s:]

# --- Footer OUR LOCATIONS: keep Lower North Shore only
bowral = d.find('9A/310-312 Bong Bong Street')
cell_s = d.rfind('<td align="left" class="es-m-p10b es-m-text"', 0, bowral)
cell_e = d.find('</tbody></table></td></tr></tbody></table>', bowral)
d = d[:cell_s] + '<td align="center" style="padding:0;Margin:0;display:none"></td></tr>' + d[cell_e:]
byron = d.find('2/1 Marvell Street')
r_s = d.rfind('<tr><td align="left" class="es-m-p25" style="padding:30px 30px 0;Margin:0">', 0, byron)
r_e = d.find(' <tr>', d.find('1300 898 597'))  # next footer row (social links)
seg = d[r_s:r_e]
assert 'Byron Bay' in seg and 'Balmoral' in seg and seg.count('<table') == seg.count('</table>'), 'footer row unbalanced'
d = d[:r_s] + d[r_e:]

# --- Rebuild LNS cards in place (template row modules kept verbatim)
lns_s = d.find('font-size:22px">Lower North Shore</p>')
lns_e = d.find('<table cellspacing="0" cellpadding="0" align="center" class="es-footer"', lns_s)
sec = d[lns_s:lns_e]
card_re = re.compile(
    r'(<a target="_blank" href=")https://www\.atlas\.com\.au/property/[^"]+(".*?<img[^>]*?src=")[^"]+(".*?font-size:18px">)[^<]+(</p>.*?font-size:11px">)[^<]+(</p>.*?font-size:11px">)[^<]+(</p>.*?OPEN INSPECTION</strong></p>.*?font-size:12px">)[^<]+(</p>)',
    re.S)
found = card_re.findall(sec)
assert len(found) == len(CARDS), f'template has {len(found)} card slots, data has {len(CARDS)}'
it = iter(CARDS)

def fill(m):
    street, suburb, bed, bath, car, s, e, pid, slug, img = next(it)
    href = (f'https://www.atlas.com.au/property/{slug}?utm_source=ofi_edm&utm_medium=email'
            f'&utm_campaign={CAMPAIGN}&utm_content={pid}')
    src_ = CDN + img + '?nf_fm=jpg&nf_q=70&nf_w=800'
    return (m.group(1) + href + m.group(2) + src_ + m.group(3) + street + m.group(4) + suburb.upper() + ' NSW'
            + m.group(5) + specs(bed, bath, car) + m.group(6) + f'{DAY} {t12(s)} – {t12(e)}' + m.group(7))

sec = card_re.sub(fill, sec)
d = d[:lns_s] + sec + d[lns_e:]

# --- Brand baseline fixes
d = one(r'class="es-wrapper-color" lang="en" style="background-color:transparent"',
        'class="es-wrapper-color" lang="en" style="background-color:#F6F6F6"', d)
d = re.sub(r'#2cb543', 'transparent', d, flags=re.I)

# --- Guards
for gone in ('Southern Highlands', 'Byron Bay', 'Balmoral QLD', 'Bowral', 'Saturday', 'Plan your Saturday',
             'THIS WEEKEND', 'office/brisbane', 'datocms-assets.com/190151/17'):
    assert gone not in d, f'leftover: {gone}'
assert d.count('<table') == d.count('</table>')

d = xhtml_pass(d)  # final step, always
out = os.path.join(HERE, 'OFI_LNS_24Sep2026.html')
open(out, 'w', encoding='utf-8').write(d)
print('wrote', out, len(d.encode()), 'bytes')
