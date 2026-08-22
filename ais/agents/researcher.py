"""Researcher agent: curated literature knowledge + gap analysis.

HONESTY NOTE
------------
The "literature" here is a structured summary of well-established,
textbook-level knowledge about TSP heuristics (Croes 1958; Lin 1965;
Bentley 1992; Martin/Otto/Felten 1991; Lourenço/Martin/Stützle 2003
ILS framework; Johnson & McGeoch 1997 experimental methodology). Claims
marked KNOWN are common knowledge in the field, not our findings. The
Researcher does NOT invent citations; it encodes design priors that the
experimental loop is then free to refute.
"""
from __future__ import annotations

from dataclasses import dataclass

EVIDENCE_KNOWN = "KNOWN_FACT"
EVIDENCE_HYPOTHESIS = "HYPOTHESIS"


@dataclass
class ResearchNote:
    topic: str
    claim: str
    evidence_class: str          # KNOWN_FACT | HYPOTHESIS | OUR_FINDING
    source: str                  # literature tag or 'this project: run set X'
    design_prior: dict | None = None   # suggestion for candidate space


LITERATURE: list[ResearchNote] = [
    ResearchNote(
        "2-opt", "First-improvement 2-opt with don't-look bits and neighbour "
        "lists gives near-best-known quality at a small fraction of full-scan "
        "cost on large instances.",
        EVIDENCE_KNOWN, "Bentley 1992; Johnson&McGeoch 1997",
        {"ls_operators": ("two_opt",), "nl_k": [8, 16, 40, None]}),
    ResearchNote(
        "or-opt", "Or-opt segment relocation (segments of length 1-3) escapes "
        "2-opt local optima; combined 2-opt+Or-opt dominates either alone in "
        "classical studies.",
        EVIDENCE_KNOWN, "Or 1976; Johnson&McGeoch 1997",
        {"ls_operators": [("two_opt", "or_opt"), ("or_opt1", "two_opt")]}),
    ResearchNote(
        "ils-kick", "Perturbation via random double-bridge plus local search "
        "with better-acceptance (basic ILS) strongly improves over repeated "
        "local search from scratch.",
        EVIDENCE_KNOWN, "Martin/Otto/Felten 1991; L/M/S 2003",
        {"perturbation": "double_bridge"}),
    ResearchNote(
        "acceptance", "Accepting some worsening moves (SA / threshold / LAHC) "
        "can help but interacts with kick strength; better-only acceptance "
        "with strong diversification is competitive when time is short.",
        EVIDENCE_HYPOTHESIS, "L/M/S 2003 (their Sec. on acceptance criteria)",
        {"acceptance": ["better", "threshold", "record_to_record", "sa", "lahc"]}),
    ResearchNote(
        "construction", "Construction quality matters less once ILS time "
        "budget grows; cheap NN construction is standard for ILS starts.",
        EVIDENCE_KNOWN, "Johnson&McGeoch 1997",
        {"construction": ["nn", "greedy", "cheapest_ins", "random"]}),
    ResearchNote(
        "kick-base", "Kicking from the incumbent best vs the current solution "
        "changes intensification/diversification balance; results are "
        "instance- and budget-dependent (no universal winner reported).",
        EVIDENCE_HYPOTHESIS, "L/M/S 2003 discussion",
        {"perturb_base": ["current", "best"]}),
]


class Researcher:
    """Maintains the knowledge base and proposes gaps worth testing."""

    def __init__(self):
        self.notes = list(LITERATURE)
        self.findings: list[ResearchNote] = []

    def add_finding(self, note: ResearchNote):
        assert note.evidence_class == "OUR_FINDING"
        self.findings.append(note)

    def gap_questions(self) -> list[str]:
        """Open questions this campaign should answer experimentally."""
        return [
            "Q1: At fixed 10 s budget, which acceptance criterion maximises "
            "mean quality across medium uniform instances?",
            "Q2: Does neighbour-list pruning (k=8..40) sacrifice measurable "
            "quality vs full scan at n<=200 within equal budgets?",
            "Q3: Do operator orderings (two_opt->or_opt vs or_opt1->two_opt) "
            "differ measurably?",
            "Q4: How do component effects scale with instance size "
            "(n=500..1000)?",
            "Q5: Are rankings robust across instance distributions "
            "(uniform/clustered/grid)?",
        ]

    def summarise(self) -> str:
        lines = ["## Literature knowledge base (curated)", ""]
        for nt in self.notes:
            lines.append(f"- [{nt.evidence_class}] {nt.topic}: {nt.claim} "
                         f"(source: {nt.source})")
        if self.findings:
            lines.append("")
            lines.append("## Findings recorded by this campaign")
            for nt in self.findings:
                lines.append(f"- [{nt.evidence_class}] {nt.topic}: {nt.claim} "
                             f"(source: {nt.source})")
        return "\n".join(lines)
