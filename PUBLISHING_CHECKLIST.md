# Open items before submission

Updated 12 October 2026, after external technical review.

## Resolved in code

- [x] Field build with no seeded demonstration data (`field.html`)
- [x] Phase fixed by cluster activation date in the field build; inert at the counter
- [x] Baseline no longer assumes a sale — silent phase asks dispensed / referred /
      not dispensed, so a baseline referral is recorded as a referral
- [x] Counselling labels carry no instruction during baseline; tick boxes retained
- [x] Unassessed components never count as concordant; outcome left unscorable instead
- [x] `components_unassessed` and `outcome_unscorable` exported per row
- [x] Real CSV download and a one-file daily backup bundle
- [x] Interface text no longer describes a study server that does not exist
- [x] `LICENSE` and `CITATION.cff` placeholders removed
- [x] `STANDARDS.md` — classifications used, and why a self-contained instrument is correct
      for a counter where no prescription arrives
- [x] 60 regression assertions, each pinning a reviewed defect

## Still needed from people, not from code

- [ ] **Written ownership and attribution agreement** between YWN and Sncho. `LICENSE` names
      both jointly and says so provisionally. This must be signed, not assumed.
- [ ] **Panel sign-off** on `DC-SST_panel_decision_log.xlsx` — 415 products and 53
      molecule-level calls. Sheet 4 first.
- [ ] **Freeze the outcome algorithm** and test it against independently adjudicated
      examples before recruitment, as the review asks. The scoring is now deterministic and
      covered by tests; what is missing is a set of encounters scored by hand by two
      reviewers and compared against the tool.
- [ ] **Decide the encounter definition in the protocol** and make the text match the data
      model: every eligible antibiotic-related encounter is recorded, with dispensing status
      stored separately. The software now supports this; the protocol wording must agree.
- [ ] **Confirm whether TDR review is anonymised.** If it is, do not link the public
      repository; submit the technology brief with screenshots instead.

## Upload note

The GitHub upload on 9 October missed `src/` and `data/` — only top-level files went up.
When re-uploading, drag the **folders** themselves, not their contents, and confirm the file
list shows paths like `src/build.py` before committing.
