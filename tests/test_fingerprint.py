"""Fingerprinting: integrity is exact, recognition is a similarity proxy."""

from __future__ import annotations

from interpretation.fingerprint import fingerprint, jaccard, normalize, shingles


def test_normalize_sees_through_cosmetic_edits():
    assert normalize("The Revolution, restored!") == "the revolution restored"


def test_shingles_fall_back_to_unigrams_when_short():
    assert shingles("revolution") == frozenset({"revolution"})
    assert "a turning back" in shingles("a turning back to order")


def test_identical_text_is_recognised_verbatim():
    a = fingerprint("a return to a prior rightful order")
    b = fingerprint("a return to a prior rightful order")
    assert a.content_hash == b.content_hash
    assert jaccard(a.signature, b.signature) == 1.0


def test_paraphrase_is_recognised_but_not_identical():
    a = fingerprint("an irreversible forward break that founds a new order")
    b = fingerprint("an irreversible forward break that establishes a fresh regime")
    sim = jaccard(a.signature, b.signature)
    assert 0.0 < sim < 1.0  # a proxy: similar, not the same


def test_disjoint_text_does_not_collide():
    a = fingerprint("the revolving of the heavenly spheres")
    b = fingerprint("equality of conditions among the people")
    assert jaccard(a.signature, b.signature) < 0.2


def test_empty_passage_is_never_recognised():
    a = fingerprint("")
    b = fingerprint("anything at all here")
    assert jaccard(a.signature, b.signature) == 0.0
