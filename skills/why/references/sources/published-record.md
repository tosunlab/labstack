# Published Record

## What this source contains

The published record is what the authors of a method or a number wrote and released. In research, the "why" of a design choice often lives here, and so does the setting behind a reported number.

- **The paper and its versions.** arXiv keeps every version public (v1, v2, ...), and the abstract page without a version number shows the latest. Versions mark submitted, revised, accepted, and published stages, errata, and expanded appendices. A number or setting can change between versions.
- **Appendix and supplementary material.** Hyperparameters, preprocessing, evaluation details, ablations, and "we tried X but it diverged" notes usually live here, not in the main text.
- **Released code, configs, and model cards.** The authors' repository at the paper's commit or tag, its configs and default arguments, its README, and model or dataset cards.
- **Review discussion.** OpenReview forums: reviews, author responses, comments, the meta-review and decision, and the paper's revision history. A reviewer's question and the authors' reply often state why a choice was made or what changed after review.
- **Errata, author issues, and later work.** Erratum versions, issues and discussions on the released repository ("can't reproduce Table 2"), and the authors' later papers that revise a setting.

## How to search it

Use web access, the arXiv and OpenReview APIs, or an MCP for them. Read the released repository with git, `gh`, or the web. Read only: post nothing, open no issues.

1. **Pin the version.** Identify which paper version the target follows (the anchor, a code comment, the citation in the repo). Read that version and the latest, and note the submission history on the abstract page. Cite versioned IDs (`arXiv:YYMM.NNNNNvN`).
2. **Read the full paper.** Search the text, tables, captions, footnotes, and appendices for the target's setting, symbol, or number. Record every place it appears and whether they agree.
3. **Read the released code at the paper's commit.** Find the commit or tag that matches the paper (README, release notes, a link in the paper). Read the config and code path that produce the reported number, and compare them with the setting the paper states.
4. **Read the review discussion.** Open the forum (`openreview.net/forum?id=<id>`). Read the reviews, author responses, and comments, and check the revision history for what changed. With the `openreview-py` client, fetch the submission with `details='replies'` for its discussion and `get_note_edits(<note_id>)` for its revisions.
5. **Search errata and author issues.** Search the released repository's issues and discussions for the setting, the number, "reproduce", and the table name. Check the venue page and later versions for errata, and the authors' later papers for a revised setting.

## What good evidence looks like here

- An appendix or footnote stating why a design choice was made ("we use X because Y diverged")
- An author response on OpenReview explaining a setting, or naming a change made after review
- A released config at the paper's commit that sets the target's value, or one that disagrees with the paper (a contradiction to surface, not resolve)
- A repository issue where the authors confirm the setting behind a reported number, or acknowledge an error
- A later version or erratum that changes the number

## Common pitfalls

- **Wrong version.** The abstract page shows the latest version, and numbers, settings, and appendices change between versions. Cite the version you read.
- **Paper vs. released code.** The released config, model card, or default arguments can state a different setting from the one the paper reports. Record both with citations. Don't pick one.
- **Unstated evaluation details.** A reported number depends on an evaluation stack the paper may not state in full: metric parameters, tokenization and preprocessing, prompt format, number of shots, normalization. The same metric name can hide different settings. Record what the paper states and list what it leaves out.
- **"Standard" or "default".** A setting the paper calls standard that the released code does not pin is unspecified. List it; don't fill it in.
- **Post-hoc rationale.** A reason given in a camera-ready version may have been written after the choice was made. Note the version where it first appears.
- **Knowledge-only MCPs.** The `openreview-mcp` server helps write `openreview-py` calls but fetches no submissions or reviews. Use the API or the forum page for the record itself.
- **Access limits.** Some OpenReview content is visible only to certain readers, and a withdrawn arXiv version has no full text. Note what you couldn't read as a gap.

## What to return

For each relevant item:
- Paper title and versioned ID or DOI, and which versions you read
- Each relevant passage verbatim, with section, table, figure, footnote, or appendix location
- Released repository URL, the commit or tag you read, and file:line of the relevant config or code
- OpenReview forum URL and the note quoted (review, response, comment), with author role and date
- Issues or errata: URL, author, date, and quote
- Where the paper versions, appendix, config, and code agree or disagree on the target

Sources: SOURCES.md entries `arxiv-versions`, `openreview-docs`, `openreview-mcp`, `reclaim`, `sacrebleu-clarity`, `olmes`.
