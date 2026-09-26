"""Build the Atlas property landing page.

  python3 build.py            -> index.html (production: CDN fonts, relative images)
  python3 build.py --inline F -> F (self-contained fragment, fonts/images as data URIs)
"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).parent
CDN = "https://cdn.jsdelivr.net/gh/tadatlas/atlas-app-fonts@main/"
FONTS = {
    "FONT_RHYMES": "rhymes%20woff/Rhymes%20Display%20Light.woff2",
    "FONT_FAKT_400": "Fakt%20WOFF/FaktTT-Normal.woff2",
    "FONT_FAKT_500": "Fakt%20WOFF/FaktTT-Medium.woff2",
    "FONT_FAKT_700": "Fakt%20WOFF/FaktTT-Bold.woff2",
}
IMAGES = {"IMG_HERO": "assets/hero.jpg", "IMG_INTERIOR": "assets/interior.jpg"}
LOGO = ("https://eupsscf.stripocdn.email/content/guids/CABINET_399e3ce7c0233178f8ffdcf5f73b4ebe7cc6aec5daeb767c90c6e81e04368330"
        "/images/atlas_logo_combined2.png")

def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()

def render(inline, font_dir=None):
    html = (HERE / "property.src.html").read_text()
    subs = {"LOGO": LOGO}
    for k, rel in FONTS.items():
        if inline:
            local = pathlib.Path(font_dir) / rel.split("/")[-1].replace("%20", "-")
            subs[k] = data_uri(local, "font/woff2")
        else:
            subs[k] = CDN + rel
    for k, rel in IMAGES.items():
        subs[k] = data_uri(HERE / rel, "image/jpeg") if inline else rel
    for k, v in subs.items():
        html = html.replace("{{%s}}" % k, v)
    assert "{{" not in html, "unreplaced placeholder"
    return html

if __name__ == "__main__":
    if "--inline" in sys.argv:
        out, font_dir = sys.argv[sys.argv.index("--inline") + 1], sys.argv[-1]
        pathlib.Path(out).write_text(render(True, font_dir))
    else:
        body = render(False)
        head, rest = body.split("</style>", 1)
        doc = ('<!doctype html>\n<html lang="en-AU">\n<head>\n<meta charset="utf-8">\n'
               '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
               + head + "</style>\n</head>\n<body>" + rest + "</body>\n</html>\n")
        (HERE / "index.html").write_text(doc)
