#!/usr/bin/env python3
"""
Fetch high-impact forex calendar events from Forex Factory's data source.
Outputs a JSON file with today's and tomorrow's high-impact events.
"""

import json
import requests
from datetime import datetime, timedelta
import sys

def fetch_forex_calendar():
    """Fetch forex calendar from Fair Economy CDN (Forex Factory's data source)"""
    
    # Fair Economy CDN - Forex Factory's data source
    url = "https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    try:
        print(f"Fetching calendar data from {url}...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✓ Successfully fetched {len(data)} total events")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching calendar: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"✗ Error parsing JSON: {e}")
        sys.exit(1)

def filter_high_impact_events(events):
    """Filter for today's and tomorrow's HIGH impact events only"""
    
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    
    filtered = []
    
    for event in events:
        try:
            # Parse the event date
            event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
            
            # Check if event is today or tomorrow
            if event_date not in [today, tomorrow]:
                continue
            
            # Check if it's HIGH impact (Forex Factory uses 'High' string or impact level 3)
            impact = event.get('impact', '').strip()
            
            # High impact is typically marked as 'High' or with 3 in some feeds
            if impact.lower() != 'high' and event.get('volatility', 0) < 3:
                continue
            
            # Clean up the event data
            cleaned_event = {
                'date': event.get('date'),
                'time': event.get('time'),
                'currency': event.get('country', ''),  # Country code (USD, EUR, GBP, etc.)
                'event': event.get('title', ''),
                'impact': impact,
                'forecast': event.get('forecast', ''),
                'previous': event.get('previous', ''),
                'actual': event.get('actual', '')
            }
            
            filtered.append(cleaned_event)
            
        except (KeyError, ValueError) as e:
            print(f"Warning: Skipping malformed event: {e}")
            continue
    
    print(f"✓ Filtered to {len(filtered)} high-impact events")
    return filtered

def save_calendar(events, filename='calendar.json'):
    """Save filtered events to JSON file"""
    
    output = {
        'updated_at': datetime.utcnow().isoformat() + 'Z',
        'events': events
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved {len(events)} events to {filename}")

def main():
    print("=" * 60)
    print("Forex Factory Calendar Fetcher")
    print("=" * 60)
    
    # Fetch calendar data
    all_events = fetch_forex_calendar()
    
    # Filter for high-impact events
    high_impact = filter_high_impact_events(all_events)
    
    # Save to file
    save_calendar(high_impact)
    
    print("=" * 60)
    print("✓ Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
