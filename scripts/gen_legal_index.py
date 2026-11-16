#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate /legal/ index pages for all locales in the docs repo.

Reads <title> of each legal document page (legal/<doc>/index.html and
<lang>/legal/<doc>/index.html) and builds a self-contained index page
per locale, matching the legal-page visual style (same CSS variables).
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DOCS_HOST = "https://docs.parselex.app"
DOCS = ["terms", "privacy", "personal-data", "cookies", "payments", "disclaimer"]
LOCALES = {"en": "legal", "ru": "ru/legal", "es": "es/legal", "fr": "fr/legal", "hi": "hi/legal"}

# one-line description per document, per locale
DESC = {
    "en": {
        "terms": "Governing the use of the Parselex platform and services.",
        "privacy": "What we collect, why, and how your data is protected.",
        "personal-data": "How case documents and personal data are processed.",
        "cookies": "Cookies and local storage on Parselex websites.",
        "payments": "Subscription billing, renewals and cancellations.",
        "disclaimer": "AI-generated output: scope, limits and human review.",
    },
    "ru": {
        "terms": "Условия использования платформы и сервисов Parselex.",
        "privacy": "Что мы собираем, зачем и как защищаются ваши данные.",
        "personal-data": "Как обрабатываются документы дел и персональные данные.",
        "cookies": "Cookies и локальное хранилище на сайтах Parselex.",
        "payments": "Списание по подписке, продление и отмена.",
        "disclaimer": "Результаты ИИ: границы применения и проверка человеком.",
    },
    "es": {
        "terms": "Condiciones de uso de la plataforma y los servicios de Parselex.",
        "privacy": "Qué recopilamos, por qué y cómo se protegen sus datos.",
        "personal-data": "Cómo se procesan los documentos del caso y los datos personales.",
        "cookies": "Cookies y almacenamiento local en los sitios de Parselex.",
        "payments": "Facturación de suscripciones, renovaciones y cancelaciones.",
        "disclaimer": "Resultados de IA: alcance, límites y revisión humana.",
    },
    "fr": {
        "terms": "Conditions d'utilisation de la plateforme et des services Parselex.",
        "privacy": "Ce que nous collectons, pourquoi et comment vos données sont protégées.",
        "personal-data": "Traitement des documents de dossier et des données personnelles.",
        "cookies": "Cookies et stockage local sur les sites Parselex.",
        "payments": "Facturation des abonnements, renouvellements et annulations.",
        "disclaimer": "Résultats de l'IA : périmètre, limites et revue humaine.",
    },
    "hi": {
        "terms": "Parselex प्लेटफ़ॉर्म और सेवाओं के उपयोग की शर्तें।",
        "privacy": "हम क्या एकत्र करते हैं, क्यों, और आपका डेटा कैसे सुरक्षित है।",
        "personal-data": "केस दस्तावेज़ों और व्यक्तिगत डेटा की प्रक्रिया कैसे होती है।",
        "cookies": "Parselex वेबसाइटों पर cookies और लोकल स्टोरेज।",
        "payments": "सब्सक्रिप्शन बिलिंग, नवीनीकरण और रद्दीकरण।",
        "disclaimer": "AI-आउटपुट: दायरा, सीमाएँ और मानव समीक्षा।",
    },
}

INTRO = {
    "en": "Legal documents governing the use of Parselex.",
    "ru": "Правовые документы, регулирующие использование Parselex.",
    "es": "Documentos legales que regulan el uso de Parselex.",
    "fr": "Documents juridiques régissant l'utilisation de Parselex.",
    "hi": "Parselex के उपयोग को नियंत्रित करने वाले कानूनी दस्तावेज़।",
}
LEGAL_LABEL = {"en": "Legal", "ru": "Правовые документы", "es": "Legal",
               "fr": "Mentions légales", "hi": "कानूनी दस्तावेज़"}


def page_title(path):
    if not os.path.isfile(path):
        return None
    m = re.search(r"<title>(.*?)</title>", open(path, encoding="utf-8").read(), re.S)
    return m.group(1).strip() if m else None


def build(locale):
    base = LOCALES[locale]
    items = []
    for d in DOCS:
        t = page_title(os.path.join(ROOT, base, d, "index.html"))
        if not t:
            print(f"  !! missing {base}/{d}/index.html - skipped")
            continue
        desc = DESC[locale][d]
        items.append((d, t, desc))
    hreflang = "".join(
        f'\n<link rel="alternate" hreflang="{c}" href="{DOCS_HOST}/{("" if c == "en" else c + "/")}legal/">'
        for c in ["en", "ru", "es", "fr", "hi"])
    cards = "".join(
        f'<a class="doc" href="{d}/"><span class="dn">{t}</span><span class="dd">{desc}</span>'
        f'<span class="go">&#8594;</span></a>'
        for d, t, desc in items)
    return f"""<!DOCTYPE html>
<html lang="{locale}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{LEGAL_LABEL[locale]} — Parselex</title>
<meta name="description" content="{INTRO[locale]}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{DOCS_HOST}/{("" if locale == "en" else locale + "/")}legal/">\
{hreflang}
<style>
:root,[data-theme="light"]{{--bg-body:#F8F9FB;--bg-card:#FFFFFF;--border:#E2E5EB;--text:#1A1D23;--text-2:#5A6070;--muted:#8B919E;--primary:#1B2A4A;--accent:#C9953C}}
[data-theme="dark"]{{--bg-body:#141821;--bg-card:#1C2030;--border:#2A3040;--text:#E8EAF0;--text-2:#A0A8B8;--muted:#6B7280;--primary:#E8EAF0;--accent:#D4A843}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg-body);color:var(--text);line-height:1.65;font-size:15px;min-height:100vh;display:flex;flex-direction:column}}
.top{{background:var(--bg-card);border-bottom:1px solid var(--border);padding:12px 24px;display:flex;justify-content:space-between;align-items:center}}
.brand{{display:flex;align-items:center;gap:10px;font-weight:800;font-size:16px;color:var(--text);text-decoration:none}}
.brand-icon{{width:30px;height:30px;border-radius:8px;background:var(--primary);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:15px}}
.back{{font-size:13px;color:var(--accent);font-weight:600;text-decoration:none}}
.wrap{{max-width:820px;margin:0 auto;padding:44px 24px;flex:1;width:100%}}
h1{{font-size:26px;font-weight:800;margin-bottom:6px;color:var(--text)}}
.intro{{color:var(--text-2);margin-bottom:26px}}
.doc{{display:flex;align-items:center;gap:14px;background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:10px;text-decoration:none;color:var(--text);transition:border-color .15s}}
.doc:hover{{border-color:var(--accent)}}
.doc .dn{{font-weight:700;display:block}}
.doc .dd{{color:var(--text-2);font-size:13.5px;display:block;margin-top:2px}}
.doc .go{{margin-left:auto;color:var(--accent);font-weight:800}}
.foot{{max-width:820px;width:100%;margin:0 auto;padding:18px 24px;border-top:1px solid var(--border);font-size:12.5px;color:var(--muted)}}
.foot a{{color:var(--accent);text-decoration:none}}
</style>
</head>
<body>
<div class="top"><a class="brand" href="{"/" if locale == "en" else "/" + locale + "/"}"><span class="brand-icon">&#9878;</span>PARSELEX</a>
<a class="back" href="{DOCS_HOST}/">&#8592; docs.parselex.app</a></div>
<div class="wrap">
<h1>{LEGAL_LABEL[locale]}</h1>
<p class="intro">{INTRO[locale]}</p>
{cards}
</div>
<div class="foot">&#9878; Parselex &#8212; <a href="{DOCS_HOST}">docs.parselex.app</a></div>
</body>
</html>"""


for loc, rel in LOCALES.items():
    out_dir = os.path.join(ROOT, rel)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build(loc))
    print(f"written {rel}/index.html")
