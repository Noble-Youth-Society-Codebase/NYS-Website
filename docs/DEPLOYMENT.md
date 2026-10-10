# Deployment

**Publish directory: `dist/`.** Deploy its contents, with `index.html` directly in the web root.

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
