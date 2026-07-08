# Company mentor photos

Photos are keyed by **company number** (not name), so mentor turnover only requires replacing one file.

```bash
# Drop photos in assets/images/incoming/ (any filenames), then:
python3 scripts/import-photos.py --zip ~/Downloads/your-photos.zip
# or
python3 scripts/import-photos.py
```

Output: `company-01.jpg` … `company-36.jpg` in this folder. See `data/photo-import-report.txt` for gaps.

Recommended image size: at least 400×500 px, portrait orientation.

Battalion mapping (6 companies each):

| Battalion | Companies |
|-----------|-----------|
| 1st | 1–6 |
| 2nd | 7–12 |
| 3rd | 13–18 |
| 4th | 19–24 |
| 5th | 25–30 |
| 6th | 31–36 |
