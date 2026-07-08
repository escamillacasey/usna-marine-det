# Company mentor portraits (Cascade — public www)

Copies of `assets/images/intranet/mentors/company-*.jpg` for upload to Cascade when publishing on **Marine Corps - Public** (`www.usna.edu/MarineCorps`).

**Cascade path:** `_files/images/public/mentors/`

The `intranet/mentors/` folder is blocked by USNA WAF on the public site. Use this folder for www deploys; keep `intranet/mentors/` for the real intranet host.

After roster or photo changes, refresh from intranet:

```bash
cp assets/images/intranet/mentors/company-*.jpg assets/images/public/mentors/
```
