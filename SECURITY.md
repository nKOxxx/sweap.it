# Security Policy

sweap is a local-only tool: it reads and modifies your own database files on
your own machine and performs no network I/O. That property is a design law,
not a promise.

## The local-only property, and how to check it

- All five runtime tools import only the Python standard library. No socket,
  no requests, no urllib, no shell-outs. A regex scan over every runtime path
  returns zero matches.
- The verification script `scripts/repro_receipt.py` is also
  standard-library-only and fully offline; it exercises the product tools by
  running them on a synthetic store it builds in a temp directory.
- The scan command and the hard-socket-firewall test procedure are documented
  in [docs/WARRANTY.md](docs/WARRANTY.md). Unplug the network; sweap behaves
  identically. Verified 2026-10-17, see
  [research/R29_security_audit.md](research/R29_security_audit.md).

## Reporting a vulnerability

Open a GitHub issue and label it `security`. Do not include secrets, store
contents, or auth tokens in the issue; describe the class of problem and a
minimal repro. If the repro requires your store, share a synthetic one.

What counts as a vulnerability here:

- any network egress added anywhere in the runtime path
- quarantine or restore writing outside the declared paths
- a path where `--apply-manifest` executes without the double human gate
- schema-drift cases where apply succeeds silently instead of aborting
- hash verification gaps in restore

## Non-goals

- In-path prompt compression and provider-side pricing are out of scope;
  sweap works on stores at rest.
- The reference-store measurements in `research/` are from the maintainers'
  own machines and are not disclosures.

## Secrets hygiene for contributors

Never commit tokens, cookies, or store files. The repo runs a gitleaks gate
on every push (see `.github/workflows/gitleaks.yml`).
