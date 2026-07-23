#!/usr/bin/env python3
"""Assembles the static Amber Consultants site from page fragments + shared shell.
Run: python3 build.py   (from the site/ directory)
Source of truth for header/footer/nav lives here so all 8 pages stay in sync.
"""
import json
import os
import re
import urllib.parse

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(SITE_DIR, "pages")

NAV_ITEMS = [
    ("home", "Home", "home.html", None),
    ("about", "About Us", "about.html", None),
    ("services", "Services", "services.html", [
        ("property-management.html", "Property Management"),
        ("real-estate.html", "Real Estate"),
        ("renovation-repairs.html", "Renovation & Repairs"),
        ("interior-design.html", "Interior Design"),
    ]),
    ("gallery", "Gallery", "gallery.html", None),
    ("listings", "Listings", "listings.html", None),
    ("sell", "Sell/Rent", "sell.html", None),
]

# Single source of truth for business details — edit business.json and re-run
# this script; it propagates into the header/footer, page copy, and the
# client-side scripts via the generated js/business-config.js.
with open(os.path.join(SITE_DIR, "business.json"), encoding="utf-8") as f:
    BUSINESS = json.load(f)

WHATSAPP_URL = (
    "https://api.whatsapp.com/send/?phone=" + BUSINESS["whatsappNumber"] +
    "&text=" + urllib.parse.quote_plus(BUSINESS["whatsappMessage"])
)

def tel_href(number):
    """Turns a display phone/landline string into a dialable tel: target."""
    digits = re.sub(r"[^\d+]", "", number)
    if digits.startswith("0"):
        digits = "+91" + digits[1:]
    elif not digits.startswith("+"):
        digits = "+91" + digits
    return digits

PHONE_TEL = tel_href(BUSINESS["phone"])
LANDLINE_TEL = tel_href(BUSINESS["landline"])

# Tokens usable inside pages/*.html fragments — replaced at build time.
FRAGMENT_TOKENS = {
    "{{WHATSAPP_URL}}": WHATSAPP_URL,
    "{{PHONE_TEL}}": PHONE_TEL,
    "{{PHONE}}": f'<a href="tel:{PHONE_TEL}">{BUSINESS["phone"]}</a>',
    "{{LANDLINE}}": f'<a href="tel:{LANDLINE_TEL}">{BUSINESS["landline"]}</a>',
    "{{EMAIL}}": f'<a href="mailto:{BUSINESS["email"]}">{BUSINESS["email"]}</a>',
    "{{ADDRESS}}": BUSINESS["address"],
    "{{HOURS}}": BUSINESS["hours"],
    "{{MAPS_QUERY}}": BUSINESS["googleMapsQuery"],
}

def apply_fragment_tokens(text):
    for token, value in FRAGMENT_TOKENS.items():
        text = text.replace(token, value)
    return text

def nav_html(active_key, mobile=False):
    out = []
    cls = "mobile-sheet-nav" if mobile else "nav-links"
    tag_open = "<ul class=\"nav-links\">" if not mobile else ""
    for key, label, href, children in NAV_ITEMS:
        current = ' aria-current="page"' if key == active_key else ""
        if children:
            open_cls = " open" if key == active_key and mobile else ""
            if mobile:
                out.append(f'''<li class="has-dropdown{open_cls}">
                  <a class="nav-link" href="{href}"{current}>{label}</a>
                  <div class="dropdown-inline">
                    {''.join(f'<a href="{c_href}">{c_label}</a>' for c_href, c_label in children)}
                  </div>
                </li>''')
            else:
                out.append(f'''<li class="has-dropdown">
                  <a class="nav-link" href="{href}"{current}>{label}
                    <svg class="chev" viewBox="0 0 12 8" fill="none"><path d="M1 1.5L6 6.5L11 1.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                  </a>
                  <div class="dropdown">
                    {''.join(f'<a href="{c_href}">{c_label}</a>' for c_href, c_label in children)}
                  </div>
                </li>''')
        else:
            out.append(f'<li><a class="nav-link" href="{href}"{current}>{label}</a></li>')
    joined = "\n".join(out)
    if mobile:
        return joined
    return f'<ul class="nav-links">\n{joined}\n</ul>'

def render_shell(title, description, active_key, body, og_image="assets/images/Home-marketing-leasing-1024x684.jpg", extra_scripts=None):
    nav_desktop = nav_html(active_key, mobile=False)
    nav_mobile = nav_html(active_key, mobile=True)
    extra_scripts_html = "".join(f'\n<script src="{src}"></script>' for src in (extra_scripts or []))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Amber Consultants</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/logos/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body>

<a href="#main" class="visually-hidden-focusable" style="position:absolute;left:-9999px;">Skip to content</a>

<header class="site-header">
  <div class="container nav-row">
    <a href="home.html" class="brand-mark" aria-label="Amber Consultants home">
      <img src="assets/logos/logo-header.png" alt="Amber Consultants">
    </a>
    <nav aria-label="Primary">
      {nav_desktop}
    </nav>
    <div class="nav-cta">
      <a href="contact.html" class="btn btn-primary btn-sm">Contact Us</a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
        <span></span>
      </button>
    </div>
  </div>
</header>

<div class="sheet-backdrop"></div>
<aside class="mobile-sheet">
  <div class="mobile-sheet-header">
    <img src="assets/logos/logo-header.png" alt="Amber Consultants" style="height:42px;">
    <button class="nav-toggle" aria-label="Close menu"><span></span></button>
  </div>
  <ul>
    {nav_mobile}
  </ul>
  <a href="contact.html" class="btn btn-primary btn-block" style="margin-top:24px;">Contact Us</a>
</aside>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="assets/logos/logo-white.png" alt="Amber Consultants" style="border-radius:8px;">
        <p>Property management, real estate, renovation and repairs, and interior design for NRI and non-local owners - handled end to end from Chennai.</p>
        <div class="social-row">
          <a class="social-icon" href="{BUSINESS['social']['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M15 8.5h2.5V5.3c-.43-.06-1.9-.18-3.6-.18-3.57 0-6 2.24-6 6.35V15H4.5v3.6H7.9V24h3.7v-5.4h3.4l.5-3.6h-3.9v-3.05c0-1.05.3-1.75 1.8-1.75z" fill="currentColor"/></svg>
          </a>
          <a class="social-icon" href="{BUSINESS['social']['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4.2" stroke="currentColor" stroke-width="1.6"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor"/></svg>
          </a>
          <a class="social-icon" href="{BUSINESS['social']['linkedin']}" target="_blank" rel="noopener" aria-label="LinkedIn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="3" stroke="currentColor" stroke-width="1.6"/><path d="M7 10v7M7 7.2v.01M11.5 17v-4.2c0-1.6.9-2.5 2.2-2.5 1.2 0 2 .8 2 2.5V17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Explore</h5>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="listings.html">Listings</a></li>
          <li><a href="contact.html">Contact Us</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        <ul>
          <li><a href="property-management.html">Property Management</a></li>
          <li><a href="real-estate.html">Real Estate</a></li>
          <li><a href="renovation-repairs.html">Renovation &amp; Repairs</a></li>
          <li><a href="interior-design.html">Interior Design</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Contact</h5>
        <ul class="footer-contact">
          <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 22s7-6.2 7-12A7 7 0 1 0 5 10c0 5.8 7 12 7 12z" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="10" r="2.4" stroke="currentColor" stroke-width="1.6"/></svg>{BUSINESS['address']}</li>
          <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M4 5h4l2 5-2.5 1.5a11 11 0 0 0 5 5L14 14l5 2v4a2 2 0 0 1-2 2C9.5 22 2 14.5 2 7a2 2 0 0 1 2-2z" stroke="currentColor" stroke-width="1.6"/></svg><a href="tel:{PHONE_TEL}" style="color:inherit;">{BUSINESS['phone']}</a></li>
          <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="4" width="20" height="16" rx="2" stroke="currentColor" stroke-width="1.6"/><path d="m3 6 9 7 9-7" stroke="currentColor" stroke-width="1.6"/></svg><a href="mailto:{BUSINESS['email']}" style="color:inherit;">{BUSINESS['email']}</a></li>
          <li><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.6"/><path d="M12 7v5l3.5 2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>{BUSINESS['hours']}</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {BUSINESS['copyrightYear']} {BUSINESS['name']}. {BUSINESS['tagline']}.</span>
      <span>Website Designed by <a href="{BUSINESS['designedBy']['url']}" target="_blank" rel="noopener" style="color:inherit; text-decoration:underline; text-underline-offset:2px;">{BUSINESS['designedBy']['name']}</a></span>
      <a href="{BUSINESS['sanityStudioUrl']}" target="_blank" rel="noopener" class="admin-link" style="color:inherit; text-decoration:underline; text-underline-offset:2px;">Admin</a>
    </div>
  </div>
</footer>

<a href="{WHATSAPP_URL}" target="_blank" rel="noopener" class="whatsapp-fab" aria-label="Chat with Amber Consultants on WhatsApp">
  <svg width="30" height="30" viewBox="0 0 24 24" fill="white" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.098-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347M12.05 21.785h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.002-5.45 4.437-9.884 9.889-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884M20.52 3.449C18.24 1.245 15.24 0 12.045 0 5.463 0 .104 5.36.101 11.943c0 2.105.549 4.161 1.595 5.976L0 24l6.235-1.635a11.94 11.94 0 0 0 5.71 1.454h.005c6.582 0 11.941-5.36 11.944-11.943a11.876 11.876 0 0 0-3.374-8.421" fill="white"/></svg>
</a>

<div class="lightbox">
  <button class="lightbox-close" aria-label="Close">✕</button>
  <button class="lightbox-nav lightbox-prev" aria-label="Previous">‹</button>
  <img src="" alt="">
  <button class="lightbox-nav lightbox-next" aria-label="Next">›</button>
</div>

<script src="js/business-config.js"></script>
<script src="js/main.js"></script>{extra_scripts_html}
</body>
</html>
"""

PAGES = [
    ("home.html", "Home", "Property management, interior design, real estate, and renovation - complete property solutions for NRI and non-local owners in Chennai.", "home"),
    ("about.html", "About Us", "Meet Amber Consultants - your trusted partner for NRI and non-local property management in Chennai.", "about"),
    ("services.html", "Services", "Amber Consultants - property management, real estate, renovation and repairs, and interior design. Choose a service to get started.", "services"),
    ("property-management.html", "Property Management", "End-to-end rental property management: tenant screening, lease management, maintenance, and financial reporting.", "services"),
    ("real-estate.html", "Real Estate", "Buy, sell, and rent residential and commercial property in Chennai with expert guidance from Amber Consultants.", "services"),
    ("renovation-repairs.html", "Renovation & Repairs", "Painting, electrical, plumbing, and full renovation work for homes and commercial spaces in Chennai.", "services"),
    ("interior-design.html", "Interior Design", "Residential and commercial interior design in Chennai - modular kitchens, renovations, and complete home transformations.", "services"),
    ("gallery.html", "Gallery", "A look at Amber Consultants' interior design and property work.", "gallery"),
    ("listings.html", "Listings", "Property listings from Amber Consultants - browse properties for sale and for rent.", "listings"),
    ("sell.html", "Sell / Rent Your Property", "List your property with Amber Consultants - tell us about it and we'll help you sell or rent it.", "sell"),
    ("contact.html", "Contact Us", "Get in touch with Amber Consultants - call, WhatsApp, or send us your property management enquiry.", "contact"),
]

def write_business_config():
    """Generates js/business-config.js from business.json so client-side
    scripts (listings.js, main.js) can read business details without a
    runtime fetch — a plain <script> tag works identically on file://,
    a local server, and GitHub Pages."""
    out_path = os.path.join(SITE_DIR, "js", "business-config.js")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated from business.json by build.py — do not edit directly.\n")
        f.write("window.AMBER_BUSINESS = " + json.dumps(BUSINESS, indent=2) + ";\n")
    print("built js/business-config.js")

def main():
    write_business_config()

    for filename, title, desc, active_key in PAGES:
        frag_path = os.path.join(PAGES_DIR, filename)
        with open(frag_path, encoding="utf-8") as f:
            body = apply_fragment_tokens(f.read())
        extra_scripts = ["js/listings.js"] if filename == "listings.html" else None
        html = render_shell(title, desc, active_key, body, extra_scripts=extra_scripts)
        out_path = os.path.join(SITE_DIR, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("built", filename)
        if filename == "home.html":
            home_html = html

    # The domain root mirrors the Home page in full (chrome and nav intact),
    # not a separate chrome-less splash.
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_html)
    print("built index.html (mirrors home.html)")

if __name__ == "__main__":
    main()
