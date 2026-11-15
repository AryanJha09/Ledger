# Ledger v2 report

Detectors v2.0; confidence threshold 0.8; primary prompt p1_autonomous; 5250 runs loaded.
## Format compliance (all prompts and samples)

Runs that did not parse are excluded from every behavioural rate below.

| model          | valid                       |   repaired |   status:ok |   status:no_json |   status:invalid_json |   status:empty |   status:schema_error |
|:---------------|:----------------------------|-----------:|------------:|-----------------:|----------------------:|---------------:|----------------------:|
| deepseek_r1_7b | 95% [93, 96] (996/1050)     |        945 |         996 |               48 |                     4 |              2 |                     0 |
| llama3_8b      | 100% [99, 100] (1049/1050)  |          1 |        1049 |                1 |                     0 |              0 |                     0 |
| mistral_7b     | 99% [99, 100] (1042/1050)   |          8 |        1042 |                7 |                     1 |              0 |                     0 |
| phi3_medium    | 100% [99, 100] (1048/1050)  |        724 |        1048 |                0 |                     1 |              0 |                     1 |
| qwen2_5_7b     | 100% [100, 100] (1050/1050) |          0 |        1050 |                0 |                     0 |              0 |                     0 |

## Behavioural signal rates, hiring (prompt p1_autonomous, sample 0)

Each cell: rate [Wilson 95% CI] (k/n).

| model_key      | unsupported_assumption   | fills_missing        | forward_looking       | extra_schema_fact     | risk_rationalization   | unjustified_confidence   | gap_acknowledged      | masked_overreach      | appropriate_restraint   | risky_commitment      |   n |
|:---------------|:-------------------------|:---------------------|:----------------------|:----------------------|:-----------------------|:-------------------------|:----------------------|:----------------------|:------------------------|:----------------------|----:|
| deepseek_r1_7b | 9% [5, 15] (13/144)      | 5% [2, 10] (7/144)   | 0% [0, 3] (0/144)     | 5% [2, 10] (7/144)    | 2% [1, 6] (3/144)      | 6% [3, 11] (8/144)       | 44% [36, 52] (63/144) | 1% [0, 4] (1/144)     | 14% [9, 20] (20/144)    | 50% [42, 58] (72/144) | 144 |
| llama3_8b      | 7% [4, 12] (10/149)      | 4% [2, 9] (6/149)    | 3% [1, 7] (4/149)     | 0% [0, 3] (0/149)     | 5% [3, 10] (8/149)     | 1% [0, 4] (1/149)        | 48% [40, 56] (72/149) | 7% [4, 12] (10/149)   | 54% [46, 62] (81/149)   | 7% [4, 12] (10/149)   | 149 |
| mistral_7b     | 60% [52, 68] (89/148)    | 14% [9, 20] (20/148) | 36% [29, 44] (54/148) | 26% [20, 34] (39/148) | 47% [39, 55] (70/148)  | 9% [5, 14] (13/148)      | 21% [15, 28] (31/148) | 59% [51, 66] (87/148) | 25% [19, 33] (37/148)   | 1% [0, 4] (1/148)     | 148 |
| phi3_medium    | 1% [0, 4] (1/150)        | 1% [0, 4] (1/150)    | 0% [0, 2] (0/150)     | 0% [0, 2] (0/150)     | 1% [0, 4] (1/150)      | 0% [0, 2] (0/150)        | 34% [27, 42] (51/150) | 1% [0, 4] (1/150)     | 64% [56, 71] (96/150)   | 1% [0, 4] (1/150)     | 150 |
| qwen2_5_7b     | 1% [0, 5] (2/150)        | 1% [0, 4] (1/150)    | 1% [0, 4] (1/150)     | 0% [0, 2] (0/150)     | 0% [0, 2] (0/150)      | 1% [0, 5] (2/150)        | 31% [24, 38] (46/150) | 0% [0, 2] (0/150)     | 54% [46, 62] (81/150)   | 11% [7, 17] (17/150)  | 150 |

## Premise disclosure, hiring

A model that lists no assumptions cannot score as unsupported, so signal rates must be read together with how often anything is stated. silent_risky_commitment: commits where the policy says defer, stating no assumption and acknowledging no gap.

| model          | assumption_stated      |   mean_assumptions | unsupported_given_stated   | escalated_share_of_assumptions   | missing_unacknowledged_in_missing   | silent_risky_commitment   |   n |
|:---------------|:-----------------------|-------------------:|:---------------------------|:---------------------------------|:------------------------------------|:--------------------------|----:|
| deepseek_r1_7b | 24% [17, 31] (34/144)  |               0.39 | 38% [24, 55] (13/34)       | 32% [21, 45] (18/56)             | 14% [5, 31] (4/29)                  | 16% [11, 23] (23/144)     | 144 |
| llama3_8b      | 13% [9, 20] (20/149)   |               0.14 | 50% [30, 70] (10/20)       | 48% [28, 68] (10/21)             | 23% [12, 41] (7/30)                 | 2% [1, 6] (3/149)         | 149 |
| mistral_7b     | 97% [92, 99] (143/148) |               1.41 | 62% [54, 70] (89/143)      | 50% [44, 57] (105/208)           | 50% [33, 67] (15/30)                | 0% [0, 3] (0/148)         | 148 |
| phi3_medium    | 3% [1, 7] (4/150)      |               0.03 | 25% [5, 70] (1/4)          | 25% [5, 70] (1/4)                | 33% [19, 51] (10/30)                | 1% [0, 4] (1/150)         | 150 |
| qwen2_5_7b     | 3% [1, 8] (5/150)      |               0.05 | 40% [12, 77] (2/5)         | 25% [7, 59] (2/8)                | 40% [25, 58] (12/30)                | 6% [3, 11] (9/150)        | 150 |

## Decisions and agreement with the normative policy, hiring



| model          |   n | proceed               | defer                   | decline               | matches_policy         |
|:---------------|----:|:----------------------|:------------------------|:----------------------|:-----------------------|
| deepseek_r1_7b | 144 | 48% [40, 56] (69/144) | 18% [13, 25] (26/144)   | 34% [27, 42] (49/144) | 44% [37, 53] (64/144)  |
| llama3_8b      | 149 | 26% [19, 33] (38/149) | 74% [67, 81] (111/149)  | 0% [0, 3] (0/149)     | 77% [70, 83] (115/149) |
| mistral_7b     | 148 | 1% [0, 5] (2/148)     | 99% [95, 100] (146/148) | 0% [0, 3] (0/148)     | 66% [58, 73] (98/148)  |
| phi3_medium    | 150 | 20% [14, 27] (30/150) | 80% [73, 86] (120/150)  | 0% [0, 2] (0/150)     | 83% [77, 88] (125/150) |
| qwen2_5_7b     | 150 | 28% [21, 36] (42/150) | 64% [56, 71] (96/150)   | 8% [5, 13] (12/150)   | 77% [69, 83] (115/150) |

## Unsupported assumptions by condition, hiring



| model_key      | condition      | unsupported_assumption   | masked_overreach     | risky_commitment     |   n |
|:---------------|:---------------|:-------------------------|:---------------------|:---------------------|----:|
| deepseek_r1_7b | contradictory  | 14% [6, 31] (4/28)       | 4% [1, 18] (1/28)    | 96% [82, 99] (27/28) |  28 |
| deepseek_r1_7b | missing        | 21% [10, 38] (6/29)      | 0% [0, 12] (0/29)    | 69% [51, 83] (20/29) |  29 |
| deepseek_r1_7b | no_uncertainty | 7% [2, 21] (2/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| deepseek_r1_7b | normal         | 0% [0, 12] (0/29)        | 0% [0, 12] (0/29)    | 34% [20, 53] (10/29) |  29 |
| deepseek_r1_7b | stress         | 4% [1, 18] (1/28)        | 0% [0, 12] (0/28)    | 54% [36, 70] (15/28) |  28 |
| llama3_8b      | contradictory  | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| llama3_8b      | missing        | 13% [5, 30] (4/30)       | 13% [5, 30] (4/30)   | 17% [7, 34] (5/30)   |  30 |
| llama3_8b      | no_uncertainty | 7% [2, 22] (2/29)        | 7% [2, 22] (2/29)    | 0% [0, 12] (0/29)    |  29 |
| llama3_8b      | normal         | 3% [1, 17] (1/30)        | 3% [1, 17] (1/30)    | 17% [7, 34] (5/30)   |  30 |
| llama3_8b      | stress         | 10% [3, 26] (3/30)       | 10% [3, 26] (3/30)   | 0% [0, 11] (0/30)    |  30 |
| mistral_7b     | contradictory  | 57% [39, 73] (17/30)     | 53% [36, 70] (16/30) | 3% [1, 17] (1/30)    |  30 |
| mistral_7b     | missing        | 63% [46, 78] (19/30)     | 63% [46, 78] (19/30) | 0% [0, 11] (0/30)    |  30 |
| mistral_7b     | no_uncertainty | 46% [30, 64] (13/28)     | 43% [27, 61] (12/28) | 0% [0, 12] (0/28)    |  28 |
| mistral_7b     | normal         | 57% [39, 73] (17/30)     | 57% [39, 73] (17/30) | 0% [0, 11] (0/30)    |  30 |
| mistral_7b     | stress         | 77% [59, 88] (23/30)     | 77% [59, 88] (23/30) | 0% [0, 11] (0/30)    |  30 |
| phi3_medium    | contradictory  | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| phi3_medium    | missing        | 3% [1, 17] (1/30)        | 3% [1, 17] (1/30)    | 0% [0, 11] (0/30)    |  30 |
| phi3_medium    | no_uncertainty | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| phi3_medium    | normal         | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 3% [1, 17] (1/30)    |  30 |
| phi3_medium    | stress         | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| qwen2_5_7b     | contradictory  | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| qwen2_5_7b     | missing        | 3% [1, 17] (1/30)        | 0% [0, 11] (0/30)    | 37% [22, 54] (11/30) |  30 |
| qwen2_5_7b     | no_uncertainty | 3% [1, 17] (1/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| qwen2_5_7b     | normal         | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 17% [7, 34] (5/30)   |  30 |
| qwen2_5_7b     | stress         | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 3% [1, 17] (1/30)    |  30 |

## Does the condition change behaviour? hiring

Chi-square test of independence across the five conditions; Cramer's V as effect size.

| model          | signal                 | test   |             p |   cramers_v |   dof |
|:---------------|:-----------------------|:-------|--------------:|------------:|------:|
| deepseek_r1_7b | unsupported_assumption | chi2   |   0.0431873   |    0.261424 |     4 |
| deepseek_r1_7b | risk_rationalization   | chi2   |   0.0128774   |    0.296894 |     4 |
| deepseek_r1_7b | deferred               | chi2   |   0.000659699 |    0.366919 |     4 |
| llama3_8b      | unsupported_assumption | chi2   |   0.255457    |    0.189063 |     4 |
| llama3_8b      | risk_rationalization   | chi2   |   0.0718083   |    0.240296 |     4 |
| llama3_8b      | deferred               | chi2   |   1.78615e-17 |    0.753807 |     4 |
| mistral_7b     | unsupported_assumption | chi2   |   0.195929    |    0.202074 |     4 |
| mistral_7b     | risk_rationalization   | chi2   |   2.03617e-07 |    0.498251 |     4 |
| mistral_7b     | deferred               | chi2   |   0.532699    |    0.145939 |     4 |
| phi3_medium    | unsupported_assumption | chi2   |   0.402385    |    0.163846 |     4 |
| phi3_medium    | risk_rationalization   | chi2   |   0.402385    |    0.163846 |     4 |
| phi3_medium    | deferred               | chi2   |   3.73847e-22 |    0.843274 |     4 |
| qwen2_5_7b     | unsupported_assumption | chi2   |   0.551064    |    0.142374 |     4 |
| qwen2_5_7b     | risk_rationalization   | none   | nan           |    0        |   nan |
| qwen2_5_7b     | deferred               | chi2   |   1.31896e-13 |    0.665218 |     4 |

## Uncertain conditions vs no-uncertainty control, hiring

Fisher's exact test, Holm-corrected across all rows; Cohen's h effect size.

| model          | signal                 |   rate_uncertain |   rate_control |   cohens_h |           p |      p_holm |
|:---------------|:-----------------------|-----------------:|---------------:|-----------:|------------:|------------:|
| deepseek_r1_7b | unsupported_assumption |        0.129412  |      0.0666667 |  0.21366   | 0.509026    | 1           |
| deepseek_r1_7b | risk_rationalization   |        0.0352941 |      0         |  0.377981  | 0.56623     | 1           |
| deepseek_r1_7b | gap_acknowledged       |        0.576471  |      0.1       |  1.08084   | 3.92483e-06 | 5.49477e-05 |
| llama3_8b      | unsupported_assumption |        0.0777778 |      0.0689655 |  0.0338109 | 1           | 1           |
| llama3_8b      | risk_rationalization   |        0.0777778 |      0         |  0.565269  | 0.192468    | 1           |
| llama3_8b      | gap_acknowledged       |        0.544444  |      0.206897  |  0.715375  | 0.00235034  | 0.0258538   |
| mistral_7b     | unsupported_assumption |        0.655556  |      0.464286  |  0.387851  | 0.0797036   | 0.717332    |
| mistral_7b     | risk_rationalization   |        0.611111  |      0         |  1.79489   | 8.45192e-10 | 1.26779e-08 |
| mistral_7b     | gap_acknowledged       |        0.277778  |      0.0714286 |  0.569143  | 0.0222525   | 0.222525    |
| phi3_medium    | unsupported_assumption |        0.0111111 |      0         |  0.211211  | 1           | 1           |
| phi3_medium    | risk_rationalization   |        0.0111111 |      0         |  0.211211  | 1           | 1           |
| phi3_medium    | gap_acknowledged       |        0.466667  |      0.0666667 |  0.981765  | 4.94892e-05 | 0.000593871 |
| qwen2_5_7b     | unsupported_assumption |        0.0111111 |      0.0333333 | -0.155997  | 0.439076    | 1           |
| qwen2_5_7b     | risk_rationalization   |        0         |      0         |  0         | 1           | 1           |
| qwen2_5_7b     | gap_acknowledged       |        0.422222  |      0.0333333 |  1.0474    | 2.81968e-05 | 0.000366558 |

## Logistic regression with response length as covariate, hiring

If condition effects survive controlling for log response length, the detector is not just measuring verbosity.

| model_key      | term                                                                 |   odds_ratio |     or_low |   or_high |            p | error            |
|:---------------|:---------------------------------------------------------------------|-------------:|-----------:|----------:|-------------:|:-----------------|
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |      4.89366 |   0.558315 |  42.8932  |   0.151649   | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |      5.75995 |   0.740702 |  44.7913  |   0.0942994  | nan              |
| deepseek_r1_7b | fit_failed                                                           |    nan       | nan        | nan       | nan          | math range error |
| llama3_8b      | fit_failed                                                           |    nan       | nan        | nan       | nan          | Singular matrix  |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |      1.45228 |   0.502385 |   4.19819 |   0.490859   | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |      2.93175 |   0.952183 |   9.02681 |   0.0608519  | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |      2.15294 |   0.718631 |   6.44999 |   0.170759   | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |      4.27609 |   1.3439   |  13.6059  |   0.0138757  | nan              |
| mistral_7b     | log_chars                                                            |     14.8211  |   2.36921  |  92.7165  |   0.00395141 | nan              |
| phi3_medium    | fit_failed                                                           |    nan       | nan        | nan       | nan          | math range error |
| qwen2_5_7b     | fit_failed                                                           |    nan       | nan        | nan       | nan          | math range error |

## Pairwise model differences in unsupported assumptions, hiring



| a              | b           |     rate_a |     rate_b |   cohens_h |           p |      p_holm |
|:---------------|:------------|-----------:|-----------:|-----------:|------------:|------------:|
| deepseek_r1_7b | llama3_8b   | 0.0902778  | 0.0671141  |  0.0862495 | 0.51884     | 1           |
| deepseek_r1_7b | mistral_7b  | 0.0902778  | 0.601351   | -1.16456   | 3.4819e-21  | 2.43733e-20 |
| deepseek_r1_7b | phi3_medium | 0.0902778  | 0.00666667 |  0.446874  | 0.000614608 | 0.00368765  |
| deepseek_r1_7b | qwen2_5_7b  | 0.0902778  | 0.0133333  |  0.378899  | 0.00284963  | 0.0142481   |
| llama3_8b      | mistral_7b  | 0.0671141  | 0.601351   | -1.25081   | 2.29292e-24 | 1.83434e-23 |
| llama3_8b      | phi3_medium | 0.0671141  | 0.00666667 |  0.360624  | 0.00541818  | 0.0216727   |
| llama3_8b      | qwen2_5_7b  | 0.0671141  | 0.0133333  |  0.292649  | 0.0197303   | 0.059191    |
| mistral_7b     | phi3_medium | 0.601351   | 0.00666667 |  1.61143   | 1.81467e-34 | 1.81467e-33 |
| mistral_7b     | qwen2_5_7b  | 0.601351   | 0.0133333  |  1.54346   | 6.0977e-33  | 5.48793e-32 |
| phi3_medium    | qwen2_5_7b  | 0.00666667 | 0.0133333  | -0.0679751 | 1           | 1           |

## Confidence behaviour, hiring

Brier/ECE use agreement with the normative policy as the correctness label.

| model          | mean_conf         |   distinct_values |   conf_no_uncertainty |   conf_missing |   conf_contradictory |   auroc_lower_conf_when_deficient |   brier_vs_policy |   ece_vs_policy |
|:---------------|:------------------|------------------:|----------------------:|---------------:|---------------------:|----------------------------------:|------------------:|----------------:|
| deepseek_r1_7b | 0.79 [0.77, 0.82] |                15 |                 0.947 |          0.693 |                0.936 |                             0.445 |             0.411 |           0.398 |
| llama3_8b      | 0.73 [0.72, 0.74] |                 4 |                 0.772 |          0.757 |                0.723 |                             0.431 |             0.171 |           0.046 |
| mistral_7b     | 0.69 [0.68, 0.71] |                 7 |                 0.736 |          0.678 |                0.718 |                             0.466 |             0.242 |           0.133 |
| phi3_medium    | 0.71 [0.70, 0.73] |                12 |                 0.887 |          0.648 |                0.692 |                             0.68  |             0.152 |           0.143 |
| qwen2_5_7b     | 0.73 [0.71, 0.74] |                 8 |                 0.84  |          0.703 |                0.713 |                             0.586 |             0.184 |           0.099 |

## Behavioural signal rates, loan (prompt p1_autonomous, sample 0)

Each cell: rate [Wilson 95% CI] (k/n).

| model_key      | unsupported_assumption   | fills_missing         | forward_looking        | extra_schema_fact     | risk_rationalization   | unjustified_confidence   | gap_acknowledged      | masked_overreach       | appropriate_restraint   | risky_commitment       |   n |
|:---------------|:-------------------------|:----------------------|:-----------------------|:----------------------|:-----------------------|:-------------------------|:----------------------|:-----------------------|:------------------------|:-----------------------|----:|
| deepseek_r1_7b | 11% [7, 15] (25/237)     | 8% [5, 12] (18/237)   | 1% [0, 4] (3/237)      | 1% [0, 3] (2/237)     | 2% [1, 4] (4/237)      | 2% [1, 5] (5/237)        | 25% [20, 31] (60/237) | 4% [2, 8] (10/237)     | 14% [10, 19] (34/237)   | 43% [37, 50] (103/237) | 237 |
| llama3_8b      | 0% [0, 2] (0/250)        | 0% [0, 2] (0/250)     | 0% [0, 2] (0/250)      | 0% [0, 2] (0/250)     | 0% [0, 2] (0/250)      | 0% [0, 2] (0/250)        | 6% [4, 10] (15/250)   | 0% [0, 2] (0/250)      | 55% [49, 61] (138/250)  | 5% [3, 9] (13/250)     | 250 |
| mistral_7b     | 76% [70, 81] (190/250)   | 20% [16, 26] (51/250) | 53% [47, 59] (132/250) | 17% [13, 22] (43/250) | 48% [42, 54] (120/250) | 6% [4, 10] (15/250)      | 23% [18, 29] (58/250) | 76% [70, 81] (190/250) | 14% [10, 19] (35/250)   | 0% [0, 2] (0/250)      | 250 |
| phi3_medium    | 6% [3, 9] (14/250)       | 6% [3, 9] (14/250)    | 0% [0, 2] (0/250)      | 0% [0, 2] (1/250)     | 4% [2, 7] (9/250)      | 0% [0, 2] (0/250)        | 10% [7, 15] (26/250)  | 6% [3, 9] (14/250)     | 55% [49, 61] (137/250)  | 0% [0, 2] (0/250)      | 250 |
| qwen2_5_7b     | 6% [3, 9] (14/250)       | 2% [1, 5] (5/250)     | 4% [2, 7] (9/250)      | 0% [0, 2] (0/250)     | 4% [2, 7] (10/250)     | 0% [0, 2] (0/250)        | 10% [7, 14] (24/250)  | 6% [3, 9] (14/250)     | 30% [25, 36] (75/250)   | 25% [20, 31] (62/250)  | 250 |

## Premise disclosure, loan

A model that lists no assumptions cannot score as unsupported, so signal rates must be read together with how often anything is stated. silent_risky_commitment: commits where the policy says defer, stating no assumption and acknowledging no gap.

| model          | assumption_stated      |   mean_assumptions | unsupported_given_stated   | escalated_share_of_assumptions   | missing_unacknowledged_in_missing   | silent_risky_commitment   |   n |
|:---------------|:-----------------------|-------------------:|:---------------------------|:---------------------------------|:------------------------------------|:--------------------------|----:|
| deepseek_r1_7b | 22% [18, 28] (53/237)  |               0.35 | 47% [34, 60] (25/53)       | 40% [31, 51] (34/84)             | 31% [20, 45] (15/48)                | 24% [19, 30] (58/237)     | 237 |
| llama3_8b      | 0% [0, 2] (0/250)      |               0    | n/a                        | n/a                              | 92% [81, 97] (46/50)                | 5% [3, 9] (13/250)        | 250 |
| mistral_7b     | 92% [88, 95] (231/250) |               1.32 | 82% [77, 87] (190/231)     | 68% [63, 73] (226/331)           | 28% [17, 42] (14/50)                | 0% [0, 2] (0/250)         | 250 |
| phi3_medium    | 9% [6, 13] (22/250)    |               0.11 | 64% [43, 80] (14/22)       | 59% [41, 75] (16/27)             | 56% [42, 69] (28/50)                | 0% [0, 2] (0/250)         | 250 |
| qwen2_5_7b     | 9% [6, 13] (22/250)    |               0.09 | 64% [43, 80] (14/22)       | 64% [43, 80] (14/22)             | 58% [44, 71] (29/50)                | 24% [19, 30] (60/250)     | 250 |

## Decisions and agreement with the normative policy, loan



| model          |   n | proceed               | defer                    | decline                | matches_policy         |
|:---------------|----:|:----------------------|:-------------------------|:-----------------------|:-----------------------|
| deepseek_r1_7b | 237 | 20% [15, 25] (47/237) | 22% [17, 27] (51/237)    | 59% [52, 65] (139/237) | 51% [45, 58] (122/237) |
| llama3_8b      | 250 | 23% [18, 29] (58/250) | 77% [71, 82] (192/250)   | 0% [0, 2] (0/250)      | 72% [66, 77] (179/250) |
| mistral_7b     | 250 | 0% [0, 2] (0/250)     | 100% [98, 100] (250/250) | 0% [0, 2] (0/250)      | 60% [54, 66] (151/250) |
| phi3_medium    | 250 | 8% [5, 12] (20/250)   | 92% [88, 95] (230/250)   | 0% [0, 2] (0/250)      | 68% [62, 74] (171/250) |
| qwen2_5_7b     | 250 | 28% [23, 34] (70/250) | 39% [33, 45] (98/250)    | 33% [27, 39] (82/250)  | 72% [66, 77] (179/250) |

## Unsupported assumptions by condition, loan



| model_key      | condition      | unsupported_assumption   | masked_overreach     | risky_commitment     |   n |
|:---------------|:---------------|:-------------------------|:---------------------|:---------------------|----:|
| deepseek_r1_7b | contradictory  | 4% [1, 14] (2/49)        | 0% [0, 7] (0/49)     | 84% [71, 91] (41/49) |  49 |
| deepseek_r1_7b | missing        | 29% [18, 43] (14/48)     | 15% [7, 27] (7/48)   | 48% [34, 62] (23/48) |  48 |
| deepseek_r1_7b | no_uncertainty | 2% [0, 12] (1/44)        | 0% [0, 8] (0/44)     | 0% [0, 8] (0/44)     |  44 |
| deepseek_r1_7b | normal         | 6% [2, 17] (3/47)        | 0% [0, 8] (0/47)     | 34% [22, 48] (16/47) |  47 |
| deepseek_r1_7b | stress         | 10% [4, 22] (5/49)       | 6% [2, 17] (3/49)    | 47% [34, 61] (23/49) |  49 |
| llama3_8b      | contradictory  | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| llama3_8b      | missing        | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 16% [8, 29] (8/50)   |  50 |
| llama3_8b      | no_uncertainty | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| llama3_8b      | normal         | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 10% [4, 21] (5/50)   |  50 |
| llama3_8b      | stress         | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | contradictory  | 78% [65, 87] (39/50)     | 78% [65, 87] (39/50) | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | missing        | 78% [65, 87] (39/50)     | 78% [65, 87] (39/50) | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | no_uncertainty | 84% [71, 92] (42/50)     | 84% [71, 92] (42/50) | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | normal         | 68% [54, 79] (34/50)     | 68% [54, 79] (34/50) | 0% [0, 7] (0/50)     |  50 |
| mistral_7b     | stress         | 72% [58, 83] (36/50)     | 72% [58, 83] (36/50) | 0% [0, 7] (0/50)     |  50 |
| phi3_medium    | contradictory  | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| phi3_medium    | missing        | 10% [4, 21] (5/50)       | 10% [4, 21] (5/50)   | 0% [0, 7] (0/50)     |  50 |
| phi3_medium    | no_uncertainty | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| phi3_medium    | normal         | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| phi3_medium    | stress         | 18% [10, 31] (9/50)      | 18% [10, 31] (9/50)  | 0% [0, 7] (0/50)     |  50 |
| qwen2_5_7b     | contradictory  | 16% [8, 29] (8/50)       | 16% [8, 29] (8/50)   | 28% [17, 42] (14/50) |  50 |
| qwen2_5_7b     | missing        | 10% [4, 21] (5/50)       | 10% [4, 21] (5/50)   | 28% [17, 42] (14/50) |  50 |
| qwen2_5_7b     | no_uncertainty | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 0% [0, 7] (0/50)     |  50 |
| qwen2_5_7b     | normal         | 0% [0, 7] (0/50)         | 0% [0, 7] (0/50)     | 30% [19, 44] (15/50) |  50 |
| qwen2_5_7b     | stress         | 2% [0, 10] (1/50)        | 2% [0, 10] (1/50)    | 38% [26, 52] (19/50) |  50 |

## Does the condition change behaviour? loan

Chi-square test of independence across the five conditions; Cramer's V as effect size.

| model          | signal                 | test   |             p |   cramers_v |   dof |
|:---------------|:-----------------------|:-------|--------------:|------------:|------:|
| deepseek_r1_7b | unsupported_assumption | chi2   |   8.48427e-05 |    0.317355 |     4 |
| deepseek_r1_7b | risk_rationalization   | chi2   |   0.0826256   |    0.186647 |     4 |
| deepseek_r1_7b | deferred               | chi2   |   2.26826e-07 |    0.392514 |     4 |
| llama3_8b      | unsupported_assumption | none   | nan           |    0        |   nan |
| llama3_8b      | risk_rationalization   | none   | nan           |    0        |   nan |
| llama3_8b      | deferred               | chi2   |   1.19332e-21 |    0.645914 |     4 |
| mistral_7b     | unsupported_assumption | chi2   |   0.38392     |    0.129099 |     4 |
| mistral_7b     | risk_rationalization   | chi2   |   1.44735e-17 |    0.583425 |     4 |
| mistral_7b     | deferred               | none   | nan           |    0        |   nan |
| phi3_medium    | unsupported_assumption | chi2   |   4.43468e-05 |    0.317946 |     4 |
| phi3_medium    | risk_rationalization   | chi2   |   1.52975e-07 |    0.386494 |     4 |
| phi3_medium    | deferred               | chi2   |   9.00478e-16 |    0.553644 |     4 |
| qwen2_5_7b     | unsupported_assumption | chi2   |   0.000711733 |    0.277266 |     4 |
| qwen2_5_7b     | risk_rationalization   | chi2   |   8.14256e-05 |    0.30957  |     4 |
| qwen2_5_7b     | deferred               | chi2   |   8.44983e-18 |    0.587189 |     4 |

## Uncertain conditions vs no-uncertainty control, loan

Fisher's exact test, Holm-corrected across all rows; Cohen's h effect size.

| model          | signal                 |   rate_uncertain |   rate_control |   cohens_h |           p |      p_holm |
|:---------------|:-----------------------|-----------------:|---------------:|-----------:|------------:|------------:|
| deepseek_r1_7b | unsupported_assumption |        0.143836  |      0.0227273 |   0.47532  | 0.0298814   | 0.231388    |
| deepseek_r1_7b | risk_rationalization   |        0.0273973 |      0         |   0.332573 | 0.575008    | 1           |
| deepseek_r1_7b | gap_acknowledged       |        0.390411  |      0         |   1.34982  | 1.24752e-08 | 1.74653e-07 |
| llama3_8b      | unsupported_assumption |        0         |      0         |   0        | 1           | 1           |
| llama3_8b      | risk_rationalization   |        0         |      0         |   0        | 1           | 1           |
| llama3_8b      | gap_acknowledged       |        0.0933333 |      0         |   0.620938 | 0.0231388   | 0.231388    |
| mistral_7b     | unsupported_assumption |        0.76      |      0.84      |  -0.200912 | 0.324224    | 1           |
| mistral_7b     | risk_rationalization   |        0.6       |      0         |   1.77215  | 1.84635e-16 | 2.76953e-15 |
| mistral_7b     | gap_acknowledged       |        0.373333  |      0.02      |   1.03088  | 1.22372e-07 | 1.59083e-06 |
| phi3_medium    | unsupported_assumption |        0.0933333 |      0         |   0.620938 | 0.0231388   | 0.231388    |
| phi3_medium    | risk_rationalization   |        0.06      |      0         |   0.494934 | 0.115559    | 0.577796    |
| phi3_medium    | gap_acknowledged       |        0.173333  |      0         |   0.858817 | 0.000441093 | 0.00529311  |
| qwen2_5_7b     | unsupported_assumption |        0.0933333 |      0         |   0.620938 | 0.0231388   | 0.231388    |
| qwen2_5_7b     | risk_rationalization   |        0.0666667 |      0         |   0.522315 | 0.0691709   | 0.415025    |
| qwen2_5_7b     | gap_acknowledged       |        0.16      |      0         |   0.823034 | 0.000808747 | 0.00889622  |

## Logistic regression with response length as covariate, loan

If condition effects survive controlling for log response length, the detector is not just measuring verbosity.

| model_key      | term                                                                 |   odds_ratio |     or_low |    or_high |             p | error            |
|:---------------|:---------------------------------------------------------------------|-------------:|-----------:|-----------:|--------------:|:-----------------|
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |     2.09015  |   0.156675 |  27.8838   |   0.577034    | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |    20.3338   |   2.1121   | 195.759    |   0.0091321   | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |     3.93742  |   0.325443 |  47.6374   |   0.28128     | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |     4.39591  |   0.411467 |  46.9638   |   0.22051     | nan              |
| deepseek_r1_7b | log_chars                                                            |     6.73732  |   2.92342  |  15.5268   |   7.52465e-06 | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |     0.779769 |   0.270106 |   2.25112  |   0.645603    | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |     0.592318 |   0.20365  |   1.72276  |   0.336337    | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |     0.326188 |   0.117833 |   0.902961 |   0.0310483   | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |     0.38533  |   0.136772 |   1.0856   |   0.0711449   | nan              |
| mistral_7b     | log_chars                                                            |    89.9486   |  14.8462   | 544.973    |   9.83008e-07 | nan              |
| phi3_medium    | fit_failed                                                           |   nan        | nan        | nan        | nan           | Singular matrix  |
| qwen2_5_7b     | fit_failed                                                           |   nan        | nan        | nan        | nan           | math range error |

## Pairwise model differences in unsupported assumptions, loan



| a              | b           |   rate_a |   rate_b |   cohens_h |           p |      p_holm |
|:---------------|:------------|---------:|---------:|-----------:|------------:|------------:|
| deepseek_r1_7b | llama3_8b   | 0.105485 |    0     |   0.661569 | 7.63647e-09 | 4.58188e-08 |
| deepseek_r1_7b | mistral_7b  | 0.105485 |    0.76  |  -1.45608  | 4.26097e-52 | 2.98268e-51 |
| deepseek_r1_7b | phi3_medium | 0.105485 |    0.056 |   0.18375  | 0.046703    | 0.140109    |
| deepseek_r1_7b | qwen2_5_7b  | 0.105485 |    0.056 |   0.18375  | 0.046703    | 0.140109    |
| llama3_8b      | mistral_7b  | 0        |    0.76  |  -2.11765  | 1.37961e-84 | 1.37961e-83 |
| llama3_8b      | phi3_medium | 0        |    0.056 |  -0.477819 | 0.000101243 | 0.000506215 |
| llama3_8b      | qwen2_5_7b  | 0        |    0.056 |  -0.477819 | 0.000101243 | 0.000506215 |
| mistral_7b     | phi3_medium | 0.76     |    0.056 |   1.63983  | 1.01066e-64 | 9.09598e-64 |
| mistral_7b     | qwen2_5_7b  | 0.76     |    0.056 |   1.63983  | 1.01066e-64 | 9.09598e-64 |
| phi3_medium    | qwen2_5_7b  | 0.056    |    0.056 |   0        | 1           | 1           |

## Confidence behaviour, loan

Brier/ECE use agreement with the normative policy as the correctness label.

| model          | mean_conf         |   distinct_values |   conf_no_uncertainty |   conf_missing |   conf_contradictory |   auroc_lower_conf_when_deficient |   brier_vs_policy |   ece_vs_policy |
|:---------------|:------------------|------------------:|----------------------:|---------------:|---------------------:|----------------------------------:|------------------:|----------------:|
| deepseek_r1_7b | 0.73 [0.70, 0.75] |                17 |                 0.908 |          0.628 |                0.697 |                             0.742 |             0.311 |           0.259 |
| llama3_8b      | 0.69 [0.68, 0.70] |                 6 |                 0.775 |          0.712 |                0.636 |                             0.601 |             0.208 |           0.087 |
| mistral_7b     | 0.63 [0.62, 0.65] |                 9 |                 0.656 |          0.577 |                0.65  |                             0.595 |             0.273 |           0.142 |
| phi3_medium    | 0.71 [0.70, 0.72] |                 9 |                 0.804 |          0.668 |                0.68  |                             0.638 |             0.234 |           0.188 |
| qwen2_5_7b     | 0.77 [0.76, 0.78] |                 8 |                 0.942 |          0.693 |                0.719 |                             0.766 |             0.217 |           0.153 |

## Behavioural signal rates, triage (prompt p1_autonomous, sample 0)

Each cell: rate [Wilson 95% CI] (k/n).

| model_key      | unsupported_assumption   | fills_missing         | forward_looking   | extra_schema_fact     | risk_rationalization   | unjustified_confidence   | gap_acknowledged      | masked_overreach      | appropriate_restraint   | risky_commitment      |   n |
|:---------------|:-------------------------|:----------------------|:------------------|:----------------------|:-----------------------|:-------------------------|:----------------------|:----------------------|:------------------------|:----------------------|----:|
| deepseek_r1_7b | 10% [6, 16] (14/144)     | 3% [1, 7] (4/144)     | 3% [1, 7] (4/144) | 5% [2, 10] (7/144)    | 6% [3, 11] (9/144)     | 6% [3, 11] (8/144)       | 22% [16, 29] (31/144) | 6% [3, 11] (8/144)    | 31% [24, 39] (45/144)   | 35% [28, 44] (51/144) | 144 |
| llama3_8b      | 1% [0, 5] (2/150)        | 1% [0, 4] (1/150)     | 0% [0, 2] (0/150) | 1% [0, 4] (1/150)     | 0% [0, 2] (0/150)      | 1% [0, 5] (2/150)        | 0% [0, 2] (0/150)     | 0% [0, 2] (0/150)     | 29% [22, 36] (43/150)   | 43% [36, 51] (65/150) | 150 |
| mistral_7b     | 38% [30, 46] (55/146)    | 18% [13, 26] (27/146) | 1% [0, 4] (1/146) | 21% [15, 28] (30/146) | 22% [16, 29] (32/146)  | 21% [15, 28] (30/146)    | 37% [30, 45] (54/146) | 29% [23, 37] (43/146) | 38% [30, 46] (55/146)   | 8% [5, 14] (12/146)   | 146 |
| phi3_medium    | 1% [0, 4] (1/150)        | 1% [0, 4] (1/150)     | 0% [0, 2] (0/150) | 0% [0, 2] (0/150)     | 1% [0, 4] (1/150)      | 0% [0, 2] (0/150)        | 3% [1, 7] (4/150)     | 1% [0, 4] (1/150)     | 69% [62, 76] (104/150)  | 2% [1, 6] (3/150)     | 150 |
| qwen2_5_7b     | 1% [0, 4] (1/150)        | 1% [0, 4] (1/150)     | 0% [0, 2] (0/150) | 0% [0, 2] (0/150)     | 1% [0, 4] (1/150)      | 0% [0, 2] (0/150)        | 0% [0, 2] (0/150)     | 1% [0, 4] (1/150)     | 55% [47, 62] (82/150)   | 17% [12, 23] (25/150) | 150 |

## Premise disclosure, triage

A model that lists no assumptions cannot score as unsupported, so signal rates must be read together with how often anything is stated. silent_risky_commitment: commits where the policy says defer, stating no assumption and acknowledging no gap.

| model          | assumption_stated      |   mean_assumptions | unsupported_given_stated   | escalated_share_of_assumptions   | missing_unacknowledged_in_missing   | silent_risky_commitment   |   n |
|:---------------|:-----------------------|-------------------:|:---------------------------|:---------------------------------|:------------------------------------|:--------------------------|----:|
| deepseek_r1_7b | 69% [61, 76] (99/144)  |               0.99 | 14% [9, 22] (14/99)        | 11% [7, 17] (15/142)             | 48% [31, 66] (14/29)                | 12% [8, 18] (17/144)      | 144 |
| llama3_8b      | 1% [0, 5] (2/150)      |               0.01 | 100% [34, 100] (2/2)       | 100% [34, 100] (2/2)             | 100% [89, 100] (30/30)              | 42% [34, 50] (63/150)     | 150 |
| mistral_7b     | 98% [94, 99] (143/146) |               1.63 | 38% [31, 47] (55/143)      | 25% [20, 31] (60/238)            | 17% [8, 35] (5/29)                  | 0% [0, 3] (0/146)         | 146 |
| phi3_medium    | 1% [0, 4] (1/150)      |               0.01 | 100% [21, 100] (1/1)       | 100% [21, 100] (1/1)             | 100% [89, 100] (30/30)              | 2% [1, 6] (3/150)         | 150 |
| qwen2_5_7b     | 1% [0, 5] (2/150)      |               0.01 | 50% [9, 91] (1/2)          | 50% [9, 91] (1/2)                | 100% [89, 100] (30/30)              | 17% [12, 23] (25/150)     | 150 |

## Decisions and agreement with the normative policy, triage



| model          |   n | proceed               | defer                  | decline               | matches_policy         |
|:---------------|----:|:----------------------|:-----------------------|:----------------------|:-----------------------|
| deepseek_r1_7b | 144 | 35% [27, 43] (50/144) | 40% [33, 48] (58/144)  | 25% [19, 33] (36/144) | 58% [50, 66] (84/144)  |
| llama3_8b      | 150 | 27% [21, 35] (41/150) | 32% [25, 40] (48/150)  | 41% [33, 49] (61/150) | 53% [45, 61] (80/150)  |
| mistral_7b     | 146 | 15% [10, 22] (22/146) | 77% [70, 83] (113/146) | 8% [4, 13] (11/146)   | 77% [70, 83] (113/146) |
| phi3_medium    | 150 | 20% [14, 27] (30/150) | 80% [73, 86] (120/150) | 0% [0, 2] (0/150)     | 88% [82, 92] (132/150) |
| qwen2_5_7b     | 150 | 36% [29, 44] (54/150) | 63% [55, 71] (95/150)  | 1% [0, 4] (1/150)     | 75% [68, 82] (113/150) |

## Unsupported assumptions by condition, triage



| model_key      | condition      | unsupported_assumption   | masked_overreach     | risky_commitment     |   n |
|:---------------|:---------------|:-------------------------|:---------------------|:---------------------|----:|
| deepseek_r1_7b | contradictory  | 3% [1, 17] (1/29)        | 3% [1, 17] (1/29)    | 48% [31, 66] (14/29) |  29 |
| deepseek_r1_7b | missing        | 10% [4, 26] (3/29)       | 10% [4, 26] (3/29)   | 48% [31, 66] (14/29) |  29 |
| deepseek_r1_7b | no_uncertainty | 7% [2, 23] (2/28)        | 0% [0, 12] (0/28)    | 0% [0, 12] (0/28)    |  28 |
| deepseek_r1_7b | normal         | 14% [6, 31] (4/28)       | 7% [2, 23] (2/28)    | 39% [24, 58] (11/28) |  28 |
| deepseek_r1_7b | stress         | 13% [5, 30] (4/30)       | 7% [2, 21] (2/30)    | 40% [25, 58] (12/30) |  30 |
| llama3_8b      | contradictory  | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 60% [42, 75] (18/30) |  30 |
| llama3_8b      | missing        | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 67% [49, 81] (20/30) |  30 |
| llama3_8b      | no_uncertainty | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| llama3_8b      | normal         | 3% [1, 17] (1/30)        | 0% [0, 11] (0/30)    | 50% [33, 67] (15/30) |  30 |
| llama3_8b      | stress         | 3% [1, 17] (1/30)        | 0% [0, 11] (0/30)    | 40% [25, 58] (12/30) |  30 |
| mistral_7b     | contradictory  | 24% [12, 42] (7/29)      | 24% [12, 42] (7/29)  | 7% [2, 22] (2/29)    |  29 |
| mistral_7b     | missing        | 79% [62, 90] (23/29)     | 59% [41, 74] (17/29) | 21% [10, 38] (6/29)  |  29 |
| mistral_7b     | no_uncertainty | 23% [12, 41] (7/30)      | 7% [2, 21] (2/30)    | 0% [0, 11] (0/30)    |  30 |
| mistral_7b     | normal         | 25% [13, 43] (7/28)      | 21% [10, 40] (6/28)  | 11% [4, 27] (3/28)   |  28 |
| mistral_7b     | stress         | 37% [22, 54] (11/30)     | 37% [22, 54] (11/30) | 3% [1, 17] (1/30)    |  30 |
| phi3_medium    | contradictory  | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| phi3_medium    | missing        | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 3% [1, 17] (1/30)    |  30 |
| phi3_medium    | no_uncertainty | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| phi3_medium    | normal         | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 7% [2, 21] (2/30)    |  30 |
| phi3_medium    | stress         | 3% [1, 17] (1/30)        | 3% [1, 17] (1/30)    | 0% [0, 11] (0/30)    |  30 |
| qwen2_5_7b     | contradictory  | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 57% [39, 73] (17/30) |  30 |
| qwen2_5_7b     | missing        | 3% [1, 17] (1/30)        | 3% [1, 17] (1/30)    | 20% [10, 37] (6/30)  |  30 |
| qwen2_5_7b     | no_uncertainty | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |
| qwen2_5_7b     | normal         | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 7% [2, 21] (2/30)    |  30 |
| qwen2_5_7b     | stress         | 0% [0, 11] (0/30)        | 0% [0, 11] (0/30)    | 0% [0, 11] (0/30)    |  30 |

## Does the condition change behaviour? triage

Chi-square test of independence across the five conditions; Cramer's V as effect size.

| model          | signal                 | test   |             p |   cramers_v |   dof |
|:---------------|:-----------------------|:-------|--------------:|------------:|------:|
| deepseek_r1_7b | unsupported_assumption | chi2   |   0.620512    |    0.13529  |     4 |
| deepseek_r1_7b | risk_rationalization   | chi2   |   0.123888    |    0.224179 |     4 |
| deepseek_r1_7b | deferred               | chi2   |   0.000319627 |    0.381696 |     4 |
| llama3_8b      | unsupported_assumption | chi2   |   0.551064    |    0.142374 |     4 |
| llama3_8b      | risk_rationalization   | none   | nan           |    0        |   nan |
| llama3_8b      | deferred               | chi2   |   0.000548978 |    0.363242 |     4 |
| mistral_7b     | unsupported_assumption | chi2   |   1.12006e-05 |    0.439727 |     4 |
| mistral_7b     | risk_rationalization   | chi2   |   5.13562e-05 |    0.413435 |     4 |
| mistral_7b     | deferred               | chi2   |   4.12845e-09 |    0.55469  |     4 |
| phi3_medium    | unsupported_assumption | chi2   |   0.402385    |    0.163846 |     4 |
| phi3_medium    | risk_rationalization   | chi2   |   0.402385    |    0.163846 |     4 |
| phi3_medium    | deferred               | chi2   |   5.08498e-24 |    0.87718  |     4 |
| qwen2_5_7b     | unsupported_assumption | chi2   |   0.402385    |    0.163846 |     4 |
| qwen2_5_7b     | risk_rationalization   | chi2   |   0.402385    |    0.163846 |     4 |
| qwen2_5_7b     | deferred               | chi2   |   1.62546e-18 |    0.772741 |     4 |

## Uncertain conditions vs no-uncertainty control, triage

Fisher's exact test, Holm-corrected across all rows; Cohen's h effect size.

| model          | signal                 |   rate_uncertain |   rate_control |   cohens_h |           p |     p_holm |
|:---------------|:-----------------------|-----------------:|---------------:|-----------:|------------:|-----------:|
| deepseek_r1_7b | unsupported_assumption |        0.0909091 |      0.0714286 |  0.0714552 | 1           | 1          |
| deepseek_r1_7b | risk_rationalization   |        0.0795455 |      0         |  0.571835  | 0.193142    | 1          |
| deepseek_r1_7b | gap_acknowledged       |        0.329545  |      0.0357143 |  0.842661  | 0.00112602  | 0.0146382  |
| llama3_8b      | unsupported_assumption |        0.0111111 |      0         |  0.211211  | 1           | 1          |
| llama3_8b      | risk_rationalization   |        0         |      0         |  0         | 1           | 1          |
| llama3_8b      | gap_acknowledged       |        0         |      0         |  0         | 1           | 1          |
| mistral_7b     | unsupported_assumption |        0.465909  |      0.233333  |  0.494301  | 0.0314743   | 0.377692   |
| mistral_7b     | risk_rationalization   |        0.295455  |      0         |  1.14934   | 0.000217485 | 0.00304479 |
| mistral_7b     | gap_acknowledged       |        0.522727  |      0.133333  |  0.868682  | 0.000202686 | 0.00304028 |
| phi3_medium    | unsupported_assumption |        0.0111111 |      0         |  0.211211  | 1           | 1          |
| phi3_medium    | risk_rationalization   |        0.0111111 |      0         |  0.211211  | 1           | 1          |
| phi3_medium    | gap_acknowledged       |        0.0444444 |      0         |  0.424824  | 0.570957    | 1          |
| qwen2_5_7b     | unsupported_assumption |        0.0111111 |      0         |  0.211211  | 1           | 1          |
| qwen2_5_7b     | risk_rationalization   |        0.0111111 |      0         |  0.211211  | 1           | 1          |
| qwen2_5_7b     | gap_acknowledged       |        0         |      0         |  0         | 1           | 1          |

## Logistic regression with response length as covariate, triage

If condition effects survive controlling for log response length, the detector is not just measuring verbosity.

| model_key      | term                                                                 |   odds_ratio |      or_low |   or_high |             p | error            |
|:---------------|:---------------------------------------------------------------------|-------------:|------------:|----------:|--------------:|:-----------------|
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |     0.537232 |   0.0445957 |   6.47188 |   0.624626    | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |     1.40966  |   0.213909  |   9.28971 |   0.721167    | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |     2.44001  |   0.395844  |  15.0404  |   0.336418    | nan              |
| deepseek_r1_7b | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |     2.15894  |   0.353632  |  13.1804  |   0.404399    | nan              |
| deepseek_r1_7b | log_chars                                                            |     1.83393  |   0.791687  |   4.24826 |   0.157079    | nan              |
| llama3_8b      | fit_failed                                                           |   nan        | nan         | nan       | nan           | Singular matrix  |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.contradictory] |     1.00838  |   0.300972  |   3.37847 |   0.98921     | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.missing]       |    14.1243   |   4.004     |  49.8242  |   3.83995e-05 | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.normal]        |     1.22805  |   0.362376  |   4.1617  |   0.741486    | nan              |
| mistral_7b     | C(condition, Treatment(reference='no_uncertainty'))[T.stress]        |     2.17591  |   0.688507  |   6.87657 |   0.185425    | nan              |
| mistral_7b     | log_chars                                                            |     0.275563 |   0.0398933 |   1.90345 |   0.19115     | nan              |
| phi3_medium    | fit_failed                                                           |   nan        | nan         | nan       | nan           | Singular matrix  |
| qwen2_5_7b     | fit_failed                                                           |   nan        | nan         | nan       | nan           | math range error |

## Pairwise model differences in unsupported assumptions, triage



| a              | b           |     rate_a |     rate_b |   cohens_h |           p |      p_holm |
|:---------------|:------------|-----------:|-----------:|-----------:|------------:|------------:|
| deepseek_r1_7b | llama3_8b   | 0.0972222  | 0.0133333  |  0.402727  | 0.0015085   | 0.006034    |
| deepseek_r1_7b | mistral_7b  | 0.0972222  | 0.376712   | -0.687468  | 1.70945e-08 | 1.19661e-07 |
| deepseek_r1_7b | phi3_medium | 0.0972222  | 0.00666667 |  0.470703  | 0.000305959 | 0.00183575  |
| deepseek_r1_7b | qwen2_5_7b  | 0.0972222  | 0.00666667 |  0.470703  | 0.000305959 | 0.00183575  |
| llama3_8b      | mistral_7b  | 0.0133333  | 0.376712   | -1.0902    | 1.58744e-17 | 1.26996e-16 |
| llama3_8b      | phi3_medium | 0.0133333  | 0.00666667 |  0.0679751 | 1           | 1           |
| llama3_8b      | qwen2_5_7b  | 0.0133333  | 0.00666667 |  0.0679751 | 1           | 1           |
| mistral_7b     | phi3_medium | 0.376712   | 0.00666667 |  1.15817   | 8.34106e-19 | 8.34106e-18 |
| mistral_7b     | qwen2_5_7b  | 0.376712   | 0.00666667 |  1.15817   | 8.34106e-19 | 8.34106e-18 |
| phi3_medium    | qwen2_5_7b  | 0.00666667 | 0.00666667 |  0         | 1           | 1           |

## Confidence behaviour, triage

Brier/ECE use agreement with the normative policy as the correctness label.

| model          | mean_conf         |   distinct_values |   conf_no_uncertainty |   conf_missing |   conf_contradictory |   auroc_lower_conf_when_deficient |   brier_vs_policy |   ece_vs_policy |
|:---------------|:------------------|------------------:|----------------------:|---------------:|---------------------:|----------------------------------:|------------------:|----------------:|
| deepseek_r1_7b | 0.80 [0.78, 0.82] |                10 |                 0.927 |          0.748 |                0.778 |                             0.637 |             0.334 |           0.338 |
| llama3_8b      | 0.77 [0.76, 0.78] |                 4 |                 0.763 |          0.773 |                0.797 |                             0.387 |             0.324 |           0.278 |
| mistral_7b     | 0.75 [0.74, 0.76] |                 7 |                 0.75  |          0.769 |                0.703 |                             0.565 |             0.184 |           0.037 |
| phi3_medium    | 0.77 [0.76, 0.78] |                 8 |                 0.87  |          0.74  |                0.722 |                             0.702 |             0.133 |           0.138 |
| qwen2_5_7b     | 0.79 [0.78, 0.81] |                 5 |                 0.932 |          0.75  |                0.832 |                             0.478 |             0.216 |           0.225 |

## Decision stability across seeded samples



| model          |   cases | identical_decision     |
|:---------------|--------:|:-----------------------|
| deepseek_r1_7b |     250 | 51% [45, 57] (127/250) |
| llama3_8b      |     250 | 74% [68, 79] (185/250) |
| mistral_7b     |     250 | 98% [95, 99] (245/250) |
| phi3_medium    |     250 | 88% [83, 91] (219/250) |
| qwen2_5_7b     |     250 | 75% [69, 80] (187/250) |
