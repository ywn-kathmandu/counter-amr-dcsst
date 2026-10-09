# Before this repo goes public

Delete this file once the list is done.

## Gates — either of these can stop publication outright

- [ ] **Is TDR review for CA26-0034 anonymised or blinded?** A public repo carrying
      institution names, author names and commit-author emails de-anonymises the application.
      If review is blinded, **do not publish** — submit the technology brief with screenshots
      instead.
- [ ] **Does the eTDR submission portal have a field for a URL?** TDR submissions run through
      structured portals with fixed fields and named attachments. If there is no field for it,
      the link must live inside the technology brief; it is not a separate deliverable.

## Ownership and attribution

- [ ] `LICENSE` has a placeholder copyright line. Fill in the agreed holder.
- [ ] **Get YWN's agreement in writing** before describing the tool as a YWN product or
      placing the repo under YWN's organisation. This is an IP statement about another
      institution and should not first appear in a document submitted to WHO.
- [ ] `CITATION.cff` has placeholder authors and ORCIDs. Fill in, or delete the file.
- [ ] Confirm the provenance narrative in the proposal matches what actually happened. If the
      AMR-at-the-counter concept originated on the Sncho side rather than with YWN, say so —
      an existing lookup tool offered to a research team that needed a counter-level
      instrument is just as strong a story and nobody can contradict it.

## Data rights

- [ ] **Confirm redistribution rights for the DDA-derived register** before publishing
      `data/brands.json` and `data/nonab.json`. The DDA source is public, the enrichment and
      the brand–generic crosswalk are your work. If rights are unclear, ship a sample subset
      and state that the full crosswalk is available to the study team and will be deposited
      at study end.

## Hygiene

- [ ] Squash history into a single initial commit, or check the existing history for author
      emails, test data and anything else you would not publish.
- [ ] Repo description and topics set; no Sncho branding in either.
- [ ] Enable GitHub Pages (Settings → Pages → `main`, folder `/`), then put the resulting URL
      into the README's "Live demo" line and into the technology brief.
- [ ] Open the Pages URL on a phone. The tool is built for a counter tablet and reviewers read
      on phones.

## Known content notes

- The tool auto-loads 190 simulated sales on first visit so the analysis screens are not
  empty. This is labelled on the Surveillance and Dispensing-log screens and in the header
  bar. **Do not describe any of those numbers as findings** anywhere in the application.
- Fonts load from Google Fonts, so the demo needs a network connection. True offline operation
  would need the fonts embedded.
