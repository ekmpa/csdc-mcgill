# Calendar

## Automated calendar sync

The homepage featured seminar card is data-driven from `_data/events.yml`.

To enable automatic sync from a published Outlook calendar via GitHub Actions (no app secrets required):

1. Publish the specific Outlook calendar you want to show.
2. Add repository variables (not secrets):
   - `OUTLOOK_CALENDAR_HTML_URL` (for the embedded calendar page)
   - `OUTLOOK_CALENDAR_ICS_URL` (optional; if omitted, script derives it from the HTML URL)
3. Run `.github/workflows/auto-sync-calendar-events.yml` manually once, or wait for the scheduled run.

The sync script is `src/python/sync_outlook_calendar_events.py`.

## Auto-merge behavior

Calendar sync pull requests are configured to auto-merge.

For that to work reliably:

1. Auto-merge must be enabled in the repository settings.
2. Any required branch protection checks on `main` must pass.
3. If required checks do not run for bot-created pull requests, use a dedicated token for PR creation instead of relying only on the default `GITHUB_TOKEN`.