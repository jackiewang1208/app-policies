# App policies · Jackie Liao

Public privacy policies for apps by Jackie Liao. This repository contains only static policy pages, not application source code.

## Published pages

- [Arrow Trails privacy policy — English](https://jackiewang1208.github.io/app-policies/arrow-trails/privacy/)
- [Arrow Trails 隐私政策 — 简体中文](https://jackiewang1208.github.io/app-policies/arrow-trails/privacy/zh/)

Public privacy contact: **wangjackiedev@gmail.com**.

## Publishing

GitHub Pages serves `main` → `/ (root)`. `.nojekyll` keeps the HTML and CSS as plain static files; no build step, JavaScript, external fonts, analytics or package installation is needed. Push reviewed changes to `main` to publish updates.

Run the static checks with `python3 tools/check_site.py`. To preview locally, run `python3 -m http.server 8766` from this directory, then open `http://localhost:8766/`.

## Adding another app

Create `<app-slug>/privacy/index.html` and, if needed, `<app-slug>/privacy/zh/index.html`. Reuse `styles.css`, but review each app's actual data practices independently. Keep public policy addresses stable.

Policies are standalone: do not add links to the site root, a shared app directory, or other apps. The root page is a neutral notice and does not list apps. An app's policy may link to its own language versions and relevant external privacy statements. This navigation separation does not make the public repository or its files private.

## Content maintenance

The Arrow Trails policy describes its current offline Android implementation. Recheck the policy before publishing an app update that adds advertising, analytics, crash reporting, accounts, purchases or cloud features. Keep English and Chinese versions aligned and update both dates when changing the policy.

The policy includes commitments to use support emails only for responding to requests, retain them only as necessary, and handle privacy requests. These practices must also be followed when operating the support mailbox.

Publishing a webpage does not update the game's in-app policy entry or Play Console. Those are separate release tasks. Only publish approved public contact information; do not add account IDs, private contacts, credentials, signing keys or private game files.
