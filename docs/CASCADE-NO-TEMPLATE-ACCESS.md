# No Template access — load Marines CSS via local.css

Use this when you can edit **Assets** but not the USMC **Template**.

## Steps in Cascade

1. Build the bundle on your machine:
   ```bash
   bash scripts/build-cascade-bundle.sh
   ```

2. **Assets** → USMC site → `_files/css/`

3. **Upload** `cascade/marines.css` (keep the filename `marines.css`)

4. **Edit** the existing asset **`local.css`**

5. **Remove** any `@import url("marines.css")` line you added in the middle of the file — browsers ignore `@import` unless it is at the **very top** of the stylesheet.

6. **Append** the Marines bundle at the **bottom** of `local.css`:
   ```bash
   bash scripts/print-local-css-append.sh
   ```
   Copy the terminal output and paste it at the end of `local.css` in Cascade.

   **Or** upload `cascade/marines.css` as a separate file and ask the webmaster to add `<link href="_files/css/marines.css" …>` to the Template head ( `@import` in `local.css` only works at line 1).

7. **Submit** and **publish** `local.css`

8. **Republish** your page (hard refresh in browser: Cmd+Shift+R)

## Verify

Open in browser (must not be 404):

- https://www.usna.edu/USMC/_files/css/marines.css
- https://www.usna.edu/USMC/_files/css/local.css (view source — should end with `@import url("marines.css");`)

On your page, DevTools → Network → CSS → both files should load with status 200.

## JavaScript (optional)

Upload `js/main.js` to `_files/js/main.js`. Adding it requires Template/footer access unless your page **Configure** tab has a script region — ask webmaster if needed.

## After CSS updates

Re-run `bash scripts/build-cascade-bundle.sh`, re-upload `marines.css` to Cascade (replace the asset). No change to `local.css` import line needed.
