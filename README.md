# Noble Youth Society website

Portable HTML, CSS, and JavaScript recreation of the owner-authorized [Noble Youth Society Wix site](https://nysvancouver.wixsite.com/noble-youth-society).

**Deploy only `dist/`. Edit and rebuild from `construction/`.**

For AWS Amplify drag-and-drop deployment, run `python construction/scripts/package_amplify.py` and upload the generated `nys-amplify.zip`.

## Repository layout

| Path | Purpose | Deploy? |
| --- | --- | --- |
| `dist/` | Complete website: HTML, CSS, JavaScript, images, fonts, video, and route aliases | **Yes — this folder only** |
| `construction/content.json` | Editable page text, member profiles, events, and media references | No |
| `construction/assets/` | Source styles and browser interactions, copied to `dist/assets/` during builds | No |
| `construction/scripts/` | Build, validation, and optional migration tools | No |
| `construction/reference/` | Captured public Wix source; local only, ignored by Git | No |
| `docs/` | Deployment guide and migration notes | No |
| `.github/workflows/check.yml` | GitHub Actions build and validation workflow | No |
| `amplify.yml` | AWS Amplify build and publish settings for GitHub deployment | No |

```text
.
├── README.md
├── .gitignore
├── .gitattributes
├── .github/workflows/check.yml
├── amplify.yml
├── dist/                         ← DEPLOY THESE FILES
│   ├── index.html
│   ├── our-members.html
│   ├── past-events.html
│   ├── upcoming-events.html
│   ├── join-us.html
│   └── assets/                   # Local media and runtime files
├── construction/                 ← EDIT / BUILD FILES
│   ├── README.md
│   ├── content.json
│   ├── assets/                   # Source CSS and JavaScript
│   ├── scripts/
│   └── reference/                # Local only, ignored
└── docs/
```

## Preview

From the repository root, with Python 3.10 or newer:

```sh
python -m http.server 8787 --bind 127.0.0.1 --directory dist
```

Open [http://127.0.0.1:8787/](http://127.0.0.1:8787/). Stop the server with Ctrl+C. You can also open `dist/index.html` directly.

## Edit and build

Edit `construction/content.json` for text, profiles, events, and links. Edit CSS and browser behavior in `construction/assets/`. To change page structure, edit `construction/scripts/build_site.py`.

Do not edit page content directly in `dist/`: Amplify rebuilds from `construction/` on every deployment and replaces those edits. Keep member biographies and grades in `construction/content.json`, then rebuild both the pages and search data.

```sh
python construction/scripts/build_site.py
python construction/scripts/check_site.py
```

The regular build uses only Python's standard library. It generates HTML and runtime data, and copies source CSS/JS into `dist/assets/`. Generated files and copied assets in `dist/` will be overwritten by builds. Local images, fonts, and video stay in `dist/assets/` and are tracked in Git. Add new media there and reference an `assets/...` path in the content file.

## Deploy

### AWS Amplify drag and drop

```sh
python construction/scripts/package_amplify.py
```

This rebuilds and checks the site, then creates `nys-amplify.zip` with `index.html` at the archive root and all media included. In the AWS Amplify console, choose **Create new app → Deploy without Git**, select **Drag and drop**, upload that ZIP, and choose **Save and deploy**. Re-run the command to package future updates. See [deployment instructions](docs/DEPLOYMENT.md) for the full workflow.

### AWS Amplify from GitHub

Commit the repository files directly: `dist/`, `construction/`, `docs/`, `.github/`, `README.md`, `.gitignore`, and `.gitattributes`. Captured Wix HTML in `construction/reference/` stays local and is ignored by Git.

In AWS Amplify, choose **Create new app → GitHub**, authorize repository access, select this repository and the `main` branch, then **Save and deploy**. The root `amplify.yml` selects Python 3.11, builds and checks the site, and publishes only `dist/`. Amplify automatically deploys future pushes to the connected branch.

GitHub Actions independently builds and checks pushes and pull requests to `main`. GitHub Pages does not need to be enabled. See [deployment instructions](docs/DEPLOYMENT.md) for setup and troubleshooting.


## Included

Five main pages, three original utility routes, ten route aliases, 22 captured event entries, 24 slideshow images, and 16 profiles. Current leadership appears first, grouped by seniority, followed by past leadership grouped by term. Profiles appear two per row above 600 px and one per row on phones.

Contact prepares an email draft for the visitor to send; the chat button offers contact options. Wix's submission and live chat backends are not included. Enrollment retains the original Google Form link. See [migration notes](docs/MIGRATION.md) and [construction instructions](construction/README.md).
