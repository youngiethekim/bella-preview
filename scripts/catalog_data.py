#!/usr/bin/env python3
"""Shared catalog parsing for the lookbook + the ops catalog database.

One source of truth for the SKU grammar ({ROOM}-{COLLECTION}-{###}) and the
room/brand/style vocabularies, so bella-lookbook.html and bella-catalog-db.html
can never drift apart. Both generators read the same tiles in assets/lookbook/.
"""
import os, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LB = ROOT / "assets" / "lookbook"

ROOM = {"LR": "Living Room", "DR": "Dining Room", "BDR": "Bedroom", "BR": "Bedroom", "BD": "Bedroom",
        "KI": "Kitchen", "KT": "Kitchen", "OF": "Office", "EX": "Exterior"}
ROOM_ORDER = ["Living Room", "Dining Room", "Bedroom", "Kitchen", "Office", "Exterior"]
# branded SKUs: {ROOM}-{BRAND}-###
BRAND = {"ROVE": "Rove Concepts", "SUNDAYS": "Sundays", "MOB": "Mobital", "GUS": "Gus*",
         "EM": "Eternity Modern", "ROC": "Roche Bobois"}
BRAND_ORDER = ["Rove Concepts", "Sundays", "Mobital", "Gus*", "Eternity Modern", "Roche Bobois"]
# each brand's signature style, mapped onto the canonical style vocabulary below
SIG_STYLE = {"ROVE": "Modern", "SUNDAYS": "Coastal", "MOB": "Modern", "GUS": "Mid-Century",
             "EM": "Contemporary", "ROC": "Bold Luxe"}
# catalogue SKUs: {ROOM}-{STYLE}-### (style codes)
STYLE_CODES = {"MDRN": "Modern", "CONT": "Contemporary", "COAS": "Coastal", "HAMP": "Hamptons Coastal",
               "MCM": "Mid-Century", "SCND": "Scandinavian", "TRNS": "Transitional", "FARM": "Farmhouse",
               "MFRM": "Modern Farmhouse", "NDBH": "Nordic Boho", "TRAD": "Traditional",
               "PTIO": "Patio", "SKY": "Sky"}
STYLE_ORDER = ["Modern", "Contemporary", "Coastal", "Hamptons Coastal", "Mid-Century", "Scandinavian",
               "Transitional", "Farmhouse", "Modern Farmhouse", "Nordic Boho", "Bold Luxe", "Traditional",
               "Patio", "Sky"]

SKU_RE = re.compile(r'^(LR|DR|BDR|BD|BR|KI|KT|OF|EX)-([A-Z]+)-([A-Z]?)(\d{2,4})$')


def load_items(verbose=True):
    """Parse every tile in assets/lookbook/ into a sorted list of set records."""
    items = []
    for f in sorted(os.listdir(LB)):
        if not f.lower().endswith(".jpg"):
            continue
        sku = f[:-4]
        m = SKU_RE.match(sku)
        if not m:
            if verbose: print("SKIP (unparsed):", sku)
            continue
        room, mid, _pfx, num = m.group(1), m.group(2), m.group(3), int(m.group(4))
        it = {"sku": sku, "img": f"assets/lookbook/{f}", "room": ROOM.get(room, room), "num": num}
        if mid in BRAND:                       # branded set
            it.update(type="brand", brand=BRAND[mid], label=BRAND[mid], style=SIG_STYLE[mid])
        elif mid in STYLE_CODES:               # style-catalogue set
            it.update(type="style", brand=None, label=STYLE_CODES[mid], style=STYLE_CODES[mid])
        else:
            if verbose: print("SKIP (unknown collection):", sku)
            continue
        items.append(it)
    items.sort(key=sortkey)
    return items


def sortkey(it):
    tr = 0 if it["type"] == "brand" else 1
    cr = (BRAND_ORDER.index(it["label"]) if it["type"] == "brand" and it["label"] in BRAND_ORDER
          else (STYLE_ORDER.index(it["style"]) if it["style"] in STYLE_ORDER else 99))
    rr = ROOM_ORDER.index(it["room"]) if it["room"] in ROOM_ORDER else 99
    return (tr, cr, rr, it["num"])


def facets(items):
    """The filter option lists actually present, in intended display order."""
    rooms = [r for r in ROOM_ORDER if any(i["room"] == r for i in items)]
    brands = [b for b in BRAND_ORDER if any(i.get("brand") == b for i in items)]
    styles = [s for s in STYLE_ORDER if any(i["style"] == s for i in items)]
    return rooms, brands, styles
