# Construction files — do not deploy

The deployable website is `../dist/`.

- `content.json`: editable content and media paths.
- `assets/styles.css`: shared styling.
- `assets/members.css`: seniority brackets and two-card rows.
- `assets/fonts.css`: local font declarations.
- `assets/site.js`: navigation, gallery, photo viewer, search, contact draft preview.
- `scripts/build_site.py`: generates HTML/data and copies CSS/JS.
- `scripts/check_site.py`: checks links, fragments, assets, and member preservation.

Run these scripts from the repository root. They also resolve their file paths correctly when invoked from another working directory.

## Optional Wix extraction

Normal builds need no third-party packages. Re-extraction needs `beautifulsoup4` and the captured HTML, gallery references, and asset inventory in `reference/`. These captures are local only and ignored by Git. Fresh clones already contain the editable content and all deploy media.

```sh
python -m pip install -r construction/requirements-extraction.txt
python construction/scripts/prepare_content.py
python construction/scripts/download_assets.py
python construction/scripts/build_site.py
python construction/scripts/check_site.py
```

Re-extraction overwrites manual edits to `content.json` and `assets/fonts.css`. It targets the captured Wix markup. The asset downloader retrieves public media listed in the manifest and skips existing nonempty files.
