# Forex Calendar to Discord via GitHub Actions

This repository automatically fetches high-impact forex economic calendar events from Forex Factory and makes them available for your n8n workflow.

## 🎯 How It Works

1. **GitHub Actions** runs daily at 6:30 AM UTC (before your 7 AM Discord message)
2. Fetches forex calendar data from Fair Economy CDN (Forex Factory's data source)
3. Filters for HIGH-IMPACT events only
4. Commits `calendar.json` to the repository
5. Your n8n workflow reads from the GitHub raw URL (whitelisted in n8n Cloud)

## 🚀 Setup Instructions

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `forex-calendar-data` (or whatever you prefer)
3. Set to **Public** (so n8n can access the raw file without authentication)
4. **Important**: Do NOT initialize with README (we'll push our files)
5. Click "Create repository"

### Step 2: Upload Files to GitHub

```bash
# On your computer (with git installed):
git clone https://github.com/YOUR_USERNAME/forex-calendar-data.git
cd forex-calendar-data

# Copy all files from this folder into the repo
# Then commit and push:
git add .
git commit -m "Initial commit - Forex calendar automation"
git push origin main
```

**OR** use GitHub's web interface:
1. Click "uploading an existing file"
2. Upload all files from this folder
3. Commit changes

### Step 3: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the **"Actions"** tab
3. If prompted, click **"I understand my workflows, go ahead and enable them"**
4. You should see "Fetch Forex Calendar" workflow

### Step 4: Test the Workflow

1. Click on "Fetch Forex Calendar" workflow
2. Click **"Run workflow"** > **"Run workflow"** button
3. Wait 30-60 seconds
4. Refresh the page - you should see a green checkmark ✓
5. Go back to your repo main page
6. `calendar.json` should now contain today's high-impact events!

### Step 5: Get the Raw URL

Once `calendar.json` is populated:
1. Click on `calendar.json` in your repo
2. Click the **"Raw"** button
3. Copy the URL - it will look like:
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/forex-calendar-data/main/calendar.json
   ```

**This is the URL you'll use in n8n!**

---

## 📊 Calendar Data Format

The `calendar.json` file contains:

```json
{
  "updated_at": "2024-12-16T06:30:00Z",
  "events": [
    {
      "date": "2024-12-16",
      "time": "13:30",
      "currency": "USD",
      "event": "Retail Sales m/m",
      "impact": "High",
      "forecast": "0.5%",
      "previous": "0.4%",
      "actual": ""
    }
  ]
}
```

---

## 🤖 n8n Workflow Integration

See `n8n-workflow.json` for the complete n8n workflow that:
1. Triggers at 7:00 AM UK time
2. Fetches `calendar.json` from GitHub (using the raw URL)
3. Formats events into Discord message
4. Sends to your Discord webhook

---

## 🔄 Schedule

- **GitHub Actions**: Runs at 6:30 AM UTC daily (automatic)
- **n8n Workflow**: Triggers at 7:00 AM UK time (reads GitHub data)

This ensures fresh data is always available before your Discord message.

---

## 🛠️ Troubleshooting

### GitHub Action fails
- Check the "Actions" tab for error logs
- Common issue: The Fair Economy CDN might be temporarily unavailable
- Solution: Workflow will retry tomorrow automatically

### n8n can't access the file
- Make sure repository is **Public**
- Use the **Raw** URL (starts with `raw.githubusercontent.com`)
- Don't use the regular GitHub page URL

### No events in calendar.json
- The calendar only includes HIGH-IMPACT events
- Some days genuinely have no high-impact news
- Check Forex Factory manually to verify

---

## 📝 Notes

- GitHub Actions has 2,000 free minutes/month (this uses ~1 minute/day = 30 min/month)
- The Fair Economy CDN is Forex Factory's official data source
- Events are in UTC time by default (your n8n workflow converts to UK/NY time)

---

## 🎉 Done!

Once set up:
1. ✅ GitHub automatically fetches calendar daily
2. ✅ n8n reads from GitHub (no network restrictions)
3. ✅ Discord gets formatted high-impact news at 7 AM

No more blocked domains, no API keys needed, completely free!
