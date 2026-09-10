# Manarion Top 100 Battlor Income

A daily-updated horizontal bar chart of the top 100 battlors on the
[Manarion](https://manarion.com) `highest_damage_spell_rank` leaderboard, ranked
by daily untaxed dust income and colored by guild.

**Live chart:** `https://<your-username>.github.io/<repo-name>/top100battlor.html`
(update this link once GitHub Pages is enabled — see below)

## How it works

`main.py`:

1. Fetches the top 100 leaderboard entries from the Manarion API.
2. Fetches each player's full profile (rate-limited to 1 request/second per
   the API's limit, using `time.sleep(2)` for safety margin).
3. Fetches the guild list and maps each player's `GuildID` to a guild name.
4. Computes each player's daily dust income from their boosts.
5. Sorts everyone by income (descending) and renders a Plotly horizontal bar
   chart, saved as a static, self-contained HTML file at `docs/top100battlor.html`.

A GitHub Actions workflow (`.github/workflows/update.yml`) runs this script
once a day and commits the refreshed HTML file, so the chart stays current
without any manual steps.

## Running it locally

```bash
pip install -r requirements.txt
python main.py
```

This writes `docs/top100battlor.html`, which you can open directly in a browser.

Note: the full run takes a few minutes because of the API's 1 call/second
rate limit across 100 players.

## Hosting / automation setup

1. Push this repo to GitHub.
2. In **Settings → Pages**, set source to "Deploy from a branch," branch
   `main`, folder `/docs`.
3. In **Settings → Actions → General**, under "Workflow permissions," make
   sure "Read and write permissions" is selected (needed so the daily
   workflow can commit the updated HTML back to the repo).
4. The workflow runs automatically every day at 06:00 UTC, or you can
   trigger it manually from the **Actions** tab (`Run workflow`).
5. Once Pages finishes its first build, your chart is public at:
   ```
   https://<your-username>.github.io/<repo-name>/top100battlor.html
   ```

## Files

| File | Purpose |
|---|---|
| `main.py` | Fetches data and generates the chart |
| `requirements.txt` | Python dependencies |
| `docs/top100battlor.html` | Generated chart (output, committed by CI) |
| `.github/workflows/update.yml` | Daily scheduled job |
| `.gitignore` | Standard Python ignores |

## Data source

All player and guild data comes from the public
[Manarion API](https://api.manarion.com). This project is unaffiliated with
Manarion.
