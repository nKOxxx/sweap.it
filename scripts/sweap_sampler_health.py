#!/usr/bin/env python3
"""Daily health check for the sweap wire sampler (watchdog: silent when healthy).

Healthy = last ledger frame newer than 26h AND >=5 frames in trailing 26h.
Unhealthy = prints one alert line (cron delivers it). Exit 0 always.
"""
import json, os, time

LEDGER = os.path.expanduser("~/.sweap/wire_ledger.jsonl")
WINDOW_S = 26 * 3600

def main():
    now = time.time()
    if not os.path.exists(LEDGER):
        print(f"WIRE ALERT: ledger missing at {LEDGER}; sampler may be dead")
        return
    frames = []
    with open(LEDGER) as f:
        for line in f:
            try:
                frames.append(json.loads(line))
            except Exception:
                pass
    if not frames:
        print("WIRE ALERT: ledger exists but has zero frames")
        return
    last = max(fr.get("ts", 0) for fr in frames)
    recent = [fr for fr in frames if fr.get("ts", 0) > now - WINDOW_S]
    age_h = (now - last) / 3600
    if age_h > 26:
        print(f"WIRE ALERT: last ledger frame is {age_h:.0f}h old (>{26}h); check cron sweap-wire-sampler / state.db")
    elif len(recent) < 5:
        print(f"WIRE ALERT: only {len(recent)} frames in trailing 26h; sampler may be stalling")
    # else: silent

if __name__ == "__main__":
    main()
