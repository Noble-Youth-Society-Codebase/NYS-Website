"""Build, validate, and package the static site for Amplify drag-and-drop hosting."""
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"
OUTPUT = ROOT / "nys-amplify.zip"


def main():
    for script in ("build_site.py", "check_site.py"):
        subprocess.run(
            [sys.executable, str(ROOT / "construction" / "scripts" / script)],
            cwd=ROOT,
            check=True,
        )

    # Write beside the output so a failed build/package keeps the previous ZIP.
    with tempfile.NamedTemporaryFile(
        dir=ROOT, prefix=".nys-amplify-", suffix=".zip", delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        files = sorted(path for path in DIST.rglob("*") if path.is_file())
        with ZipFile(temporary_path, "w", compression=ZIP_DEFLATED) as archive:
            for path in files:
                # Amplify needs index.html at the root, without a dist/ wrapper.
                archive.write(path, path.relative_to(DIST).as_posix())
        with ZipFile(temporary_path) as archive:
            if "index.html" not in archive.namelist():
                raise RuntimeError("Deployment archive is missing root index.html")
            corrupt_file = archive.testzip()
            if corrupt_file:
                raise RuntimeError(f"Deployment archive is corrupt: {corrupt_file}")
        temporary_path.replace(OUTPUT)
    finally:
        temporary_path.unlink(missing_ok=True)

    print(f"Ready to upload: {OUTPUT}", flush=True)
    print(f"Packaged {len(files)} files ({OUTPUT.stat().st_size / 1024 / 1024:.1f} MiB).")


if __name__ == "__main__":
    main()
