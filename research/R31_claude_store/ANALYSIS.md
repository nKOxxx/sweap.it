# R31 - Claude Code local store: where the weight hides

Date: 2026-10-17. Method: hub-side byte census on live transcripts (2 files,
1.82 MB total) -> blind DeepSeek worker analysis (needle CLAUDE-STORE-ANALYSIS-OK,
3m53s) -> hub recount of every worker number. Raw capture: /tmp/claude_store_raw.txt
(worker verbatim). This file = hub ledger + worker analysis with corrections applied.

## HUB LEDGER (measured, one machine, 2026-10-17)

Data: ~/.claude/projects/*/. Big file = 1.55 MB, 1 session, 41 user turns, 626 lines.

| Component | Bytes | Share | Class |
|---|---|---|---|
| toolUseResult (tool outputs, structured envelope, on user records) | 256K | 16.5% | dual envelope of tool_result |
| message.content blocks (canonical conversation) | 436K | 28.1% | canonical |
|  ... of which thinking signatures (139 blocks, thinking text EMPTY) | 234.7K | 15.1% | vendor crypto |
|  ... of which tool_use inputs | 106K | 6.8% | canonical |
|  ... of which tool_result (flattened outputs) | 75K | 4.8% | dual envelope of toolUseResult |
|  ... of which text | 12K | 0.8% | canonical |
| usage receipts (token metering, on all 347 assistant records) | 222K | 14.3% | bookkeeping |
| wireToolInputs (cwd-resolved input envelope, on assistant records) | 100K | 6.4% | dual envelope of tool_use |
| attachment records (147: deferred tool lists, rendered reminders) | 187K | 12.0% | scaffolding |
| per-record metadata (sessionId, uuid, parentUuid, cwd, timestamp, ...) | ~130K | 8.4% | scaffolding |
| last-prompt + misc | ~55K | 3.5% | mixed |

## HUB RECOUNT CORRECTIONS TO WORKER OUTPUT

1. CORRECTED: worker claimed uuid and requestId are constant across the session.
   Measured: uuid 626 distinct values, requestId 130 distinct. Constants are:
   sessionId, cwd, version, userType, entrypoint, gitBranch, advisorModel.
   Effect on conclusions: none (constant-field hoisting estimate shrinks slightly).
2. ADDED (worker missed, hub found): usage receipts = 222K on 347 assistant records,
   only 130 distinct payloads => ~217 receipts are repeats of an earlier receipt.
   Largest single recoverable-by-repetition class found so far in this file.
3. VERIFIED EXACT: worker T3 arithmetic (75+230K band, 4.8%/14.8%), T1 verdicts,
   the 3.4x toolUseResult:tool_result size ratio (256K vs 75K).
4. HUB PROBE (post-worker): whole assistant messages byte-compared: 0/347 exact
   repeats. Combined with 0/131 inputs and 0/131 outputs: NO byte-identical
   duplication exists anywhere tested in this store. Hermes-class disease absent.

## CENTRAL VERDICT (survives recount)

Claude Code does not have the Hermes disease (byte-identical copies). It has a
different pattern: dual-envelope storage (same tool call/output recorded twice in
different shapes, inputs cwd-resolved, outputs structured-vs-flattened), heavy
bookkeeping (usage receipts 222K), vendor crypto where thinking text would be
(234.7K signatures, 0 bytes of thinking text), and per-line scaffolding. Worker
estimate of reversibly recoverable bytes: 75-230K (~5-15%), UNPROVEN - requires a
quarantine-restore test on a copy before any claim. Falsifiers preserved below.

---

## WORKER ANALYSIS (DeepSeek, verbatim after extraction; see corrections above)

Query: # RESEARCH BRIEF ;  LLM vendor session stores: where the weight hides 
(Claude Code case study, GPT/Codex outlook)

You are a research analyst. You have NO access to our machine, code, or store. 
Everything you need is in this brief. Work from first principles + your training
knowledge. Use UNKNOWN rather than inventing. Every outside-of-brief claim you 
make gets a confidence tag [HIGH]/[MED]/[LOW] plus source type (training 
knowledge, documented behavior, speculation). Every output you derive gets 
[HYPOTHETICAL].

Context: we built sweap.it, a tool that weighs an LLM agent's persistent session
store, removes duplication reversibly (quarantine, full undo), and prices memory
lapses. Our measured anchor case is the Hermes agent's SQLite store. The open 
question: do OTHER vendors' local stores carry the same class of hidden weight? 
The user has started running Claude Code and Codex CLI on one Mac to find out.

## MEASURED ANCHORS [ANCHOR] ;  all numbers below were measured on one machine, 
2026-10-17. Recompute anything you use; attack anything that looks wrong.

### A. Hermes (our baseline)
- A1 [ANCHOR] Store: single SQLite DB (agent state), 206.5 MB after diet.
- A2 [ANCHOR] On the tested store schema, every thinking blob was stored twice, 
across all models tested: 9,456 rows, 26 MB.
- A3 [ANCHOR] Diet v2 removed 37.57 MB (244.1 -> 206.5 MB), 0 bytes of 
information lost (duplicates only), fully reversible via quarantine restore.
- A4 [ANCHOR] Models on that lane: GLM family, DeepSeek, MiniMax.

### B. Claude Code local transcripts (2 session files, JSONL, 1.82 MB total; the
big one: 1.55 MB, 1 session, 41 user turns)
- B1 [ANCHOR] Structure: one JSON object per line. Record types seen: user, 
assistant, attachment, atis-latch, last-prompt, queue-operation, cost-state.
- B2 [ANCHOR] Thinking blocks: 139 blocks in the big file. The `thinking` text 
field is EMPTY (0 bytes) in every single block. Each block instead carries a 
`signature` field: 234,732 bytes total in that file, avg 1,688 B, min 976, max 
9,268 (vendor cryptographic signatures, not recoverable text).
- B3 [ANCHOR] Tool inputs stored twice per call, in two DIFFERENT envelopes, 
0/131 byte-identical:
  - copy 1: assistant record -> message.content[] -> {type: tool_use, input: 
{...}}
  - copy 2: same assistant record -> top-level wireToolInputs -> {tool_use_id: 
{...}}
  - observed envelope difference (real example, [ANCHOR]):
copy 1 input: {"command": "cat program.md", "description": "Read 
program.md"}
copy 2 input: {"command": "cd /Users/ares/autoresearch-mlx && cat 
program.md", "description": "Read program.md"}
- B4 [ANCHOR] Tool outputs stored twice per call, also 0/131 byte-identical:
  - copy 1: user record -> message.content[] -> {type: tool_result, tool_use_id,
content: "..."}
  - copy 2: same user record -> top-level toolUseResult: {"stdout": "...", ...} 
(structured result object; observed wrapping: raw string content vs {"stdout": 
...} object)
- B5 [ANCHOR] Byte ledger for the 1.55 MB file: content blocks (message.content 
JSON) = 436 KB total (thinking 242K incl. signatures, tool_use 106K, tool_result
75K, text 12K). Non-message scaffolding ~= 1.1 MB: toolUseResult 256K, 
wireToolInputs 100K, attachment records 187K (147 records: deferred tool lists, 
rendered system-reminders), per-record session metadata ~130K (sessionId, uuid, 
parentUuid, cwd, timestamp, gitBranch, requestId, version, userType, entrypoint,
advisorModel ;  repeated on every line), last-prompt 14K, misc.
- B6 [ANCHOR] Second file (264 KB, 7 turns) shows the same pattern 
proportionally.

### C. Codex CLI (OpenAI)
- C1 [ANCHOR] Fresh install: ~/.codex exists, 352 KB, skills only, ZERO session 
files on disk yet. Its transcript format is UNKNOWN to us (sessions are expected
under ~/.codex/sessions/ once the first run happens, but that is [ASSUMPTION]).

## YOUR TASKS

### T1 ;  Classification. For each Claude Code storage pattern in B2-B5, 
classify:
(i) DUPLICATION: same information recoverable from elsewhere in the same file 
(state the recovery path precisely);
(ii) SCAFFOLDING: functional metadata required for session resume/replay/UI 
(which fields are strictly necessary vs redundant, and why ;  attack your own 
answer);
(iii) VENDOR CRYPTO: untouchable (signatures).
The money question: B3/B4 claim "stored twice" ;  but 0/131 copies are 
byte-identical. Is the second envelope (a) pure redundancy (recoverable from 
copy 1 + local context like cwd), (b) partially unique (carries data copy 1 
lacks ;  e.g. structured fields, rewritten commands), or (c) a view, not a copy? 
Give your per-pattern verdict with reasoning, and the precise honest phrasing a 
vendor-paranoid reader would accept instead of "stored twice". Demand-style 
rigor: state FALSIFIED IF lines for each verdict.

### T2 ;  The honest claim. If we wanted to tell Claude Code users "your 
transcripts carry hidden weight", what claim is exactly supportable from B1-B6 
alone? Draft the claim in <=3 sentences, no marketing language, every number 
traceable to an anchor. Include a FALSIFIED IF.

### T3 ;  Recoverable-bytes estimate [HYPOTHETICAL]: if a reversible, 
quarantine-based dedup ran on the big Claude file, what byte range is plausibly 
recoverable? Show arithmetic per component (B3/B4 envelopes, metadata, 
attachments), state assumptions explicitly, and give a low/high band, not a 
point. What % of the 1.55 MB is that? What could BREAK if copy 2 were 
quarantined instead of deleted (name the consumers: session resume, /rewind, 
subagent replay, export ;  tag each [LOW]/[MED]/[HIGH] confidence).

### T4 ;  Cross-vendor comparison table: Hermes vs Claude Code. Rows: storage 
engine; what gets persisted for thinking; tool input persistence; tool output 
persistence; session scaffolding; duplication type (byte-identical vs 
dual-envelope); reversibility mechanics we have proven. Every cell gets a source
tag:  /  /  / [UNKNOWN].

### T5 ;  Codex outlook: from documented behavior of OpenAI Codex CLI (training 
knowledge, tag everything), what should we expect its session persistence to 
look like, what are the first three measurements to take once a session file 
exists, and what pattern would make it MORE or LESS dedupable than Claude 
Code's? UNKNOWN over invention.

### T6 ;  Adjacent vendors in one short paragraph each (training knowledge, 
tagged): Gemini CLI, Cursor, Aider, OpenAI desktop ChatGPT. Where do they 
persist sessions locally on macOS, and which are worth measuring next? UNKNOWN 
over invention.

### T7 ;  Attack OUR anchor: A2 says "stored twice" for Hermes with 
byte-identical confidence. What observation would falsify the parallel we're 
implying between Hermes and Claude Code (i.e., that the same disease is present 
in a different body)?

## OUTPUT CONTRACT
- Final line of output, exactly: CLAUDE-STORE-ANALYSIS-OK
- Markdown. No site copy, no social posts, no marketing language anywhere. This 
is internal research.
- Plain-language summary section at the END written for a non-technical founder:
short paragraphs, no jargon left unexplained, no project shorthand.
- Every table cell sourced or tagged UNKNOWN. Every derived number 
[HYPOTHETICAL]. FALSIFIED IF lines wherever a claim could die.
Initializing agent...

I'll start by loading the on-domain skill (sweap-stack) since this brief
is squarely about the store-weighing product laws it encodes, then
produce the analysis.

Skill loaded ;  its honesty gates (cross-store "not universal" check,
"envelope scaffolding never claimed as dead weight," banned-copy law) map
directly onto this brief, so I'll hold the analysis to those standards.
This is a pure analysis deliverable from the brief's anchors + training
knowledge; per the brief I'm not inspecting the machine.

LLM vendor session stores: where the weight hides
Claude Code case study, GPT/Codex outlook ;  internal research

Legend: [ANCHOR] = measured in the brief. [HYPOTHETICAL] =
derived/estimated, must not be quoted as fact. [HIGH]/[MED]/[LOW] =
confidence, followed by source type {training knowledge | documented
behavior | speculation}.

T1 ;  Classification of Claude Code storage patterns (from B2–B5)

B2 ;  Thinking blocks: empty text + vendor signature → VENDOR CRYPTO
The thinking field is 0 bytes in all 139 blocks; each block instead
carries a signature (234,732 B total, avg 1,688 B). The only
recoverable reading of this sample: **Claude Code does not persist
chain-of-thought text on disk at all** on this file. What's left is a
tamper-evident signature ;  integrity metadata the client uses to prove
the (hidden) thinking wasn't edited, not a text payload. Tag: **VENDOR
CRYPTO, untouchable.**

- Why not recoverable: a signature is not a serialization of the
thinking; stripping it loses integrity verification and there is no text
to reclaim.
- Note the sharp contrast with our own A2 (Hermes persists thinking,
twice). Here the vendor's COT is withheld, not duplicated. This alone
weakens any "same disease everywhere" narrative (see T7).

> FALSIFIED IF: any signature block decodes/decompresses to readable
chain-of-thought (i.e., it is an obfuscated text payload rather than a
digest), or the vendor's server accepts a resumed session with signatures
stripped.
> FALSIFIED IF: a later sample of Claude Code shows a populated
thinking text field (version/feature drift), turning this into a
"thinking IS persisted" problem rather than a crypto-only one.

B3 ;  Tool inputs in two envelopes, 0/131 byte-identical → **(b)
partially unique bytes, informationally redundant via cwd** (honest
label: a resolved clone / derived view, NOT "stored twice")
Copy 1 (canonical): message.content[] → {type: tool_use, input}. Copy 2
(top-level): wireToolInputs → {tool_use_id: input}. The observed pair:

- copy 1 input: {"command": "cat program.md", ...}
- copy 2 input: `{"command": "cd /Users/ares/autoresearch-mlx && cat
program.md", ...}`

The second copy is the same invocation, **rewritten / expanded against
the recorded working directory** (cwd is itself a per-record metadata
field, so it's present in the same file). It is therefore not
byte-identical ;  but the unique bytes are reconstructable from copy 1
plus the cwd field already in the file. That is a deterministic
transform, i.e. redundancy in the information-theoretic sense, stored as
distinct bytes.

Verdict: (a)→(b) hybrid. At the byte level it's partially unique; at
the information level it's recoverable (copy 1 + cwd ⇒ copy 2). It is
best described as a cwd-resolved derived view of the primary copy,
physically occupying its own bytes.

> FALSIFIED IF: any copy-2 input contains a value not derivable from copy
1 + the recorded context (cwd, branch, timestamp) ;  e.g., a genuinely
different command, an extra argument, a rewrite no cwd-prefix rule can
produce. Then it carries unique information and is NOT dedupable under a
lose-nothing rule.
> FALSIFIED IF: quarantining copy 2 breaks any consumer that copy 1
cannot restore (then it's not redundant in the operational sense).

B4 ;  Tool outputs in two envelopes → **(b) partially unique; the
structured envelope carries payload copy 1 likely lacks**
Copy 1: `message.content[] → {type: tool_result, tool_use_id, content:
"<string>"} (flattened). Copy 2: top-level toolUseResult: {"stdout":
...}` (structured object). The brief's [ANCHOR] is that the wrapping
differs (raw string vs structured object); the two copies carry the *same
stdout content but in different shapes*.

**The critical number: copy 1 tool_result content = 75 KB; copy 2
toolUseResult = 256 KB. The second envelope is ~3.4× larger** than
the primary copy. That is only explainable if copy 2 carries fields copy
1 lacks ;  stderr, exit codes, file-edit records, tool-specific structured
output ;  not just a reshaped stdout. So on the evidence, the stdout
substring is redundant, but a large share of copy 2's 256 KB is **unique
structured data with no twin in copy 1. Honest verdict: (b) partially
unique**, and the recoverable slice is capped by the 75 KB overlap, not
the 256 KB envelope.

> FALSIFIED IF: copy 2, once flattened, turns out to byte-cover
essentially all of copy 1 (i.e., copy 1 is a truncated subset of a
fully redundant-enough copy 2) ;  then the recoverable slice grows toward
the 75 KB bound rather than the small band I give in T3.
> FALSIFIED IF: a toolUseResult field (stderr, exit code) is shown to
ALSO appear in copy 1 ;  collapsing my "unique" share.

B5 ;  Per-line session metadata & attachments → **SCAFFOLDING, with a
repeated-invariant sub-category that is informationally duplicated but
functionally load-bearing**
Two distinct things under one ~1.1 MB scaffolding umbrella:

- Repeated-invariant metadata (~130 KB): `sessionId, uuid,
parentUuid, cwd, timestamp, gitBranch, requestId, version, userType,
entrypoint, advisorModel` repeated on every line. The constant fields
(sessionId, uuid, version, userType, cwd, gitBranch, requestId) have the
same value on all 41 turns ;  that is genuine byte duplication (value
N twice), the closest analogue to Hermes's A2/A3. BUT it is
load-bearing: each JSONL line is self-describing so a
streaming/partial-tail resume and out-of-order read can rehydrate without
a header. Classification: (ii) SCAFFOLDING that is partly redundant ; 
the redundancy is real, but deleting it (rather than re-deriving it on
read via a header scheme) changes replay semantics.
- **Attachment records (187 KB, 147 records: deferred tool lists,
rendered system-reminders) and last-prompt (14 KB)**:
rendered/derived UI artifacts, re-derivable in principle from the
conversation but their regeneration is unproven and they serve
display/resume. Classification: (i)/(ii) borderline; on product law
(envelope scaffolding never claimed as dead weight) these are **not
claimable** without a source-of-truth proof.

> FALSIFIED IF: a resume//rewind/subagent-replay path reconstructs the
full conversation from message.content alone with zero dependence on
the per-line metadata or attachments ;  then the metadata/attachment bytes
are pure recoverable duplication and my "don't touch" stance is too
conservative.

Money question, consolidated: "Stored twice" is **not accurate for
this file**, because 0/131 copies are byte-identical. The demand-rigorous
phrasing a vendor-paranoid reader accepts:

> The same tool invocation/output is recorded in two envelopes ;  the
canonical message.content blocks and top-level
wireToolInputs/toolUseResult fields ;  but the second envelope is **a
derived, re-shaped view**, not a byte copy: tool inputs are cwd-resolved
rewrites (reconstructable from copy 1 + the recorded working directory),
and tool outputs are a structured object that may carry fields the
flattened copy lacks. So this is **dual-envelope representation with a
deterministic transform**, not byte-identical duplication. The genuinely
byte-redundant share is dominated by repeated-invariant metadata and the
overlap between the two envelopes ;  both smaller and riskier to reclaim
than Hermes's case.

T2 ;  The honest claim (≤3 sentences, every number → anchor)

> On one measured 41-turn Claude Code session transcript (B1: 1.55 MB),
the same tool invocations and outputs are recorded in two envelopes ; 
the canonical message.content blocks plus top-level
wireToolInputs/toolUseResult fields (B5: ≈356 KB combined) ;  and ≈130
KB of session metadata is repeated once per line (B5). That
second-envelope weight is a **transformed view, not a byte copy (B3/B4:
0/131 match)**, and roughly 235 KB of vendor signatures is not
recoverable text (B2), so unlike our Hermes store (A3: 37.57 MB removed,
zero loss) there is no proven zero-loss quarantine yet. The question
of whether this weight can be removed ;  and how much ;  is untested, not
demonstrated.

> FALSIFIED IF: this claim dies if re-measurement shows the second
envelope carries genuinely unique fields (stderr/exit codes/cwd-rewrites
not derivable from copy 1 + context), which would collapse the
recoverable-byte estimate toward zero; or if a quarantine test of the
redundant envelope turns out to lose bytes other consumers need (then
it is not the zero-cost weight Hermes's store has).

T3 ;  Recoverable-bytes estimate [HYPOTHETICAL], with consumers at risk

Assumption set (explicit):
1. Recoverable = bytes you can drop and restore with a
wel-with-zero-information-loss rule (same standard as Hermes A3). Any
byte with no twin in copy 1 + recorded context is treated as **not
recoverable** (lose-nothing floor).
2. Only components with a stated believe-redundancy model are counted;
attachments and the ~439 KB "misc" remainder are excluded ([UNKNOWN]
composition, never claimed ;  product law).
3. All figures below are band estimates off the B5 ledger for the 1.55 MB
file = ~1,550 KB.

Component: wireToolInputs
Size (B5): 100 KB
Redundancy model: copy 2 = cwd-resolved clone of copy 1 tool_use;
  derivable from copy 1 + cwd field
Recoverable LOW: 60 KB
Recoverable HIGH: 100 KB
Rationale: High: full envelope verifiable-against-copy1. Low: only
  confirmed-derivable delta.
Component: toolUseResult
Size (B5): 256 KB
Redundancy model: stdout overlaps copy 1 (75 KB); rest is unique
  structured fields
Recoverable LOW: 15 KB
Recoverable HIGH: 60 KB
Rationale: Bounded by the 75 KB primary copy; high assumes ~80%
  byte-overlap of that 75 KB; low assumes only exact-matching stdout
  substrings. The 256→75 KB gap is mostly unique data, not waste.
Component: per-line metadata
Size (B5): 130 KB
Redundancy model: constant fields repeated per turn; hoistable if
  read-path is re-designed
Recoverable LOW: 0 KB
Recoverable HIGH: 70 KB
Rationale: Low: don't touch (line-independence is functional). High: hoist
  provably-constant fields (sessionId, uuid, version, userType, cwd,
  gitBranch, requestId) only if a restore pass re-expands on read ;  [LOW]
  confidence it's safe.
Component: attachments (187 KB)
Size (B5): ; 
Redundancy model: excluded
Recoverable LOW: 0
Recoverable HIGH: 0
Rationale: UI/render scaffolding; no regeneration proof.
Component: misc (~439 KB)
Size (B5): ; 
Redundancy model: excluded
Recoverable LOW: 0
Recoverable HIGH: 0
Rationale: [UNKNOWN] composition; never claim.
Component: Total
Size (B5):
Redundancy model:
Recoverable LOW: ≈ 75 KB
Recoverable HIGH: ≈ 230 KB
Rationale:
Component: % of 1.55 MB
Size (B5):
Redundancy model:
Recoverable LOW: ≈ 4.8%
Recoverable HIGH: ≈ 14.8%
Rationale: ~5–15% band

Headline [HYPOTHETICAL]: roughly 75–230 KB, i.e. ~5–15% of
the 1.55 MB file, is plausibly recoverable ;  **and the largest single
line-item, the 256 KB toolUseResult, is mostly unique payload, not
waste. Note this is structurally different from Hermes: there is no
duplicated-thinking class** here (B2 thinking is empty), which was our
biggest line-item (A2: 26 MB). The Claude disease is smaller and riskier
to harvest.

**What breaks if copy 2 is quarantined (not deleted) ;  named consumers:**

Consumer: session resume
Wiring evidence: Whether resume rehydrates from message.content (copy 1)
  or the top-level wire fields is unobserved
Risk if copy 2 quarantined: If it reads wire fields, resume degrades until
  restore. If it reads copy 1, no impact.
Tag: [MED]
Consumer: /rewind
Wiring evidence: Rebuilds a past turn's tool state; both copies live on
  the same record
Risk if copy 2 quarantined: Depends which copy feeds the rebuild; likely
  copy 1
Tag: [MED]
Consumer: subagent replay
Wiring evidence: Structured toolUseResult is the plausible source for
  structured subagent replay
Risk if copy 2 quarantined: Quarantine likely breaks it if structured
  fields are read
Tag: [MED-HIGH]
Consumer: export
Wiring evidence: Markdown/export almost certainly reads canonical
  message.content (copy 1)
Risk if copy 2 quarantined: Copy 2 quarantine harmless to exports
Tag: [LOW]
Consumer: reverse consumer
Wiring evidence: If the wire fields are what's re-sent to the API on
  resume and copy 1 is actually the derived one, the risk direction flips
Risk if copy 2 quarantined: Then copy 1 is the quarantine target, not copy
  2
Tag: [MED]

Because copy 2 (top-level wire) looks like a cache/derivation aid rather
than the canonical record, **quarantine risk is plausibly LOW-MED ;  but
with zero wiring evidence every read-path is at least [MED].** The honest
next step on a real machine is: copy the file, quarantine copy 2,
exercise each consumer one at a time, restore ;  mirroring our own R26
demo-on-copy protocol. Nothing here is a claim until that runs.

> FALSIFIED IF: any single consumer fails a quarantine-then-restore
round-trip (restore not zero-work). Then copy 2 is not isomorphic
redundancy and the ~75–230 KB band collapses toward 0.
> FALSIFIED IF: re-measurement shows copy 1 tool_result is large enough
to twin most of toolUseResult (i.e., my 75 KB overlap bound is wrong
and the true overlap approaches the envelope), pushing the high band up
toward ~300 KB / ~19%.

T4 ;  Cross-vendor comparison: Hermes vs Claude Code

Row: Storage engine
Hermes (our lane): Single SQLite DB (agent state) ;  [measured, one
  machine] A1
Claude Code: JSONL transcripts (.claude/projects/**/*.jsonl) ;  [measured,
  one machine] B1
Row: Thinking persistence
Hermes (our lane): Persisted, byte-identical twice (reasoning +
  reasoning_content twin columns), 26 MB on 9,456 rows ;  [measured] A2
Claude Code: Not persisted as text (0-byte thinking); only vendor
  signature (234.7 KB) ;  [measured] B2
Row: Tool input persistence
Hermes (our lane): [UNKNOWN] (not anchored in brief)
Claude Code: Dual envelope ;  copy 1 message.content + copy 2
  wireToolInputs (cwd-resolved), 0/131 byte-identical ;  [measured] B3
Row: Tool output persistence
Hermes (our lane): [UNKNOWN]
Claude Code: Dual envelope ;  copy 1 flattened string + copy 2 structured
  toolUseResult (3.4× larger) ;  [measured] B4
Row: Session scaffolding
Hermes (our lane): SQLite schema (rows/columns) ;  [measured]
Claude Code: Per-line metadata repeated on every record (~130 KB),
  attachment records (187 KB) ;  [measured] B5
Row: Duplication type
Hermes (our lane): Byte-identical duplicate columns ;  [measured, one
  machine] A2/A3
Claude Code: Dual-envelope with deterministic transform
  (resolved/reshaped), plus repeated-invariant metadata ;  [measured]
  B3/B4/B5
Row: Reversibility proven
Hermes (our lane): Yes ;  quarantine + full undo, 37.57 MB removed
  (244.1→206.5), 0 bytes lost, restore verified ;  [measured] A3
Claude Code: Not tested ;  no quarantine/restore has run; risk to
  resume/rewind/subagent unproven ;  [UNKNOWN]

Source tags per cell: every Claude cell is [measured, one machine, two
files]. Every Hermes cell is [measured, one machine]. The two [UNKNOWN]
cells (Hermes tool I/O persistence) are genuinely not in the brief ; 
flagged, not guessed.

T5 ;  Codex CLI outlook (all training knowledge, tagged)

- Session persistence (expected): OpenAI's open-source Codex CLI
(Rust) writes per-session artifacts under ~/.codex/sessions/ ;  a
session/metadata file (TOML) plus an append-only JSONL rollout of the
trajectory, readable for codex resume. [MED, training knowledge].
- Thinking: Codex drives the Responses API, where chain-of-thought is
returned as an **encrypted/protected reasoning field (encrypted_content
/ summary). So latent reasoning should not be (recoverable) plaintext
on disk** ;  at most a summary or protected token. [MED, training
knowledge → speculation on the persistence of that field to the local
rollout].
- Tool I/O: tool calls + tool results are carried inline in the
message array of the rollout. Whether they're ALSO mirrored into a second
envelope (Claude-style) or into the session TOML (cross-file) is [UNKNOWN].

First three measurements once a session file exists:
1. Layout & bytes/turn: list ~/.codex/sessions/, get the true
extensions (.jsonl vs .toml), measure bytes-per-session and
bytes-per-turn; is per-line metadata repeated on every record or hoisted?
2. Duplication census: pick one tool call, grep its tool_use_id (or
a known stdout string) across the file(s) ;  does the payload appear
once, twice in one file (dual-envelope), or **twice across the
session file AND the rollout** (cross-file byte-identical)?
3. Thinking persistence: grep for reasoning / encrypted_content /
summary in assistant records; measure bytes; check whether it persists
after the live turn and whether it's duplicated across files. [LOW/MED
confidence it's even present]

What makes Codex MORE dedupable than Claude Code: **cross-file
byte-identical duplication** (same messages in both the session TOML and
the rollout JSONL) ;  that is clean, byte-identical, zero-loss-removable
weight, very close to our Hermes A2/A3 case. **What makes it LESS
dedupable:** a single monotonic rollout with each message stored once and
metadata hoisted once ;  then there is almost no waste to harvest, and the
"disease" (as measurable by sweap) is nearly absent. The sharpening
insight for the founder: **a store that duplicates across files is MORE
product-friendly than Claude's in-file transformed dual-envelope**,
because cross-file byte-identical weight is provably
zero-loss-recoverable, while transformed envelopes are not. [MED,
training knowledge + derived]

T6 ;  Adjacent vendors (each one paragraph, training knowledge, tagged;
UNKNOWN over invention)

- Gemini CLI (Google) ;  a non-open-source npm agentic CLI in the same
class as Claude Code and Codex. Its local session store path is not
publicly documented [UNKNOWN]; it's project-scoped and likely lives under
a per-user dir (~/.gemini) or an app-data location. Gemini emits long
chain-of-thought "thoughts," so if those are persisted locally they
could become a large recoverable class ;  but local persistence of
reasoning is currently [UNKNOWN]. Worth measuring next: YES (top tier
with Codex), because it's an agentic CLI whose COT is the exact thing our
Herumes-style dupe detector would weigh. [LOW/MED]
- Cursor (Anysphere) ;  an Electron app; on macOS state lives under
~/Library/Application Support/Cursor (SQLite + JSON) for
workspace/composer/chat history, with significant server-side sync. Full
chain-of-thought is unlikely to be durably quiescent locally (streamed,
lightly persisted, server-backed) [MED]. **Worth measuring next:
moderate** (huge session volume, big stores) but lower priority than CLI
tools because the local canonical boundary is blurred by cloud sync. [MED]
- Aider (Paul Gauthier) ;  open-source (MIT) Python assistant; stores
conversation history in SQLite (aider.db / repo-scoped .aider) plus
a .aider.chat.history.md. Being SQLite-based, it is architecturally the
same class as our Hermes store (rows/columns, twin-column risk) ;  and
because it's open source, our weigh/SELECT SUM(LENGTH(col)) method
(R25) transfers directly and is auditable. Whether it persists raw
reasoning effort to that DB is [UNKNOWN]. **Worth measuring next: YES ; 
the single highest-priority target after CC/Codex**, for the
SQLite-parallel and the open-source inspectability. [MED confidence on
specifics, HIGH strategic value]
- OpenAI desktop ChatGPT ;  Electron app; conversations
stored/retrieved largely from the server with a local SQLite/LevelDB
cache under ~/Library/Application Support/OpenAI. Reasoning (COT) is
protected server-side, so it's the least likely to hold durable
quiescent local weight [MED]. Worth measuring next: LOW ;  closed,
server-backed, few analogies to a local agent store that sweap-style
zero-loss removal applies to. [LOW/MED]

Ranking to measure next: 1) Codex (already running on the Mac, T5) ·
2) Aider (SQLite architecture parallel, open source) · 3) Gemini CLI
(agentic CLI, COT-rich) · 4) Cursor · 5) ChatGPT desktop.

T7 ;  Attack our anchor A2 (does the Hermes→Claude parallel survive?)

A2 claims Hermes stores thinking byte-identically twice (9,456 rows,
26 MB), removable with 0 loss (A3). The implied parallel: *"the same
disease ;  recoverable hidden-weight duplication ;  is present in a
different body (Claude's store)."*

**That parallel does NOT survive contact with B2–B5, and here's the
falsifier:**

> FALSIFIED IF: the Hermes→Claude "same disease" parallel dies the
moment a quarantine test on the Claude file loses any byte not
reconstructable from copy 1 + recorded context, OR requires any
recompute/reconcile cost to restore a consumer ;  because Hermes restore
was zero-work byte-copy (A3). If Claude's redundancy is only
palpably-overlapping while every second-envelope byte is unique
structured data (stderr, exit codes, cwd-rewrites not derivable from
context), then Claude does not carry the lapse-class disease; it
carries a faithful dual representation with additive fields, and
removing it is data loss, not dieting.

The even sharper falsifier is structural, and B2 already delivers it:
**Hermes's biggest wasted class (26 MB of duplicated thinking) does not
exist in this Claude file at all** ;  Claude persists no thinking text,
only signatures. So the two stores are not the same body with the same
disease; they are different diseases:

- Hermes A2 = true byte-identical duplication (proven recoverable,
zero-loss) ;  the lapse/waste disease.
- Claude B2–B4 = **withheld thinking + dual-envelope with
transformed/structured second copy** (recoverable only if a lose-nothing
test passes, currently unproven) ;  a different, smaller, riskier
pathology.

Additional A2 self-audit: A2 itself would be falsified if a re-run of the
R25 column audit found the reasoning/reasoning_content columns were
not byte-identical across all 9,456 rows (i.e., the "twice" was a
view artifact rather than a true duplicate). This is the discipline the
founder's own canonical-claim law encodes ("tested" stays in the
sentence; "schema" stays singular) ;  and it is exactly why "AI stores
carry everything twice" is banned copy and the correct product frame is
"the weigh-in detects which pattern YOUR store has." The Claude
weigh-in already demonstrates that: pattern detected = *dual-envelope +
withheld thinking*, not byte-identical redundancy.

Plain-language summary (for a non-technical founder)

We built a tool that finds where an AI assistant's saved memory hides
extra, duplicated weight and that can remove it safely with an undo
button. We proved it works on our own assistant's storage (Hermes), which
kept the same hidden "thinking" notes twice, wasting 26 MB ;  and we
removed 37.57 MB with nothing lost. The open question was whether other
AI tools that save their conversations to disk have the same kind of
hidden weight. You started running two other tools ;  Claude Code and
Codex ;  on one Mac to find out.

What this analysis found for Claude Code: it saves one conversation as a
text log, and inside that log the same tool action and tool result do get
written down in two places. But ;  and this is the key catch ;  the two
copies are never identical. The second copy is a slightly rewritten or
repackaged version of the first, not a byte-for-byte duplicate. That
makes it much less safe to remove than what we did with Hermes. On this
one file, the amount we could plausibly reclaim is only about 5 to 15% of
its size, and even that is an estimate, not a proof ;  we haven't tested
it on a real machine yet. Meanwhile, one big thing we found with Hermes
(the duplicated thinking notes) doesn't exist in Claude Code at all:
Claude doesn't even save its thinking text, only a digital "seal" to
prove the thinking wasn't tampered with.

The honest bottom line: not every AI tool carries the same kind of hidden
weight. Hermes had true copies of the same thing saved twice (we proved
we can remove those with nothing lost). Claude Code has two
different-looking records of the same action ;  which is messier,
riskier, and so far unproven to be safely removable. This is exactly the
"find out which pattern your store has" story our product tells, and it
means we can't claim the same disease everywhere ;  we have to weigh each
store to see what's really inside it. The natural next steps are: once
Codex produces a conversation file, measure it the same way (it might
have a clean, easily-removable duplicate pattern, or almost no waste at
all), and run a small safe test on one Claude file (a copy, with full
undo) to see if its two records are actually removable.



---

## FALSIFIED-IF REGISTER (consolidated)

- Signatures decode to readable chain-of-thought -> thinking IS persisted, reclassify.
- Any wireToolInputs value not derivable from copy 1 + cwd -> input envelope carries
  unique data, not dedupable lose-nothing.
- toolUseResult flattened covers all of tool_result -> recoverable slice grows
  toward the 75K bound (band high rises toward ~300K / ~19%).
- Any consumer (resume/rewind/subagent/export) fails quarantine-then-restore on a
  copy -> the 75-230K band collapses toward 0; Claude pattern is not lapse-class.
- Hermes A2 re-audit finds reasoning columns not byte-identical across all 9,456
  rows -> our own anchor weakens too.

## NEXT (user-gated, nothing before a run exists)

1. Codex CLI: first session lands in ~/.codex/sessions/ [ASSUMPTION] -> run the
   same census (layout, bytes/turn, duplication census, thinking persistence).
2. Optional safe test: copy one Claude .jsonl, quarantine second envelopes,
   exercise resume/rewind, restore. Nothing claimed until that round-trips.
3. Worker ranking of next targets: Codex, Aider (SQLite parallel, open source),
   Gemini CLI, Cursor, ChatGPT desktop.

Worker session: 20261017_203049_a7d6df (hf_dispatch, deepseek, budget 850s,
actual 3m53s). Receipt chain: brief /tmp/claude_store_brief.txt, raw
/tmp/claude_store_raw.txt (38,424 bytes, needle last-line verified).
