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

## Setup (Windows)

### Prerequisites

- Python 3.7 installed
- Recommended: Git for Windows (comes with Git Bash)

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/joshjavier/asset-preparer.git
   cd asset-preparer
   ```

2. Run the script directly with:

   ```bash
   python prepare_assets.py [options]
   ```

3. *(Optional)* Add the folder to your PATH so you can run it from anywhere:
   - Press Win + R, type `"C:\Windows\system32\rundll32.exe"
     sysdm.cpl,EditEnvironmentVariables`
   - Under "User variables for \<YourName\>", edit `Path`, add the folder path
     (e.g., `C:\Users\YourName\asset-preparer`)
   - Now you can just run:

     ```bash
     prepare_assets.py [options]
     ```

## Usage

```bash
# Run on current directory, enforce 95KB limit, output "assets_ready.zip"
python prepare_assets.py

# Run on ./images, output "my_assets.zip"
python prepare_assets.py images my_assets.zip

# Custom size limit (120KB)
python prepare_assets.py images --max-size 120

# Allow oversize images to pass
python prepare_assets.py images output.zip --allow-oversize

# Just check oversize images (no renaming, no zip)
python prepare_assets.py images --check
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

- Use forward slashes (`/`) in paths for consistency, even on Windows (the
  script handles them fine).
- If you prefer PowerShell or CMD instead of Git Bash, commands work the same:

  ```powershell
  python .\prepare_assets.py images output.zip
  ```

- Backslashes (`\`) in output will be normalized to forward slashes (`/`) for
  consistency across systems.

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/new-thing`)
3. Commit changes (`git commit -m "Add new thing"`)
4. Push to branch (`git push origin feature/new-thing`)
5. Open a Pull Request
