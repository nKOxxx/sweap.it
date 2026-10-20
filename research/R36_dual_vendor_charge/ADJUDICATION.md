# R36 adjudication - dual-lane carrying charge (2026-10-20)

## Lanes

| lane | model | session | duration | verdict |
|---|---|---|---|---|
| 1 | deepseek-ai/DeepSeek-V4-Flash-0731 | 20261020_150800_91dbe4 | 6m23s | needle OK |
| 2 | Qwen/Qwen3.8-27B | 20261020_152418_76aed2 | 3m05s | needle OK |

Note: lane 2 was dispatched as MiniMax per the original burn plan; the
HyperFusion key allow-list no longer includes any MiniMax model (verified
via GET /v1/models on both keys, 2026-10-20; failed attempt session
20261020_151558_700ea1, HTTP 401 key_model_access_denied). Qwen3.8-27B ran
the identical frozen brief as the second independent derivation. Labeled
honestly everywhere.

## Pre-registration (hub, written before lane 1 returned)

PRE_REGISTRATION.md in this directory. Its first T2 table used the wrong
denominator (total store 18.21M instead of dead-weight subset); erratum
appended there per the no-silent-edit law; corrected expectations used for
adjudication below. Dead-weight = 18,210,064 x 0.9069 = 16,514,707 tokens;
cross-check: filed R33's own $8.09 = 16.51M x $0.49 confirms the basis.

## Cell-by-cell result

T1 charges ($/1M junk tokens) - 7/7 EXACT convergence (3 sources):

| model/tier | lane 1 | lane 2 | hub |
|---|---|---|---|
| deepseek-flash off-peak | 0.147 | 0.147 | 0.147 |
| deepseek-flash peak | 0.294 | 0.294 | 0.294 |
| deepseek-v4-pro off-peak | 0.638 | 0.638 | 0.638 |
| deepseek-v4-pro peak | 1.276 | 1.276 | 1.276 |
| MiniMax M3.1-Flash | 0.135 | 0.135 | 0.135 |
| MiniMax M3 <=512k | 0.24 | 0.240 | 0.240 |
| MiniMax M3 >512k | 0.48 | 0.480 | 0.480 |

T2 $ per lapse - 7/7 convergence at the cent; differences are display
rounding only (lane 1: 2 decimals, lane 2: 3 decimals, hub: 4):

| model/tier | lane 1 | lane 2 | hub corrected |
|---|---|---|---|
| MiniMax M3.1-Flash | 2.23 | 2.229 | 2.2295 |
| deepseek-flash off-peak | 2.43 | 2.428 | 2.4277 |
| MiniMax M3 <=512k | 3.96 | 3.964 | 3.9635 |
| deepseek-flash peak | 4.86 | 4.855 | 4.8553 |
| MiniMax M3 >512k | 7.93 | 7.927 | 7.9271 |
| deepseek-v4-pro off-peak | 10.54 | 10.536 | 10.5364 |
| deepseek-v4-pro peak | 21.07 | 21.073 | 21.0728 |

T4 ranking: identical order in both lanes and hub. Falsification condition
(cached price == full input price): holds for NO model on either list,
stated independently by both lanes.

## Adjudication findings

1. Lane 2 (Qwen) caveat-sentence error, numbers unaffected: it priced the
   store in MiniMax's <=512k tier (correct choice) but justified it with
   "16.51M < 512k", which is false. Correct reason: a lapse re-read
   happens across many API calls, each bounded by the model's context
   window, so each call bills at <=512k rates; the >512k row applies only
   if a single request carried that much input, which no current request
   does. Paper uses the <=512k tier as operative; >512k shown as
   [HYPOTHETICAL], which lane 2 itself flagged.
2. Lane 1 (DeepSeek) made no tier adjudication (listed both tiers); no
   error, but lane 2's flag was the sharper read.
3. Lane 2 additionally derived a rounding band on the dead-weight count
   (90.69% at 2dp -> D +/- 911 tokens = 0.011%): noted, does not move any
   cent.
4. Both lanes independently stated the MiniMax-window assumption (no
   peak/off-peak split on list M). Consistent.

## Verdict

STUDY CONVERGED. All 14 numeric cells double-derived by independent blind
lanes and hub-recounted. Admitted in full for the paper's Table 3, with
finding 1's tier note attached. No averaging was performed (none needed;
no cell diverged).

## Data-source note (for the paper's methods section)

The MiniMax rows' authority is the OFFICIAL PRICE LIST
(platform.minimax.io/docs/pricing/overview, retrieved 2026-10-20, current
displayed prices, struck-through list ignored), not a MiniMax worker lane.
Worker lanes exist to verify the DERIVATION ARITHMETIC blind; vendor data
comes from vendor-published prices with a retrieval stamp. A MiniMax worker
lane is therefore unnecessary for these figures and its absence does not
weaken them. Same principle for every vendor column in Table 3.
