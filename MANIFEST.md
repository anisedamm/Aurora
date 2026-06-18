# Interpretation manifest — defensive publication

This document is a tamper-evident, timestamped record of original
authorship over a body of conceptual-history readings. It is published
openly: the goal is to establish priority *and* keep the readings
available to scholarship, not to hide them.

- generated_at: `2026-06-18T18:16:29.613454+00:00`
- records: **15**
- chain head hash: `8d92511dff9a3c7f171fd2b3d936fc0839132d1b1456285861ba8c42bac22ab5`
- chain status: **intact**
- concepts: `democracy`, `revolution`
- record kinds: concept×3, framework×1, interpretation×5, reasoning×1, usage×5

Anchor the chain head hash above to a witness you do not control (commit
this file to git and push) to turn 'recorded' into real-world provable
'recorded by this date'.

| # | id | title | owner | source | kind | concept | sense | recorded_at | content_hash | align | anchor |
|---|----|-------|-------|--------|------|---------|-------|-------------|--------------|-------|--------|
| 0 | `language-framework` | Conceptual history as language interpretation | anise.damm | author | framework | — | — | 2026-06-18T18:16:29.534280+00:00 | `a6799dad6a98...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 1 | `thought-flow` | Thought flow — the living reasoning journal | anise.damm | collaboration | reasoning | — | — | 2026-06-18T18:16:29.584298+00:00 | `fed24b6d4ca2...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 2 | `glossary-map` | The authored glossary of conceptual histories | anise.damm | author | concept | — | — | 2026-06-18T18:16:29.599241+00:00 | `817201a8efa3...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 3 | `concept-revolution` | Concept: Revolution | anise.damm | author | concept | revolution | — | 2026-06-18T18:16:29.601071+00:00 | `8ba4c988bd27...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 4 | `rev-copernicus` | Usage: Copernicus, De revolutionibus orbium coelestium, 1543 | anise.damm | author | usage | revolution | — | 2026-06-18T18:16:29.601617+00:00 | `2a6057069e52...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 5 | `read-rev-copernicus` | Reading: revolutionibus as cyclical return (astronomical) | anise.damm | author | interpretation | revolution | celestial-return | 2026-06-18T18:16:29.603028+00:00 | `20e870e407e7...` | 0.50/0 | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 6 | `rev-1688` | Usage: English political pamphlet, c. 1689 (the Glorious Revolution) | anise.damm | author | usage | revolution | — | 2026-06-18T18:16:29.603852+00:00 | `49be3cdef53f...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 7 | `read-rev-1688` | Reading: revolution as return to a prior rightful order | anise.damm | author | interpretation | revolution | political-restoration | 2026-06-18T18:16:29.605171+00:00 | `0320c1653d68...` | 0.43/0 | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 8 | `rev-1789` | Usage: after the French Revolutionary press, c. 1791 | anise.damm | author | usage | revolution | — | 2026-06-18T18:16:29.606058+00:00 | `ae08d9684b38...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 9 | `read-rev-1789` | Reading: revolution as irreversible forward rupture | anise.damm | author | interpretation | revolution | irreversible-rupture | 2026-06-18T18:16:29.607199+00:00 | `9b0ca9c6ee90...` | 0.40/0 | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 10 | `concept-democracy` | Concept: Democracy | anise.damm | author | concept | democracy | — | 2026-06-18T18:16:29.608565+00:00 | `50c93ef4a418...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 11 | `dem-aristotle` | Usage: after Aristotle, Politics, 4th c. BCE | anise.damm | author | usage | democracy | — | 2026-06-18T18:16:29.609371+00:00 | `b0a5c2774299...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 12 | `read-dem-aristotle` | Reading: demokratia as rule by the unqualified many (pejorative) | anise.damm | author | interpretation | democracy | mob-rule | 2026-06-18T18:16:29.610940+00:00 | `b0a55ae9369c...` | 0.50/0 | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 13 | `dem-tocqueville` | Usage: after Tocqueville, Democracy in America, 1835 | anise.damm | author | usage | democracy | — | 2026-06-18T18:16:29.611794+00:00 | `f7e540f1d6d3...` | — | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |
| 14 | `read-dem-tocqueville` | Reading: democracy as legitimate popular self-government (honorific) | anise.damm | author | interpretation | democracy | popular-self-government | 2026-06-18T18:16:29.613126+00:00 | `14f97932e1e6...` | 0.45/0 | `git:2759d485b81ca40bd544d04522e434bcc50033b1` |

## How to verify

```bash
python -m interpretation verify     # recompute the chain; any edit breaks it
python -m interpretation manifest   # re-derive this file; head hash must match
```

A record's `source` says how it was produced (author vs mirror); its
`owner` says who holds priority. A mirror-produced reading names the
author-information and the attested usage it reflects in its lineage, so a
reflection can never be read as an origination.

`align` is `value/influence` — `value = purpose x fidelity` (descriptive,
faithfulness to the recorded usage, not absolute meaning) and `influence`
is how many downstream readings build on it. Alignment accrues as distinct
other readers corroborate a reading; it is shown, never enforced.
