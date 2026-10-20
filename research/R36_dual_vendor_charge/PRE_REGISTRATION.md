# R36 hub pre-registration (computed BEFORE reading either worker output)

Date: 2026-10-20. Prices from the two official lists retrieved live today
(see brief for URLs and stamps). Constants: dead tokens = 18,210,064
(= 90.69% exact census on n=37,813 rows); dead M = 18.210064.

## Expected T1 charges ($/1M junk tokens, input minus cache-read)

| model | charge |
|---|---|
| deepseek-flash, off-peak | 0.15 - 0.003 = **$0.147** |
| deepseek-flash, peak | 0.30 - 0.006 = **$0.294** |
| deepseek-v4-pro, off-peak | 0.66 - 0.022 = **$0.638** |
| deepseek-v4-pro, peak | 1.32 - 0.044 = **$1.276** |
| M3.1-Flash | 0.15 - 0.015 = **$0.135** |
| M3 <=512k | 0.30 - 0.06 = **$0.240** |
| M3 >512k | 0.60 - 0.12 = **$0.480** |

## Expected T2 $ per lapse (18.210064 x charge)

| model | $ per lapse |
|---|---|
| deepseek-flash off-peak | 18.210064 x 0.147 = **$2.676879** (~$2.68) |
| deepseek-flash peak | 18.210064 x 0.294 = **$5.353759** (~$5.35) |
| v4-pro off-peak | 18.210064 x 0.638 = **$11.618021** (~$11.62) |
| v4-pro peak | 18.210064 x 1.276 = **$23.236042** (~$23.24) |
| M3.1-Flash | 18.210064 x 0.135 = **$2.458359** (~$2.46) |
| M3 <=512k | 18.210064 x 0.240 = **$4.370415** (~$4.37) |
| M3 >512k | 18.210064 x 0.480 = **$8.740831** (~$8.74) |

## Expected T4 ranking (cheapest first)

M3.1-Flash $2.46 < deepseek-flash off-peak $2.68 < M3<=512k $4.37 <
deepseek-flash peak $5.35 < M3>512k $8.74 < v4-pro off-peak $11.62 <
v4-pro peak $23.24.

Falsification condition (cache-read == input price) holds for NO model on
either list.

Note for context (not seeded into the brief): our own free-lane runs show
0.0% provider-side cache-hit on both vendors' lanes (billed_usage_census,
2026-10-14), so dollar figures are list-price comparison prices for a
PAYING runner, not bills we paid. Frame exactly so in the paper.

## ERRATUM (hub-side, logged 2026-10-20 after the DeepSeek lane returned)

The T2 table above used the WRONG denominator: total store tokens
(18.210064M) instead of the DEAD-WEIGHT subset. The correct dead count,
derived from the anchors and consistent with filed R33's own $8.09 figure
(8.09 / 0.49 = 16.51M): **16,514,707 tokens** (18,210,064 x 0.9069).
The DeepSeek worker derived the dead basis itself, as the brief demanded;
its T2 cells are EXACT. Corrected expected T2 ($ per lapse, dead x charge):

| model | corrected $ per lapse |
|---|---|
| M3.1-Flash | 16.514707 x 0.135 = **$2.2295** (~$2.23) |
| deepseek-flash off-peak | 16.514707 x 0.147 = **$2.4277** (~$2.43) |
| M3 <=512k | 16.514707 x 0.240 = **$3.9635** (~$3.96) |
| deepseek-flash peak | 16.514707 x 0.294 = **$4.8553** (~$4.86) |
| M3 >512k | 16.514707 x 0.480 = **$7.9271** (~$7.93) |
| v4-pro off-peak | 16.514707 x 0.638 = **$10.5364** (~$10.54) |
| v4-pro peak | 16.514707 x 1.276 = **$21.0728** (~$21.07) |

T1 charges and the T4 ranking order are unchanged. Original T2 table kept
above unedited, per the no-silent-edit law.
