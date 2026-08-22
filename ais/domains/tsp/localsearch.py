"""Local search operators over closed tours.

Core state class maintains:
  * ``tour``   : python list of city ids in visit order (implicit closing edge)
  * ``pos``    : pos[city] = index in tour
  * ``Dl``     : distance matrix as python lists (fast scalar access)
  * ``nl``     : neighbour lists as python lists (candidate pruning)
  * ``mask``   : don't-look bits (Bentley 1992)

Operators:
  * two_opt : first-improvement segment reversal, restricted to neighbour
              lists (complete w.r.t. 2-opt neighbourhood when nl_k == n-1)
  * or_opt  : segment relocation (lengths 1..3) with endpoint-neighbour
              insertion candidate sets

All operators preserve permutation validity and apply only strictly
improving moves (delta > EPS).
"""
from __future__ import annotations

import numpy as np

EPS = 1e-9


class TourState:
    __slots__ = ("inst", "tour", "pos", "Dl", "nl", "mask", "n", "moves")

    def __init__(self, inst, tour: list[int], nl_k: int | None = 16):
        self.inst = inst
        self.n = inst.n
        self.tour = list(tour)
        self.pos = [0] * self.n
        for i, c in enumerate(self.tour):
            self.pos[c] = i
        self.Dl = inst.d_list()
        self.nl = inst.k_nearest_lists(nl_k)
        self.mask = bytearray(self.n)          # 1 = don't look
        self.moves = 0                          # applied improving moves counter

    def length(self) -> float:
        D = self.Dl
        t = self.tour
        s = 0.0
        prev = t[-1]
        for c in t:
            s += D[prev][c]
            prev = c
        return s

    def copy_tour(self) -> list[int]:
        return list(self.tour)


# ---------------------------------------------------------------------------
# 2-opt
# ---------------------------------------------------------------------------

def _apply_reversal(st: TourState, p1: int, pb: int):
    """Reverse the shorter arc between p1..pb (inclusive, cyclic)."""
    tour, pos, n = st.tour, st.pos, st.n
    d = (pb - p1) % n + 1                     # arc length a..b inclusive
    if d <= n - d:
        steps = d >> 1
        for k in range(steps):
            i = (p1 + k) % n
            j = (pb - k) % n
            ci, cj = tour[i], tour[j]
            tour[i], tour[j] = cj, ci
            pos[ci] = j
            pos[cj] = i
    else:
        e = n - d                              # complementary arc length
        steps = e >> 1
        for k in range(steps):
            i = (pb + 1 + k) % n
            j = (p1 - 1 - k) % n
            ci, cj = tour[i], tour[j]
            tour[i], tour[j] = cj, ci
            pos[ci] = j
            pos[cj] = i


def two_opt_pass(st: TourState) -> bool:
    """One sweep over don't-look-clean cities; True if any move applied."""
    tour, pos, D, nl, mask, n = st.tour, st.pos, st.Dl, st.nl, st.mask, st.n
    improved = False
    for p1 in range(n):
        a = tour[p1]
        if mask[a]:
            continue
        found = False
        a_prev = tour[p1 - 1]
        Da_prev_row = D[a_prev]
        Da_row = D[a]
        for b in nl[a]:
            pb = pos[b]
            b_next = tour[(pb + 1) % n]
            if b == a or b_next == a:
                continue
            delta = Da_prev_row[a] + D[b][b_next] - Da_prev_row[b] - Da_row[b_next]
            if delta > EPS:
                _apply_reversal(st, p1, pb)
                mask[a_prev] = 0
                mask[b] = 0
                mask[b_next] = 0
                st.moves += 1
                improved = True
                found = True
                # refresh: city at p1 changed (now b); keep scanning its list
                a = tour[p1]
                a_prev = tour[p1 - 1]
                Da_prev_row = D[a_prev]
                Da_row = D[a]
        if not found:
            mask[a] = 1
    return improved


def two_opt(st: TourState) -> int:
    """Iterate sweeps until local optimum. Returns number of sweeps."""
    sweeps = 0
    while two_opt_pass(st):
        sweeps += 1
        if sweeps > 10 * st.n:      # safety guard (should never trigger)
            break
    return sweeps


# ---------------------------------------------------------------------------
# Or-opt
# ---------------------------------------------------------------------------

def _apply_relocation(st: TourState, p: int, L: int, anchor: int):
    """Move segment starting at p (length L) to directly after anchor."""
    tour, pos, n = st.tour, st.pos, st.n
    seg = [tour[(p + k) % n] for k in range(L)]
    rest = [tour[(p + L + k) % n] for k in range(n - L)]
    ia = rest.index(anchor)
    new_tour = rest[: ia + 1] + seg + rest[ia + 1:]
    for i, c in enumerate(new_tour):
        pos[c] = i
    st.tour[:] = new_tour


def or_opt_pass(st: TourState, lengths=(1, 2, 3)) -> bool:
    tour, pos, D, nl, mask, n = st.tour, st.pos, st.Dl, st.nl, st.mask, st.n
    improved = False
    for L in lengths:
        if L >= n:
            continue
        for p in range(n):
            s0 = tour[p]
            if mask[s0]:
                continue
            s_last = tour[(p + L - 1) % n]
            prev = tour[p - 1]
            after = tour[(p + L) % n]
            gain_rm = D[prev][s0] + D[s_last][after] - D[prev][after]
            best_delta = EPS
            best_u = -1
            seen = set()
            for anchor_city in (s0, s_last):
                for u in nl[anchor_city]:
                    if u in seen:
                        continue
                    seen.add(u)
                    pu = pos[u]
                    if ((pu - p) % n) < L or ((pu + 1 - p) % n) < L:
                        continue          # anchor or successor inside segment
                    v = tour[(pu + 1) % n]
                    c = D[u][s0] + D[s_last][v] - D[u][v]
                    delta = gain_rm - c
                    if delta > best_delta:
                        best_delta = delta
                        best_u = u
            if best_u >= 0:
                _apply_relocation(st, p, L, best_u)
                for c in (prev, s0, s_last, after, best_u):
                    mask[c] = 0
                st.moves += 1
                improved = True
            else:
                mask[s0] = 1
    return improved


def or_opt(st: TourState, lengths=(1, 2, 3)) -> int:
    rounds = 0
    while or_opt_pass(st, lengths):
        rounds += 1
        if rounds > 10 * st.n:
            break
    return rounds


# ---------------------------------------------------------------------------
# Composite local search
# ---------------------------------------------------------------------------

OPERATORS = {
    "two_opt": lambda st: two_opt(st),
    "or_opt": lambda st: or_opt(st),
    "or_opt1": lambda st: or_opt(st, lengths=(1,)),
    "none": lambda st: 0,
}


def run_local_search(st: TourState, operators=("two_opt",)) -> int:
    """Apply operators round-robin until a full round changes nothing."""
    ops = [o for o in operators if o != "none"]
    if not ops:
        return 0
    rounds = 0
    while True:
        any_change = False
        for op in ops:
            before = st.moves
            OPERATORS[op](st)
            if st.moves != before:
                any_change = True
        rounds += 1
        if not any_change or rounds > 50:
            break
    return rounds
