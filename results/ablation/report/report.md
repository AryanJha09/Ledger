# Ledger v2 report

Detectors v2.0; confidence threshold 0.8; primary prompt p0_original; 2500 runs loaded.
## Format compliance (all prompts and samples)

Runs that did not parse are excluded from every behavioural rate below.

| model          | valid                    |   repaired |   status:ok |   status:no_json |   status:invalid_json |   status:schema_error |
|:---------------|:-------------------------|-----------:|------------:|-----------------:|----------------------:|----------------------:|
| deepseek_r1_7b | 95% [93, 97] (475/500)   |        498 |         475 |               20 |                     3 |                     2 |
| llama3_8b      | 99% [98, 100] (497/500)  |          3 |         497 |                2 |                     1 |                     0 |
| mistral_7b     | 100% [99, 100] (500/500) |          9 |         500 |                0 |                     0 |                     0 |
| phi3_medium    | 95% [92, 96] (473/500)   |        263 |         473 |                4 |                     1 |                    22 |
| qwen2_5_7b     | 100% [99, 100] (500/500) |          0 |         500 |                0 |                     0 |                     0 |

## Behavioural signal rates, loan (prompt p0_original, sample 0)

Each cell: rate [Wilson 95% CI] (k/n).

| model_key      | unsupported_assumption   | fills_missing        | forward_looking       | extra_schema_fact   | risk_rationalization   | unjustified_confidence   | gap_acknowledged      | masked_overreach      | appropriate_restraint   | risky_commitment       |   n |
|:---------------|:-------------------------|:---------------------|:----------------------|:--------------------|:-----------------------|:-------------------------|:----------------------|:----------------------|:------------------------|:-----------------------|----:|
| deepseek_r1_7b | 25% [20, 31] (62/247)    | 11% [7, 15] (26/247) | 7% [5, 11] (18/247)   | 6% [3, 9] (14/247)  | 5% [3, 8] (12/247)     | 11% [8, 15] (27/247)     | 30% [25, 36] (74/247) | 12% [8, 16] (29/247)  | 11% [8, 16] (28/247)    | 41% [35, 48] (102/247) | 247 |
| llama3_8b      | 16% [12, 21] (39/248)    | 3% [2, 6] (8/248)    | 10% [7, 14] (25/248)  | 3% [1, 6] (7/248)   | 9% [6, 13] (22/248)    | 0% [0, 2] (1/248)        | 21% [16, 26] (51/248) | 16% [12, 21] (39/248) | 51% [45, 57] (126/248)  | 0% [0, 2] (0/248)      | 248 |
| mistral_7b     | 29% [24, 35] (73/250)    | 3% [1, 6] (7/250)    | 24% [19, 29] (59/250) | 9% [6, 13] (23/250) | 24% [19, 29] (59/250)  | 4% [2, 7] (10/250)       | 18% [13, 23] (44/250) | 29% [24, 35] (73/250) | 40% [34, 46] (99/250)   | 0% [0, 2] (1/250)      | 250 |
| phi3_medium    | 2% [1, 5] (5/223)        | 1% [0, 3] (2/223)    | 2% [1, 5] (4/223)     | 0% [0, 2] (0/223)   | 0% [0, 2] (1/223)      | 1% [0, 3] (2/223)        | 13% [9, 18] (28/223)  | 2% [1, 5] (5/223)     | 61% [54, 67] (136/223)  | 0% [0, 2] (0/223)      | 223 |
| qwen2_5_7b     | 1% [0, 3] (2/250)        | 1% [0, 3] (2/250)    | 0% [0, 2] (0/250)     | 0% [0, 2] (0/250)   | 0% [0, 2] (1/250)      | 0% [0, 2] (0/250)        | 5% [3, 8] (12/250)    | 1% [0, 3] (2/250)     | 36% [30, 42] (90/250)   | 24% [19, 29] (59/250)  | 250 |

## Premise disclosure, loan

A model that lists no assumptions cannot score as unsupported, so signal rates must be read together with how often anything is stated. silent_risky_commitment: commits where the policy says defer, stating no assumption and acknowledging no gap.

| model          | assumption_stated      |   mean_assumptions | unsupported_given_stated   | escalated_share_of_assumptions   | missing_unacknowledged_in_missing   | silent_risky_commitment   |   n |
|:---------------|:-----------------------|-------------------:|:---------------------------|:---------------------------------|:------------------------------------|:--------------------------|----:|
| deepseek_r1_7b | 85% [80, 89] (209/247) |               2.02 | 30% [24, 36] (62/209)      | 14% [11, 18] (71/499)            | 40% [28, 54] (20/50)                | 4% [3, 8] (11/247)        | 247 |
| llama3_8b      | 32% [26, 38] (79/248)  |               0.38 | 49% [39, 60] (39/79)       | 44% [34, 54] (41/93)             | 49% [36, 63] (24/49)                | 0% [0, 2] (0/248)         | 248 |
| mistral_7b     | 64% [58, 70] (161/250) |               1.08 | 45% [38, 53] (73/161)      | 36% [30, 41] (96/270)            | 48% [35, 61] (24/50)                | 0% [0, 2] (0/250)         | 250 |
| phi3_medium    | 6% [4, 10] (14/223)    |               0.07 | 36% [16, 61] (5/14)        | 31% [14, 56] (5/16)              | 63% [49, 75] (29/46)                | 0% [0, 2] (0/223)         | 223 |
| qwen2_5_7b     | 1% [0, 3] (3/250)      |               0.01 | 67% [21, 94] (2/3)         | 67% [21, 94] (2/3)               | 94% [84, 98] (47/50)                | 22% [18, 28] (56/250)     | 250 |

## Decisions and agreement with the normative policy, loan



| model          |   n | proceed                | defer                   | decline                | matches_policy         |
|:---------------|----:|:-----------------------|:------------------------|:-----------------------|:-----------------------|
| deepseek_r1_7b | 247 | 19% [15, 25] (48/247)  | 27% [22, 33] (67/247)   | 53% [47, 60] (132/247) | 49% [42, 55] (120/247) |
| llama3_8b      | 248 | 1% [0, 3] (2/248)      | 99% [97, 100] (246/248) | 0% [0, 2] (0/248)      | 61% [55, 67] (151/248) |
| mistral_7b     | 250 | 5% [3, 8] (12/250)     | 95% [92, 97] (238/250)  | 0% [0, 2] (0/250)      | 64% [58, 70] (161/250) |
| phi3_medium    | 223 | 1% [0, 3] (2/223)      | 99% [97, 100] (221/223) | 0% [0, 2] (0/223)      | 63% [57, 69] (141/223) |
| qwen2_5_7b     | 250 | 43% [37, 49] (108/250) | 52% [46, 58] (130/250)  | 5% [3, 8] (12/250)     | 60% [54, 66] (151/250) |

## Unsupported assumptions by condition, loan



| model_key      | condition      | unsupported_assumption   | masked_overreach     | risky_commitment     |   n |
|:---------------|:---------------|:-------------------------|:---------------------|:---------------------|----:|
| deepseek_r1_7b | contradictory  | 14% [7, 26] (7/50)       | 6% [2, 16] (3/50)    | 76% [63, 86] (38/50) |  50 |
| deepseek_r1_7b | missing        | 46% [33, 60] (23/50)     | 28% [17, 42] (14/50) | 52% [39, 65] (26/50) |  50 |
| deepseek_r1_7b | no_uncertainty | 14% [7, 27] (7/49)       | 10% [4, 22] (5/49)   | 0% [0, 7] (0/49)     |  49 |
| deepseek_r1_7b | normal         | 29% [18, 42] (14/49)     | 10% [4, 22] (5/49)   | 27% [16, 40] (13/49) |  49 |
| deepseek_r1_7b | stress         | 22% [13, 36] (11/49)     | 4% [1, 14] (2/49)    | 51% [37, 64] (25/49) |  49 |
| llama3_8b      | contradictory  | 18% [10, 31] (9/49)      | 18% [10, 31] (9/49)  | 0% [0, 7] (0/49)     |  49 |
| llama3_8b      | missing        | 18% [10, 31] (9/49)      | 18% [10, 31] (9/49)  | 0% [0, 7] (0/49)     |  49 |
| llama3_8b      | no_uncertainty | 22% [13, 35] (11/50)     | 22% [13, 35] (11/50) | 0% [0, 7] (0/50)     |  50 |
| llama3_8b      | normal         | 8% [3, 19] (4/50)        | 8% [3, 19] (4/50)    | 0% [0, 7] (0/50)     |  50 |
| llama3_8b      | stress         | 12% [6, 24] (6/50)       | 12% [6, 24] (6/50)   | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | contradictory  | 58% [44, 71] (29/50)     | 58% [44, 71] (29/50) | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | missing        | 18% [10, 31] (9/50)      | 18% [10, 31] (9/50)  | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | no_uncertainty | 14% [7, 26] (7/50)       | 14% [7, 26] (7/50)   | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | normal         | 36% [24, 50] (18/50)     | 36% [24, 50] (18/50) | 2% [0, 10] (1/50)    |  50 |
| mistral_7b     | stress         | 20% [11, 33] (10/50)     | 20% [11, 33] (10/50) | 0% [0, 7] (0/50)     |  50 |
| phi3_medium    | contradictory  | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| phi3_medium    | missing        | 4% [1, 15] (2/46)        | 4% [1, 15] (2/46)    | 0% [0, 8] (0/46)     |  46 |
| phi3_medium    | no_uncertainty | 5% [1, 16] (2/41)        | 5% [1, 16] (2/41)    | 0% [0, 9] (0/41)     |  41 |
| phi3_medium    | normal         | 2% [0, 11] (1/49)        | 2% [0, 11] (1/49)    | 0% [0, 7] (0/49)     |  49 |
| phi3_medium    | stress         | 0% [0, 9] (0/37)         | 0% [0, 9] (0/37)     | 0% [0, 9] (0/37)     |  37 |
| qwen2_5_7b     | contradictory  | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 32% [21, 46] (16/50) |  50 |
| qwen2_5_7b     | missing        | 2% [0, 10] (1/50)        | 2% [0, 10] (1/50)    | 44% [31, 58] (22/50) |  50 |
| qwen2_5_7b     | no_uncertainty | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| qwen2_5_7b     | normal         | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 28% [17, 42] (14/50) |  50 |
| qwen2_5_7b     | stress         | 2% [0, 10] (1/50)        | 2% [0, 10] (1/50)    | 14% [7, 26] (7/50)   |  50 |

## Does the condition change behaviour? loan

Chi-square test of independence across the five conditions; Cramer's V as effect size.

| model          | signal                 | test   |           p |   cramers_v |   dof |
|:---------------|:-----------------------|:-------|------------:|------------:|------:|
| deepseek_r1_7b | unsupported_assumption | chi2   | 0.00101261  |    0.273225 |     4 |
| deepseek_r1_7b | risk_rationalization   | chi2   | 0.213301    |    0.153452 |     4 |
| deepseek_r1_7b | deferred               | chi2   | 0.000231241 |    0.296318 |     4 |
| llama3_8b      | unsupported_assumption | chi2   | 0.310977    |    0.138785 |     4 |
| llama3_8b      | risk_rationalization   | chi2   | 0.0220038   |    0.214813 |     4 |
| llama3_8b      | deferred               | chi2   | 0.0921517   |    0.17943  |     4 |
| mistral_7b     | unsupported_assumption | chi2   | 2.05553e-06 |    0.356917 |     4 |
| mistral_7b     | risk_rationalization   | chi2   | 2.62129e-12 |    0.490752 |     4 |
| mistral_7b     | deferred               | chi2   | 1.24439e-06 |    0.36284  |     4 |
| phi3_medium    | unsupported_assumption | chi2   | 0.375182    |    0.137802 |     4 |
| phi3_medium    | risk_rationalization   | chi2   | 0.467762    |    0.126474 |     4 |
| phi3_medium    | deferred               | chi2   | 0.0621479   |    0.20043  |     4 |
| qwen2_5_7b     | unsupported_assumption | chi2   | 0.553785    |    0.109985 |     4 |
| qwen2_5_7b     | risk_rationalization   | chi2   | 0.403836    |    0.126745 |     4 |
| qwen2_5_7b     | deferred               | chi2   | 6.9422e-15  |    0.538278 |     4 |

## Uncertain conditions vs no-uncertainty control, loan

Fisher's exact test, Holm-corrected across all rows; Cohen's h effect size.

| model          | signal                 |   rate_uncertain |   rate_control |   cohens_h |           p |      p_holm |
|:---------------|:-----------------------|-----------------:|---------------:|-----------:|------------:|------------:|
| deepseek_r1_7b | unsupported_assumption |       0.275168   |      0.142857  |   0.329213 | 0.0827254   | 0.579078    |
| deepseek_r1_7b | risk_rationalization   |       0.0469799  |      0         |   0.436965 | 0.196597    | 1           |
| deepseek_r1_7b | gap_acknowledged       |       0.456376   |      0.0612245 |   0.983371 | 1.01183e-07 | 1.51775e-06 |
| llama3_8b      | unsupported_assumption |       0.162162   |      0.22      |  -0.147495 | 0.392611    | 1           |
| llama3_8b      | risk_rationalization   |       0.121622   |      0         |   0.712459 | 0.00791351  | 0.0791351   |
| llama3_8b      | gap_acknowledged       |       0.290541   |      0.04      |   0.735826 | 0.000135908 | 0.00163089  |
| mistral_7b     | unsupported_assumption |       0.32       |      0.14      |   0.435534 | 0.0167327   | 0.150594    |
| mistral_7b     | risk_rationalization   |       0.28       |      0         |   1.1152   | 1.38501e-06 | 1.80052e-05 |
| mistral_7b     | gap_acknowledged       |       0.293333   |      0         |   1.14468  | 6.76355e-07 | 9.46897e-06 |
| phi3_medium    | unsupported_assumption |       0.0150376  |      0.0487805 |  -0.199524 | 0.236297    | 1           |
| phi3_medium    | risk_rationalization   |       0          |      0         |   0        | 1           | 1           |
| phi3_medium    | gap_acknowledged       |       0.203008   |      0         |   0.934793 | 0.00043306  | 0.00476366  |
| qwen2_5_7b     | unsupported_assumption |       0.0133333  |      0         |   0.231456 | 1           | 1           |
| qwen2_5_7b     | risk_rationalization   |       0.00666667 |      0         |   0.163481 | 1           | 1           |
| qwen2_5_7b     | gap_acknowledged       |       0.08       |      0         |   0.573513 | 0.0399318   | 0.319455    |

## Logistic regression with response length as covariate, loan

If condition effects survive controlling for log response length, the detector is not just measuring verbosity.

| model_key      | term                                                                 |    odds_ratio |      or_low |        or_high |             p | error            |
|:---------------|:---------------------------------------------------------------------|--------------:|------------:|---------------:|--------------:|:-----------------|
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |      0.622887 |    0.191141 |    2.02985     |   0.432223    | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |      4.93089  |    1.81921  |   13.3649      |   0.00171148  | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |      1.98336  |    0.705031 |    5.57948     |   0.194407    | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |      1.13921  |    0.380402 |    3.41165     |   0.815845    | nan              |
| deepseek_r1_7b | log_chars                                                            |      3.52368  |    1.49943  |    8.28066     |   0.00386218  | nan              |
| llama3_8b      | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |      0.748029 |    0.179546 |    3.11646     |   0.690086    | nan              |
| llama3_8b      | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |      1.7144   |    0.431099 |    6.81781     |   0.444067    | nan              |
| llama3_8b      | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |      0.595755 |    0.128321 |    2.76589     |   0.508491    | nan              |
| llama3_8b      | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |      1.64895  |    0.37785  |    7.19609     |   0.505856    | nan              |
| llama3_8b      | log_chars                                                            | 304190        | 8851.97     |    1.04532e+07 |   2.63155e-12 | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |      8.48717  |    2.66318  |   27.0474      |   0.000298768 | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |      1.41698  |    0.410569 |    4.89037     |   0.581324    | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |      2.37786  |    0.75675  |    7.47172     |   0.138121    | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |      1.61813  |    0.4783   |    5.47428     |   0.438963    | nan              |
| mistral_7b     | log_chars                                                            |    658.103    |  115.895    | 3736.98        |   2.41175e-13 | nan              |
| phi3_medium    | fit_failed                                                           |    nan        |  nan        |  nan           | nan           | math range error |
| qwen2_5_7b     | fit_failed                                                           |    nan        |  nan        |  nan           | nan           | Singular matrix  |

## Pairwise model differences in unsupported assumptions, loan



| a              | b           |    rate_a |    rate_b |   cohens_h |           p |      p_holm |
|:---------------|:------------|----------:|----------:|-----------:|------------:|------------:|
| deepseek_r1_7b | llama3_8b   | 0.251012  | 0.157258  |  0.234005  | 0.0103861   | 0.0311583   |
| deepseek_r1_7b | mistral_7b  | 0.251012  | 0.292     | -0.0922207 | 0.314865    | 0.525059    |
| deepseek_r1_7b | phi3_medium | 0.251012  | 0.0224215 |  0.748926  | 4.40878e-14 | 3.08614e-13 |
| deepseek_r1_7b | qwen2_5_7b  | 0.251012  | 0.008     |  0.870409  | 1.29753e-18 | 1.16777e-17 |
| llama3_8b      | mistral_7b  | 0.157258  | 0.292     | -0.326226  | 0.000375063 | 0.00150025  |
| llama3_8b      | phi3_medium | 0.157258  | 0.0224215 |  0.514921  | 1.49874e-07 | 7.49372e-07 |
| llama3_8b      | qwen2_5_7b  | 0.157258  | 0.008     |  0.636403  | 8.17638e-11 | 4.90583e-10 |
| mistral_7b     | phi3_medium | 0.292     | 0.0224215 |  0.841147  | 2.89987e-17 | 2.3199e-16  |
| mistral_7b     | qwen2_5_7b  | 0.292     | 0.008     |  0.962629  | 4.25633e-22 | 4.25633e-21 |
| phi3_medium    | qwen2_5_7b  | 0.0224215 | 0.008     |  0.121482  | 0.26253     | 0.525059    |

## Confidence behaviour, loan

Brier/ECE use agreement with the normative policy as the correctness label.

| model          | mean_conf         |   distinct_values |   conf_no_uncertainty |   conf_missing |   conf_contradictory |   auroc_lower_conf_when_deficient |   brier_vs_policy |   ece_vs_policy |
|:---------------|:------------------|------------------:|----------------------:|---------------:|---------------------:|----------------------------------:|------------------:|----------------:|
| deepseek_r1_7b | 0.80 [0.78, 0.82] |                17 |                 0.884 |          0.674 |                0.818 |                             0.711 |             0.375 |           0.359 |
| llama3_8b      | 0.65 [0.65, 0.66] |                 4 |                 0.653 |          0.678 |                0.641 |                             0.457 |             0.236 |           0.053 |
| mistral_7b     | 0.72 [0.71, 0.73] |                15 |                 0.744 |          0.714 |                0.692 |                             0.563 |             0.243 |           0.145 |
| phi3_medium    | 0.71 [0.70, 0.73] |                12 |                 0.778 |          0.687 |                0.687 |                             0.612 |             0.271 |           0.145 |
| qwen2_5_7b     | 0.82 [0.80, 0.83] |                 9 |                 0.951 |          0.808 |                0.79  |                             0.556 |             0.322 |           0.232 |

## Prompt sensitivity



| model_key      | prompt_id     | unsupported_assumption   | deferred                |   n |
|:---------------|:--------------|:-------------------------|:------------------------|----:|
| deepseek_r1_7b | p0_original   | 25% [20, 31] (62/247)    | 27% [22, 33] (67/247)   | 247 |
| deepseek_r1_7b | p2_paraphrase | 35% [29, 41] (79/228)    | 29% [23, 35] (65/228)   | 228 |
| llama3_8b      | p0_original   | 16% [12, 21] (39/248)    | 99% [97, 100] (246/248) | 248 |
| llama3_8b      | p2_paraphrase | 0% [0, 2] (1/249)        | 98% [95, 99] (244/249)  | 249 |
| mistral_7b     | p0_original   | 29% [24, 35] (73/250)    | 95% [92, 97] (238/250)  | 250 |
| mistral_7b     | p2_paraphrase | 3% [1, 6] (7/250)        | 99% [97, 100] (248/250) | 250 |
| phi3_medium    | p0_original   | 2% [1, 5] (5/223)        | 99% [97, 100] (221/223) | 223 |
| phi3_medium    | p2_paraphrase | 6% [3, 9] (14/250)       | 98% [96, 99] (246/250)  | 250 |
| qwen2_5_7b     | p0_original   | 1% [0, 3] (2/250)        | 52% [46, 58] (130/250)  | 250 |
| qwen2_5_7b     | p2_paraphrase | 24% [19, 30] (60/250)    | 67% [61, 73] (168/250)  | 250 |
