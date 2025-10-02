# Asset Preparer

A lightweight command-line tool for preparing image assets before upload.

This script helps CMS team members enforce size limits, sanitize directory
names, and package everything into a clean `.zip` file while skipping junk
files like `.DS_Store` or `__MACOSX`.

## Features

- Scan for oversize images (default limit: 95KB)
- Rename directories to strip illegal characters (`/$|"`)
- Create a clean `.zip` archive, excluding junk files
- `--check` mode to only report oversize images
- Exit codes for automation
- Distributed as a single `.exe` file -- no Python installation required

## Setup (Windows)

1. Download the latest release from [Releases](https://github.com/joshjavier/asset-preparer/releases) *(look for `prepare_assets.exe`)*
2. Save it somewhere convenient, e.g., in `C:\Users\YourName\bin`
3. *(Optional)* Add the folder to your PATH so you can run it from anywhere:
   - Press Win + R, type `"C:\Windows\system32\rundll32.exe"
     sysdm.cpl,EditEnvironmentVariables`
   - Under "User variables for \<YourName\>", edit `Path`, add the folder path
     (e.g., `C:\Users\YourName\bin`)
   - Now you can just run:

     ```bash
     prepare_assets.exe [options]
     ```

## Usage

```bash
# Run on current directory, enforce 95KB limit, output "assets_ready.zip"
prepare_assets.exe

# Run on ./images, output "my_assets.zip"
prepare_assets.exe images my_assets.zip

# Custom size limit (120KB)
prepare_assets.exe images --max-size 120

# Allow oversize images to pass
prepare_assets.exe images output.zip --allow-oversize

# Just check oversize images (no renaming, no zip)
prepare_assets.exe images --check
```

## Exit codes

- `0` - Success, no oversize images
- `1` - Error: oversize images (strict mode)
- `2` - `--check` mode: oversize images found

## Example output

```bash
⚠️ Found images over 95KB:
 - banner/hero.jpg
 - gallery/oversized.png
❌ Exiting because oversize images are not allowed. Use --allow-oversize to override.
```

```bash
Renamed: $10/CRM -> 10/CRM
Renamed: foo/bar$dir -> foo/bardir
🎉 Done. Output: assets_ready.zip
```

## Notes for Windows users

- Works fully offline -- no dependencies required on end-user machines.
- If you use PowerShell or CMD, commands work the same:

  ```powershell
  .\prepare_assets.exe images output.zip
  ```

- Backslashes (`\`) in output paths are normalized to forward slashes (`/`) for
  consistency across systems.

## Contributing

If you're developing locally (instead of just running the `.exe`):

1. Clone the repo

   ```bash
   git clone https://github.com/joshjavier/asset-preparer.git
   cd asset-preparer
   ```

2. Install dependencies (Python 3.7+ required):

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:

   ```bash
   python3 prepare_assets.py [options]
   ```

4. To build the `.exe`:

   ```bash
   pyinstaller --onefile prepare_assets.py
   ```
