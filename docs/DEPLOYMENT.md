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

## AWS Amplify from GitHub

1. Push the full repository to GitHub, including the hidden `.github` folder.
2. Open the [AWS Amplify console](https://console.aws.amazon.com/amplify/) and choose **Create new app → GitHub**.
3. Authorize GitHub repository access, select `Noble-Youth-Society-Codebase/NYS-Website`, and choose the `main` branch.
4. Confirm the build settings use the root `amplify.yml` and publish directory `dist`. Use the default Amazon Linux 2023 build image, which includes Python 3.11.
5. Choose **Save and deploy**, then open the generated `amplifyapp.com` URL when deployment succeeds.

The root `amplify.yml` selects Python 3.11, runs `build_site.py` and `check_site.py`, and publishes all files under `dist/`. No package installation or backend is needed. Future pushes to the connected branch automatically trigger Amplify builds and deployments. See [AWS build settings documentation](https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html).

GitHub Actions runs `.github/workflows/check.yml` to build and validate pushes and pull requests to `main`. This workflow does not deploy; Amplify handles hosting separately. Change both workflow branch filters if you use a different branch for checks.

### "Get Pages site failed" in GitHub Actions

This error comes from a GitHub Pages deployment action attempting to access a Pages site that has not been enabled. The old `pages.yml` workflow deployed to GitHub Pages; it has been replaced with build and validation checks for the Amplify workflow. Commit and push the workflow replacement and `amplify.yml`, then inspect the new **Check website** run. Re-running the previous failed run uses the old workflow and will not apply this fix.

GitHub Pages settings are not required for Amplify hosting. If you choose GitHub Pages as a separate host later, enable **Settings → Pages → Source → GitHub Actions** and add a Pages deployment workflow following [GitHub's instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

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
