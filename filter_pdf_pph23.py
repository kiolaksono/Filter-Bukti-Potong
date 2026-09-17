name: Build EXE

# Jalan otomatis tiap push ke main/master, atau bisa dipicu manual
# lewat tab "Actions" -> "Build EXE" -> "Run workflow".
# Kalau push disertai tag yang diawali "v" (misal v1.0.0), hasil .exe
# otomatis dilampirkan ke GitHub Release.
on:
  push:
    branches: [main, master]
    tags: ["v*"]
  workflow_dispatch: {}

jobs:
  build:
    runs-on: windows-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v5

      - name: Setup Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pyinstaller

      - name: Build pph23_extraction.exe
        run: >
          pyinstaller --onefile --console
          --name pph23_extraction
          pph23_extraction.py

      - name: Build filter_bukpot.exe
        run: >
          pyinstaller --onefile --console
          --name filter_bukpot
          filter_bukpot.py

      - name: Upload pph23_extraction artifact
        uses: actions/upload-artifact@v4
        with:
          name: pph23_extraction-windows-exe
          path: dist/pph23_extraction.exe

      - name: Upload filter_bukpot artifact
        uses: actions/upload-artifact@v4
        with:
          name: filter_bukpot-windows-exe
          path: dist/filter_bukpot.exe

      - name: Attach to GitHub Release
        if: startsWith(github.ref, 'refs/tags/v')
        uses: softprops/action-gh-release@v2
        with:
          files: |
            dist/pph23_extraction.exe
            dist/filter_bukpot.exe
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
