# Deployment

**Publish directory: `dist/`.** Deploy its contents, with `index.html` directly in the web root.

## AWS Amplify drag and drop

From the repository root, with Python 3.10 or newer:

```sh
python construction/scripts/package_amplify.py
```

This command rebuilds the site, validates local links and assets, and creates `nys-amplify.zip` in the repository root. It requires only Python's standard library. The ZIP contains the contents of `dist/`, including all images, fonts, video, and route aliases, with `index.html` at the archive root. Generated ZIPs are ignored by Git; run the command again after editing the site.

1. Open the [AWS Amplify console](https://console.aws.amazon.com/amplify/).
2. Choose **Create new app → Deploy without Git → Next**.
3. Enter an app name (for example, `noble-youth-society`) and branch name (for example, `production`).
4. Select **Drag and drop**, then drop `nys-amplify.zip` into the upload area.
5. Choose **Save and deploy** and open the URL after deployment succeeds.

For updates, rebuild the ZIP and upload it to the same app and branch using its manual deployment upload area. Amplify serves the prebuilt files; no build command, Node runtime, or `amplify.yml` is needed for this upload workflow.

Upload `nys-amplify.zip`, rather than a ZIP of the repository or a ZIP containing a top-level `dist/` folder. AWS requires the build output directly at the archive root. See [AWS's manual deployment instructions](https://docs.aws.amazon.com/amplify/latest/userguide/manual-deploys.html).

The site has separate HTML pages and directory aliases. Keep these files together and do not add a catch-all **200** rewrite to `/index.html`; that would hide the other pages. After deploying, check the homepage, `/our-members.html`, `/our-members/`, `/past-events.html`, and `/join-us.html`, including images and enrollment video playback.

## GitHub Pages

1. Push the full repository to GitHub, including the hidden `.github` folder.
2. Use `main` as the deployment branch, or change both branch filters in `.github/workflows/pages.yml`.
3. Select **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. Push a change to `main`, or choose **Actions → Check and deploy website → Run workflow**.
5. Open the deployment URL shown in the successful workflow or Pages settings.

The build job generates and validates the static site. The deploy job publishes only the `dist/` artifact to the `github-pages` environment. Pull requests run checks without publishing. Branch/environment rules must allow deployment.

Site links and asset references are relative, so they work under repository URLs such as `https://USERNAME.github.io/REPOSITORY/` without base URL changes.

Configuration follows [GitHub's custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Other static hosts

| Setting | Value |
| --- | --- |
| Project root | Repository root |
| Publish/output directory | `dist` |
| Build command, if Python is available | `python construction/scripts/build_site.py` |
| Already built file upload | No build command needed |
| Runtime dependencies | None |

For manual uploads, upload the contents of `dist/` into the web root. Keep `assets/` and route alias folders alongside `index.html`.

This is a multi-page site. Do not enable a single-page-app rewrite that sends every URL to the homepage. The alias folders preserve the original Wix routes.

Contact uses an email draft. Connect a form endpoint or chat provider separately if automatic form delivery or live chat is needed.
