import sys
import shutil
from pathlib import Path
from urllib.request import urlretrieve


OUTPUT_DIR = Path("licenses")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LICENSE_URL = "https://raw.githubusercontent.com/python/cpython/main/Doc/license.rst"
rst_dest = OUTPUT_DIR / "CPython-License.rst"
print(f"Downloading {LICENSE_URL}...")
urlretrieve(LICENSE_URL, rst_dest)
print(f"  Saved to {rst_dest}")

base_prefix = Path(sys.base_prefix)
license_path = base_prefix / "LICENSE.txt"

if license_path.exists():
    license_dest = OUTPUT_DIR / "Python-License.txt"
    shutil.copy(license_path, license_dest)
    print(f"  Copied {license_path} to {license_dest}")
else:
    print(f"  WARNING: Could not find LICENSE.txt in {base_prefix}")
