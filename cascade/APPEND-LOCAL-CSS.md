# Append to Cascade `local.css`

**File:** `paste-local-css-append.css` (~32 KB)

## Steps

1. In Cascade → **Assets** → `_files/css/` → open **`local.css`**
2. Scroll to the **bottom**
3. If you appended Marines styles before, **delete the old block** (from `/* --- USNA Marines site styles` through the end)
4. Open **`cascade/paste-local-css-append.css`** in this repo → **Select all** → **Copy**
5. **Paste** at the bottom of `local.css`
6. **Submit** and **Publish** `local.css`
7. Republish a test page → hard refresh (Cmd+Shift+R)

Do **not** use `@import url("marines.css")` mid-file — browsers ignore it unless it is line 1.

## Regenerate after CSS changes in the repo

```bash
bash scripts/print-local-css-append.sh > /dev/null
```

Updates `cascade/paste-local-css-append.css` automatically.

## Incremental update (already have Marines styles in local.css)

If `local.css` already contains `/* --- USNA Marines site styles`**, do **not** paste the full `paste-local-css-append.css` again — that duplicates ~1,400 lines.

For a small change (e.g. summer training galleries, prospective Marines path flow), paste only the delta:

**File:** `cascade/paste-local-css-summer-gallery-delta.css` (~170 lines)

1. Open Cascade → `_files/css/local.css`
2. Scroll to the **very bottom**
3. Paste the entire contents of `paste-local-css-summer-gallery-delta.css`
4. Publish `local.css`

You need this block if `.training-gallery`, `.program-block__gallery`, `.commissioning-path`, or `.training-section--evaluation` rules are missing.
