import sys
import requests
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: deploy <roku-url> <password>")
        sys.exit(1)

    roku_url = sys.argv[1].rstrip("/")
    password = sys.argv[2]

    zip_path = Path(__file__).parent.resolve() / "roku_app.zip"
    if not zip_path.exists():
        print("Error: roku_app.zip not found. Run 'uv run build' first.")
        sys.exit(1)

    url = f"{roku_url}/plugin_install"
    with open(zip_path, "rb") as f:
        response = requests.post(
            url,
            auth=requests.auth.HTTPDigestAuth("rokudev", password),
            files={"archive": ("roku_app.zip", f, "application/zip")},
            data={"mysubmit": "Install"},
        )

    if response.status_code == 200:
        print(f"Deployed to {roku_url}")
    else:
        print(f"Deploy failed: HTTP {response.status_code}")
        sys.exit(1)


if __name__ == "__main__":
    main()
