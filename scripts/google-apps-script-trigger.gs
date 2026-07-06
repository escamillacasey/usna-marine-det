/**
 * Optional: install in Google Sheets (Extensions → Apps Script)
 * Sends a webhook when the sheet is edited so you can run sync + get notified.
 *
 * 1. Set WEBHOOK_URL to your ntfy topic, Slack webhook, or a GitHub repository_dispatch URL
 * 2. Create trigger: onEdit (or time-driven every N minutes for batch edits)
 *
 * For GitHub Actions: use a PAT and repository_dispatch event on your repo.
 */

var WEBHOOK_URL = 'https://ntfy.sh/usna-mardet-data-updated';

function onEdit(e) {
  if (!e || !e.range) return;
  var sheet = e.range.getSheet().getName();
  var payload = {
    source: 'google-sheets',
    sheet: sheet,
    cell: e.range.getA1Notation(),
    timestamp: new Date().toISOString(),
    message: 'MARDET sheet updated — run sync and review website'
  };
  UrlFetchApp.fetch(WEBHOOK_URL, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
}
