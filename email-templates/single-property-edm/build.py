#!/usr/bin/env python3
"""Build an Atlas single-property EDM from a JSON data file.

Design system is lifted from the Weekly OFI template (Stripo export): the head/CSS,
header, OFF-MARKET ACCESS block and footer are kept verbatim in partials/, and the
property-specific blocks below are new components written in the same Stripo idiom
(es-content sections, esdev-mso-table columns, es-m-* mobile classes).

Blocks, top to bottom:
    header        dark band — logo | header line 1 / line 2           (partial)
    intro         eyebrow, serif headline                              (white)
    hero          full-width lead photo, linked to the listing         (white)
    details       street, suburb, specs, body copy                     (white)
    inspection    sand panel — OPEN INSPECTION + day/time | CTA        (white)
    gallery       two photos side by side                              (white)
    agents        ENQUIRIES — name, phone, email per agent             (white)
    sold          "Recently Sold" cards — image | details + price line (sand, optional)
    off-market    OFF-MARKET ACCESS register block                     (partial)
    footer        locations, socials, legal, ActiveCampaign footer     (partial)

Usage:
    python build.py data/<file>.json            -> output/<name>.html
    python build.py data/<file>.json --check    also runs scripts/verify_email.py --no-net
"""

import html
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "scripts"))
from xhtml_pass import xhtml_pass  # noqa: E402

SANS = "helvetica, 'helvetica neue', arial, verdana, sans-serif"
SERIF = "'times new roman', times, baskerville, georgia, serif"
TR = "mso-table-lspace:0pt;mso-table-rspace:0pt;border-spacing:0px"
TD0 = "padding:0;Margin:0;margin:0"
PB = "Margin:0;mso-line-height-rule:exactly;"

INK, BODY, SAND = "#1e1e1e", "#333333", "#ebe4df"

ASTEROID = ("https://imagesv1.asteroidcdn.com/___imageconnV2/eyJ1IjoiaHR0cHM6Ly9hZ2VudGJveGNkbi5jb20uYXUv"
            "IiwiZSI6MzE1MzYwMDAwMH0.7vD7u29jibRAITaQ9rp6xQP_aV3PNNwnIiXc_xsiNP0/")
AGENTBOX = "https://agentboxcdn.com.au/"

# Template-specific mobile rules. Every new button class needs one (blanket Stripo rule
# otherwise renders it as a fat boxed button on phones).
EXTRA_CSS = (
    '<style type="text/css">@media only screen and (max-width:600px) {'
    ' a.es-button.es-button-3401 { font-size:10px!important; padding:12px 14px!important; white-space:nowrap }'
    ' .es-m-p20 { padding:20px!important }'
    '}</style>'
)


def esc(text):
    """Escape copy for markup. Keeps intentional entities such as &nbsp;."""
    return re.sub(r"&amp;(#?\w+;)", r"&\1", html.escape(text, quote=False))


# ---------------------------------------------------------------- data helpers

def email_img(url, width=800):
    """Listing photo URL for email. AgentBox originals go through the Asteroid resizer
    (same conversion the Weekly OFI uses); Reapit URLs are used as supplied."""
    if url.startswith(AGENTBOX):
        return f"{ASTEROID}{url[len(AGENTBOX):]}?nf_fm=jpg&amp;nf_q=70&amp;nf_w={width}"
    if "asteroidcdn.com" in url:
        url = re.sub(r"nf_fm=avif", "nf_fm=jpg", url)
        url = re.sub(r"nf_w=\d+", f"nf_w={width}", url)
        return re.sub(r"&(amp;)?nf_h=\d+", "", url).replace("&nf", "&amp;nf")
    return url


def tracked(url, campaign, content):
    return (f"{url}?utm_source=property_edm&amp;utm_medium=email"
            f"&amp;utm_campaign={campaign}&amp;utm_content={content}")


def specs(p):
    s = f"{p['beds']} BED &nbsp;{p['baths']} BATH"
    return s + (f" &nbsp;{p['cars']} CAR" if p.get("cars") else "")


def phone_href(phone):
    digits = re.sub(r"\D", "", phone)
    return "tel:+61" + digits[1:] if digits.startswith("0") else "tel:" + digits


# ---------------------------------------------------------------- primitives

def section(rows, bg="#ffffff", module=""):
    return (f'<table cellpadding="0" cellspacing="0" align="center" class="es-content" role="none" '
            f'style="{TR};width:100%;table-layout:fixed !important"><tr>'
            f'<td align="center" bgcolor="#f5f5f5" class="{module}" style="{TD0};background-color:#f5f5f5">'
            f'<table align="center" bgcolor="{bg}" cellpadding="0" cellspacing="0" class="es-content-body" '
            f'role="none" style="{TR};background-color:{bg};width:600px">'
            + "".join(rows) + "</table></td></tr></table>")


def row(inner, pad="15px 30px", mclass="es-m-p25l es-m-p25r es-m-p10t es-m-p5b"):
    return f'<tr><td align="left" class="{mclass}" style="padding:{pad};Margin:0;margin:0">{inner}</td></tr>'


def stack(items, width=540):
    return (f'<table cellpadding="0" cellspacing="0" role="none" style="{TR};width:100%"><tr>'
            f'<td align="left" style="{TD0};width:{width}px">'
            f'<table cellpadding="0" cellspacing="0" role="presentation" style="{TR};width:{width}px">'
            + "".join(items) + "</table></td></tr></table>")


def columns(left, right, lw=263, gap=15, rw=262, total=540):
    """Two columns, kept side by side on mobile at 50% each (as the OFI cards are)."""
    def col(items, align, w):
        return (f'<td valign="top" class="esdev-mso-td es-m-w50" style="{TD0}">'
                f'<table align="{align}" cellpadding="0" cellspacing="0" class="es-{align}" role="none" '
                f'style="{TR};float:{align}"><tr><td align="left" style="{TD0};width:{w}px">'
                f'<table cellpadding="0" cellspacing="0" role="presentation" style="{TR};width:{w}px">'
                + "".join(items) + "</table></td></tr></table></td>")
    return (f'<table cellpadding="0" cellspacing="0" class="esdev-mso-table" role="none" '
            f'style="{TR};width:{total}px"><tr>'
            + col(left, "left", lw)
            + f'<td class="es-m-w0 es-m-p10r" style="{TD0};width:{gap}px"></td>'
            + col(right, "right", rw) + "</tr></table>")


def item(content, align="left", cls="es-m-text"):
    return f'<tr><td align="{align}" class="{cls}" style="{TD0}">{content}</td></tr>'


def spacer(h):
    return f'<tr><td align="center" height="{h}" style="{TD0};font-size:0"></td></tr>'


def p(text, *, font=SANS, size=13, lh=20, color=BODY, ls="0", mobile=None, weight="normal", extra_cls=""):
    mobile = mobile or size
    cls = f"{extra_cls} es-text-mobile-size-{mobile}".strip()
    return (f'<p class="{cls}" style="{PB}font-family:{font};line-height:{lh}px;letter-spacing:{ls};'
            f'font-weight:{weight};color:{color};font-size:{size}px;margin:0">{text}</p>')


def label(text, color=INK, bold=False, mobile=10):
    t = f'<strong style="font-weight:700 !important">{text}</strong>' if bold else text
    return item(p(t, size=11, lh=17, color=color, ls="2px", mobile=mobile))


def image(src, href, alt, width):
    return item(f'<a target="_blank" href="{href}" style="mso-line-height-rule:exactly;text-decoration:underline;'
                f'color:#1376c8;font-size:14px;font-weight:inherit"><img src="{src}" alt="{esc(alt)}" title="" '
                f'width="{width}" class="adapt-img" style="display:block;font-size:14px;border:0;outline:none;'
                f'text-decoration:none;margin:0" /></a>', align="center", cls="")


def text_link(text, href, size=12, color=BODY):
    return (f'<a href="{href}" target="_blank" style="mso-line-height-rule:exactly;text-decoration:none;'
            f'color:{color};font-size:{size}px;font-family:{SANS}">{text}</a>')


def button_dark(text, href):
    return (f'<span class="es-button-border" style="border-style:solid;border-color:transparent;background:{INK};'
            f'border-width:0;display:inline-block;border-radius:0;width:auto">'
            f'<a href="{href}" target="_blank" class="es-button es-button-3401" style="mso-style-priority:100 !important;'
            f'text-decoration:none !important;mso-padding-alt:0;font-family:{SANS};mso-line-height-rule:exactly;'
            f'color:#ffffff;font-size:10px;font-weight:normal;padding:12px 28px;display:inline-block;background:{INK};'
            f'border-radius:0;font-style:normal;line-height:12px;width:auto;text-align:center;letter-spacing:1.5px;'
            f'mso-border-alt:10px solid {INK};text-transform:none;white-space:nowrap">{text}</a></span>')


# ---------------------------------------------------------------- blocks

def intro(d):
    return row(stack([
        label(esc(d["eyebrow"]), color="#292929", mobile=11),
        spacer(10),
        item(p(esc(d["headline"]), font=SERIF, size=28, lh=34, color=INK, mobile=26, extra_cls="es-m-lh-12")),
    ]), pad="60px 30px 15px", mclass="es-m-p50t es-m-p25l es-m-p25r es-m-p5b")


def hero(d, href):
    pr = d["property"]
    return row(stack([image(email_img(pr["hero"], 1080), href, f"{pr['street']}, {pr['suburb']}", 540)]))


def details(d):
    pr = d["property"]
    items = [
        item(p(esc(pr["street"]), font=SERIF, size=22, lh=30, color=INK, mobile=18)),
        spacer(5),
        label(esc(pr["suburb"].upper()) + " NSW", color="#292929", mobile=11),
        spacer(15),
        label(specs(pr), color="#292929", mobile=11),
        spacer(25),
    ]
    for i, para in enumerate(d["body"]):
        if i:
            items.append(spacer(15))
        items.append(item(p(esc(para))))
    return row(stack(items))


def inspection(d, href):
    ins = d["inspection"]
    panel = columns(
        [label(esc(ins["label"]), bold=True), spacer(5),
         item(p(esc(ins["day"]), size=12, lh=18)), item(p(esc(ins["time"]), size=12, lh=18))],
        [spacer(8), item(button_dark(esc(d["cta"]["label"]), href), align="right", cls="")],
        lw=240, gap=10, rw=240, total=490)
    box = (f'<table cellpadding="0" cellspacing="0" role="none" style="{TR};width:100%"><tr>'
           f'<td align="left" bgcolor="{SAND}" class="es-m-p20" style="padding:25px;Margin:0;margin:0;'
           f'background-color:{SAND}">{panel}</td></tr></table>')
    return row(box)


def gallery(d, href):
    pr = d["property"]
    alt = f"{pr['street']}, {pr['suburb']}"
    g = pr.get("gallery") or []
    if len(g) < 2:
        return ""
    return row(columns([image(email_img(g[0]), href, alt, 263)], [image(email_img(g[1]), href, alt, 262)]))


def agents(d):
    def card(a):
        return [item(p(esc(a["name"]), font=SERIF, size=18, lh=22, color=INK, mobile=16)),
                spacer(8),
                item(p(text_link(esc(a["phone"]), phone_href(a["phone"])), size=12, lh=18)),
                item(p(text_link(esc(a["email"]), "mailto:" + a["email"]), size=12, lh=18))]
    ag = d["agents"]
    head = stack([label("ENQUIRIES", bold=True), spacer(15)])
    if len(ag) == 1:
        body = stack(card(ag[0]))
    else:
        body = columns(card(ag[0]), card(ag[1]))
    return row(head + body, pad="15px 30px 60px", mclass="es-m-p25l es-m-p25r es-m-p10t es-m-p50b")


def sold(d):
    s = d.get("sold")
    if not s or not s.get("items"):
        return ""
    rows = [row(stack([item(p(esc(s["heading"]), font=SERIF, size=22, lh=33, color=INK, mobile=18))]),
                pad="60px 30px 15px", mclass="es-m-p50t es-m-p25l es-m-p25r es-m-p5b")]
    for i, it in enumerate(s["items"]):
        last = i == len(s["items"]) - 1
        href = tracked(it["url"], d["campaign_slug"], it["id"])
        right = [label("SOLD", bold=True), spacer(10),
                 item(p(esc(it["street"]), font=SERIF, size=18, lh=22, color=INK, mobile=16)), spacer(5),
                 label(esc(it["suburb"].upper()) + " NSW", color="#292929", mobile=11), spacer(15),
                 label(specs(it), color="#292929", mobile=11), spacer(15),
                 label(esc(it.get("price_label", "PRICE")), bold=True),
                 item(p(esc(it["price"]), size=12, lh=18))]
        rows.append(row(columns([image(email_img(it["image"]), href, f"{it['street']}, {it['suburb']}", 263)], right),
                        pad="15px 30px 60px" if last else "15px 30px",
                        mclass=("es-m-p25l es-m-p25r es-m-p10t " + ("es-m-p50b" if last else "es-m-p25b"))))
    return section(rows, bg=SAND, module="es-module-5102")


# ---------------------------------------------------------------- assemble

def baseline_fixes(doc):
    """Brand baseline fixes carried on every build until corrected at source."""
    doc = doc.replace('class="es-wrapper" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;'
                      'border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-color:transparent',
                      'class="es-wrapper" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;'
                      'border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-color:#f6f6f6')
    return re.sub(r"#2CB543", "transparent", doc, flags=re.I)


def check_images(d):
    """Listing-ID <-> image-folder-ID cross-check (catches stale export image IDs)."""
    problems = []
    pr = d["property"]
    for u in [pr["hero"], *pr.get("gallery", [])]:
        if f"/{pr['id']}/" not in u:
            problems.append(f"{pr['street']}: image not in listing folder {pr['id']}: {u}")
    for it in (d.get("sold") or {}).get("items", []):
        if f"/{it['id']}/" not in it["image"]:
            problems.append(f"{it['street']}: image not in listing folder {it['id']}: {it['image']}")
    return problems


def build(d):
    part = {n: (HERE / "partials" / f"{n}.html").read_text() for n in ("head", "header", "offmarket", "footer")}
    href = tracked(d["property"]["url"], d["campaign_slug"], d["property"]["id"])
    main = section([intro(d), hero(d, href), details(d), inspection(d, href), gallery(d, href), agents(d)],
                   module="es-module-5101")
    doc = (part["head"].replace("{{TITLE}}", esc(d["title"])).replace("{{EXTRA_CSS}}", EXTRA_CSS)
           + part["header"].replace("{{HEADER_LINE_1}}", esc(d["header"]["line_1"]))
                           .replace("{{HEADER_LINE_2}}", esc(d["header"]["line_2"]))
           + " " + main + " " + sold(d) + " "
           + part["offmarket"].replace("{{OFFMARKET_URL}}", tracked("https://hq.atlas.com.au/offmarket",
                                                                     d["campaign_slug"], "offmarket_access"))
           + " " + part["footer"])
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", doc)
    if left:
        raise SystemExit(f"unreplaced placeholders: {left}")
    # XHTML pass is ALWAYS the last transformation (Stripo importer parses strict XML).
    return xhtml_pass(baseline_fixes(doc))


def main():
    src = Path(sys.argv[1])
    d = json.loads(src.read_text())
    for msg in check_images(d):
        print("WARN ", msg)
    out = HERE / "output" / (src.stem + ".html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(build(d))
    print(f"wrote {out.relative_to(HERE)} ({round(out.stat().st_size / 1024, 1)} KB)")
    if "--check" in sys.argv:
        subprocess.run([sys.executable, str(HERE / "scripts" / "verify_email.py"), str(out), "--no-net"])


if __name__ == "__main__":
    main()
