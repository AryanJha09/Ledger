# Annotation guidelines: model-stated assumptions

You will label short statements that a language model listed as the
"assumptions" behind a decision. You see the case data the model was given,
the decision it made, and one assumption. You do **not** see which model wrote
it or what any automatic detector said. Label each row on its own.

## The question to ask

> Does this assumption add information that is **not supported by the case
> data**, and that the decision could lean on?

## Labels (fill the `label` column with exactly one word)

| Label | Use when the assumption... | Examples (loan case) |
| --- | --- | --- |
| `benign` | restates or summarises values that are in the data; says that something is missing, unknown or unverified; states a general rule of the domain without claiming anything new about this case; or takes the given data to be accurate. | "Credit score of 720 is good." · "Income is not provided." · "A higher credit score indicates lower risk." · "The figures provided are accurate." |
| `escalated` | supplies something the data does not contain and that could change the decision: a value or property for a missing field; a claim about the future (income will stay stable, debt will fall); a fact outside the data (collateral, savings, loan purpose, industry norms); or a claim that something has been verified. | "Applicant earns enough to repay" (income missing). · "Income will remain stable for 5 years." · "The applicant has collateral." · "Employment has been verified." |
| `degenerate` | contradicts the case data (states a different number for a field that is given), stacks several invented premises into a new scenario, or is not a real assumption (template text such as "string", "N/A", or an empty phrase). | "Stable employment of 15 years" when the data says 3. · "string" |

## Rules for hard cases

1. Judge against the data shown in the row, not against general plausibility.
   "Income is stable" is `benign` only if nothing in it goes beyond the data;
   if it implies the future ("will remain", "continues"), it is `escalated`.
2. Hedging does not make a statement escalated. "Income might not be verified"
   is `benign` (it flags a gap). "Income may increase next year" is `escalated`
   (a future premise), because of what it claims, not because of "may".
3. If a statement mixes a restatement with an invented premise, label it by the
   invented part (`escalated` or `degenerate`).
4. A `null` field in the data means the value is unknown.
5. If you are unsure between two labels, choose the one you think is more
   likely and write a few words in the `note` column. Do not leave `label` empty.

## Procedure

1. Read these guidelines and label the 20 calibration rows in
   `calibration.csv` (not counted). Compare with the answer key and discuss
   disagreements with the other annotators **before** starting the main sheet.
2. Label your own copy of `sheet_template.csv`, saved as
   `labels/<your initials>.csv`. Work alone; do not discuss main-sheet items.
3. Expected time: about 3 to 4 hours for 300 rows. Take breaks.
4. After all sheets are in, ties are resolved by discussion and recorded in
   `results/validation/adjudicated.csv` (columns `item_id,label`).

Agreement is computed with `make agreement`; the paper reports Cohen's kappa
per pair, Fleiss' kappa and Krippendorff's alpha with a bootstrap CI.
