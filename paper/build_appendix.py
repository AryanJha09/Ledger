"""Generate sections/appendix.tex from the code so prompts and rules are verbatim.

    python paper/build_appendix.py
"""
import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ledger2 import dataset as ds  # noqa: E402
from ledger2.detectors import v2  # noqa: E402
from ledger2.domains import DOMAINS  # noqa: E402
from ledger2.prompts import PROMPTS  # noqa: E402


def verb(text):
    return "\\begin{scriptsize}\\begin{verbatim}\n" + text.strip("\n") + "\n\\end{verbatim}\\end{scriptsize}\n"


def tex(s):
    for a, b in [("\\", "\\textbackslash{}"), ("_", "\\_"), ("&", "\\&"), ("%", "\\%"), ("#", "\\#"),
                 ("$", "\\$"), ("{", "\\{"), ("}", "\\}")]:
        s = s.replace(a, b) if a != "\\" else s.replace(a, b)
    return s


out = ["\\section{Prompts}\\label{app:prompts}",
       "Prompts are shown for the first missing-condition loan case. \\texttt{p1\\_autonomous} is primary; "
       "\\texttt{p0\\_original} is the wording of our earlier version; \\texttt{p2\\_paraphrase} measures sensitivity."]
case = next(c for c in ds.build("loan", 1, 20261114) if c["condition"] == "missing")
for pid, fn in PROMPTS.items():
    out.append(f"\\paragraph{{{tex(pid)}}}")
    out.append(verb(fn(DOMAINS["loan"], case["input"])))

out.append("\\section{Normative policies}\\label{app:policy}")
for key, d in DOMAINS.items():
    out.append(f"\\paragraph{{{d.title.capitalize()}}} Decisions: " +
               ", ".join(f"\\texttt{{{w}}}$\\to${a}" for w, a in d.decisions.items()) + ".")
    out.append(verb(inspect.getsource(d.policy)))
    out.append("Warning signs:")
    out.append(verb(inspect.getsource(d.warning_signs)))

out.append("\\section{Detector rules (v2.0)}\\label{app:rules}")
for name in ["ACK_PATTERNS", "FORWARD_PATTERNS", "VERIFY_PATTERNS", "VALIDITY_PATTERNS"]:
    out.append(f"\\paragraph{{{tex(name)}}}")
    out.append(verb("\n".join(getattr(v2, name))))
out.append("\\paragraph{Classification procedure}")
out.append(verb(inspect.getsource(v2.classify_assumption)))
for key, d in DOMAINS.items():
    out.append(f"\\paragraph{{Field lexicons, {d.title}}}")
    out.append(verb("\n".join(f"{f.name}: {', '.join(f.lexicon)}" for f in d.fields)
                    + "\nextra-schema: " + ", ".join(d.extra_schema_lexicon)))

out.append("\\section{Annotation guideline}\\label{app:annotation}")
out.append("The full guideline given to annotators is reproduced below.")
out.append(verb((ROOT / "annotation" / "GUIDELINES.md").read_text()))

out.append("\\section{Detector errors}\\label{app:errors}")
out.append("\\res{Examples from results/validation/v2\\_errors.csv, correct and incorrect, per tag.}")

out.append("\\section{Reproducibility}\\label{app:repro}")
hashes = {k: ds.digest(ds.build(k, n, 20261114)) for k, n in [("loan", 50), ("triage", 30), ("hiring", 30)]}
out.append("Dataset seed 20261114. SHA-256 of the generated datasets: " +
           "; ".join(f"{k}: \\texttt{{{h[:16]}\\ldots}}" for k, h in hashes.items()) + ". "
           "Every table and figure is produced by \\texttt{make report} from the archived logs; "
           "the container image and model digests are listed in the released repository \\res{anonymous link}.")

(Path(__file__).parent / "sections" / "appendix.tex").write_text("\n\n".join(out) + "\n")
print("wrote sections/appendix.tex")
