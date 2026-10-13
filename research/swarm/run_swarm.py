#!/usr/bin/env python3
"""sweap.it persona swarm orchestrator: 100 persona verdicts, serial free-lane dispatch.

Laws honored: JSONL ledger (orrery law), needle acceptance (hf_dispatch law),
deterministic corpus (ensemble law), repo glyph-clean (house law).
"""
import json, os, re, subprocess, sys, time
from typing import Callable, Optional

SW = os.path.expanduser("~/sweap.it/research/swarm")
RAW = f"{SW}/raw"; os.makedirs(RAW, exist_ok=True)
personas = json.load(open(f"{SW}/personas.json"))
template = open(f"{SW}/persona_template.txt").read()
ledger = f"{SW}/swarm_ledger.jsonl"
stats_env = dict(os.environ, HF_STATS=f"{SW}/swarm_stats.tsv")

def render(p):
    b = template
    for k, v in [("PID", p["id"]), ("ROLE", p["role"]), ("SEGMENT_NAME", p["segment_name"]),
                 ("SPEND", p["monthly_llm_spend_usd"]), ("SESSIONS", p["agent_sessions_per_week"]),
                 ("PAIN", p["context_pain_0_10"]), ("SKEP", p["skepticism"]),
                 ("BUDGET", p["budget_authority"]), ("TOP_PAIN", p["top_pain"])]:
        b = b.replace("{" + k + "}", str(v))
    path = f"{SW}/brief_{p['id']}.txt"
    open(path, "w").write(b)
    return path

def parse(raw):
    t = raw.replace("\u2014", "; ")  # glyph law at ingestion
    def last(pat: str, cast: Callable = str, default: Optional[object] = None):
        m = re.findall(pat, t)
        return cast(m[-1]) if m else default
    verdict = last(r"VERDICT:\s*(INSTALL|TRY|IGNORE|HOSTILE)")
    resonance = last(r"RESONANCE:\s*(\d{1,3})", int, -1)
    pay = last(r"WOULD-PAY:\s*\$?\s*(\d+)", int, -1)
    def line_after(label):
        m = re.findall(label + r"[^\S\n]*[^\n]+", t)
        return m[-1].split(":", 1)[1].strip() if m else None
    return verdict, resonance, pay, line_after("PITCH-PROOF"), line_after("MISSING"), line_after("OBJECTION")

def dispatch(p, brief, budget):
    out = f"{RAW}/{p['id']}_raw.txt"
    r = subprocess.run(["~/.hermes/scripts/hf_dispatch.sh".replace("~", os.path.expanduser("~")),
                        brief, "deepseek", f"SWEEPIT_{p['id']}", str(budget), out],
                       capture_output=True, text=True, timeout=budget + 120, env=stats_env)
    raw = open(out).read() if os.path.exists(out) else ""
    return r.returncode, raw, out

if __name__ == "__main__":
    done, failed = 0, []
    t0 = time.time()
    seen = set()
    if os.path.exists(ledger):
        for ln in open(ledger):
            try:
                seen.add(json.loads(ln)["id"])
            except Exception:
                pass
    with open(ledger, "a") as L:
        for p in personas:
            if p["id"] in seen:  # resume support
                done += 1
                continue
            brief = render(p)
            rc, raw, out = dispatch(p, brief, 300)
            verdict, res, pay, proof, missing, obj = (None,) * 6
            if rc == 0:
                verdict, res, pay, proof, missing, obj = parse(raw)
            if verdict is None:  # one retry
                time.sleep(5)
                rc, raw, out = dispatch(p, brief, 420)
                verdict, res, pay, proof, missing, obj = parse(raw)
            if verdict is None:
                failed.append(p["id"])
                continue
            L.write(json.dumps({"ts": time.strftime("%FT%T"), "id": p["id"],
                                "segment": p["segment"], "segment_name": p["segment_name"],
                                "skepticism": p["skepticism"], "pain": p["context_pain_0_10"],
                                "spend": p["monthly_llm_spend_usd"],
                                "verdict": verdict, "resonance": res, "would_pay": pay,
                                "pitch_proof": proof, "missing": missing, "objection": obj,
                                "raw": out}) + "\n")
            L.flush()
            done += 1
            print(f"[{done}/100] {p['id']} {p['segment']} {verdict} res={res} pay=${pay}", flush=True)

    print(f"DONE in {int(time.time()-t0)}s; ok={done - len(failed)} failed={failed}")
