---
venue: NeurIPS
year: 2026
full_name: Conference on Neural Information Processing Systems (Main Track)
source_urls:
  - https://neurips.cc/Conferences/2026/ReviewerGuidelines
  - https://neurips.cc/Conferences/2026/MainTrackHandbook
  - https://neurips.cc/public/guides/PaperChecklist
  - https://neurips.cc/Conferences/2026/ai-reviewing-experiment
  - https://neurips.cc/Conferences/2026/CallForPapers
  - https://neurips.cc/public/EthicsGuidelines
  - https://blog.neurips.cc/2026/03/23/refining-the-review-cycle-neurips-2026-area-chair-pilot/
fetched: 2026-09-26
verified_by_human: false   # set to true after you check this file against the sources
---

# NeurIPS 2026 reviewer profile

Scope: Main Track only. The Evaluations & Datasets, Position Paper, and Competition tracks have their own guidelines and are not covered here. The review form below comes from the "Review Form" section of the Main Track Handbook (version V2026.3). No separate reviewer tutorial or FAQ page for 2026 was found on neurips.cc; the reviewer FAQs are part of the Handbook.

## What reviewers are asked to evaluate
- Review the paper against four core criteria: **Quality, Clarity, Significance, Originality**. How each criterion is read depends on the **Contribution Type** the authors chose. The five types are General, Theory, Use-Inspired, Concept & Feasibility, and Negative Results. Every type uses the same form. The type cannot be changed after submission, by the authors or by the reviewers.
- **General type**:
  - Quality: technical soundness, well-supported claims, appropriate methods, a complete piece of work, and an honest account of strengths and weaknesses.
  - Clarity: clear writing and organization. The paper should give an expert enough information to reproduce the results.
  - Significance: impact on the community, likelihood that others will use or build on the work, and whether it advances understanding in a demonstrable way.
  - Originality: new insights, a clear difference from prior work with citations, and novel tasks, framings, metrics, methods, or combinations. Originality "does not necessarily require introducing an entirely new method". Novel insights from evaluating existing methods, or gains in efficiency or fairness, are "equally valuable".
- **Theory type**: Quality means mathematical rigor and correctness. Reviewers need not verify every line, but they should examine the core arguments. Assumptions are judged against the novelty of the result and the norms of the literature. Empirical validation is **not** required. Clarity means intuition alongside rigor and a clear scope. Significance means new abstractions or formulations, or progress on established problems. Originality can come from new proof techniques or from tools borrowed from other fields.
- **Use-Inspired type**: the use case must be real and meaningful, and the design must fit it. Expect "non-standard" datasets and encourage them when justified. Clarity is judged for an ML audience, so domain jargon should be explained. Prior non-ML work should also be considered, and new methods compared against commonly used non-ML approaches. Originality need not mean wholly new methods.
- **Concept & Feasibility type**: claims must be strongly supported even if the full scope cannot be validated in one paper. The bars for significance and originality are high: the work should have potential to change paradigms or practice.
- **Negative Results type**: the result must rest on grounded analysis, not just an experiment that failed. Significance and originality bars are high: the result should change how the community approaches a question and be surprising or run counter to common belief. The paper need not offer a mitigation.
- A good review is a narrative, not bullet points. It covers the four dimensions, is fair, precise, and substantiated, and focuses on technical content rather than only organization or grammar. For example, a novelty objection should come with references.
- Questions should be actionable (ideally 3-5). Reviewers are strongly encouraged to state what would raise or lower their score.
- During the discussion, reviewers should read all reviews, the initial AC meta-review, and the author responses. They should update their review when their view changes, or acknowledge that they read the response when it does not.

## What reviewers are told NOT to do
- Do not write superficial or uninformed reviews without evidence. These are "worse than no review". Vague novelty claims without references are named as an example.
- Do not let personal feelings affect the review. Avoid rude or offensive wording (reviews of accepted papers are made public).
- Do not paste the abstract as the summary, and do not critique the paper in the summary.
- Do not penalize authors for being upfront about limitations or negative societal impact. Answering "no" to checklist questions is typically not grounds for rejection.
- Do not penalize a Theory paper for lacking experiments.
- Do not suggest new experiments without saying what question they would answer. Remember that authors may lack large compute to run significant experiments in a short period.
- Do not lower the overall score for perceived formatting or anonymity violations. Report them in the "Paper Formatting Concerns" field instead. Do not worry about minor violations, such as a few lines over the limit or the checklist in the wrong order. Report major violations to the AC.
- Do not both lower the score before an ethics review and flag the paper for a major ethics concern.
- Do not try to find out author identities, for example by searching arXiv. Do not actively look for preprints; coming across one is not a conflict of interest.
- If you have seen the work at a non-archival workshop, do not mention the workshop paper in your review.
- Do not actively seek out previous reviews of a resubmission (having already read them is okay). If you reviewed the paper at another venue, do not assume it is unchanged.
- Do not involve sub-reviewers.
- Do not share or discuss submissions with anyone, including unsanctioned LLMs. Do not use ideas, code, or results from submissions. Do not discuss assigned papers with reviewers, ACs, or SACs who are not assigned to the same paper.
- Do not use LLMs unless the paper is specifically allowed to use the sanctioned LLM (see LLM policy below).
- Reviewers do not have to match the conference acceptance rate. Judge each paper on its own merits.
- Do not run submitted code outside a secure environment. Docker, a VM, or a network-isolated cloud instance is recommended.
- Rejecting for lack of SOTA: there is no explicit instruction to reviewers. The AC section of the Handbook says "new approaches can't initially yield state-of-the-art competitive results, nor do all papers require extensive computational experiments" (unconfirmed as reviewer-facing guidance).

## Concurrent-work policy
From the Main Track Handbook, "Contemporaneous Work": papers that appeared online **after March 1st, 2026** are generally treated as contemporaneous. A submission will not be rejected on the basis of a comparison to contemporaneous work. Authors are still expected to cite and discuss contemporaneous work and to compare empirically as far as feasible. Any paper that influenced the submission counts as prior work and must be cited as such. Submissions very similar to contemporaneous work get extra scrutiny for plagiarism or missing credit. arXiv papers and published conference or journal papers are treated the same way. The handling AC makes more nuanced calls, such as how to determine the publication date. (Full paper deadline: May 6, 2026 AoE.)

Related rule: other archival submissions by an overlapping set of authors count as prior work (dual-submission policy). Authors may submit work already posted as a preprint without citing it.

## Review form
Field names follow the Handbook. The Handbook does not show the OpenReview widget types, the required/optional status of each field, or whether any post-rebuttal field exists (for example a final justification). All of these are unconfirmed.

| # | Field | Type | Scale / options | Instructions to reviewers |
|---|-------|------|-----------------|---------------------------|
| 1 | Summary | text | – | Briefly summarize the paper and its contributions in your own words. This is not the place to critique, and not the place to paste the abstract. The authors should generally agree with a well-written summary. |
| 2 | Contribution Type (field label unconfirmed) | choice | General / Theory / Use-Inspired / Concept & Feasibility / Negative Results (exact option labels in the form unconfirmed) | Select the submission's Contribution Type to confirm that you have read the Reviewing Guidelines for that type. |
| 3 | Strengths and Weaknesses | text | – (Markdown and LaTeX allowed) | A narrative review, not just bullet points. Give your understanding of the paper, highlight issues, and address Quality, Clarity, Significance, and Originality as interpreted for the Contribution Type. |
| 4 | Quality | score | 1-4 | Rate Quality based on your review. The definition depends on the Contribution Type. |
| 5 | Clarity | score | 1-4 | Rate Clarity. The definition depends on the Contribution Type. |
| 6 | Significance | score | 1-4 | Rate Significance. The definition depends on the Contribution Type. |
| 7 | Originality | score | 1-4 | Rate Originality. The definition depends on the Contribution Type. |
| 8 | Questions | text | – | Questions and suggestions (ideally 3-5), focused on actionable key points where an author response could change your opinion, clear up a confusion, or address a limitation. State what would raise or lower your score. If you suggest experiments, say which question they answer and keep authors' compute limits in mind. |
| 9 | Limitations | text | – | Have the authors adequately addressed the limitations and implications of their work? If yes, simply write "yes". If not, give constructive suggestions. Reward rather than punish candor about limitations and negative societal impact. |
| 10 | Overall | score | 1-6 | Overall score for the submission (labels below). |
| 11 | Confidence | score | 1-5 | How confident you are in your evaluation (labels below). |
| 12 | Ethical concerns | checkbox | "NO or VERY MINOR ethics concerns only", "CLEAR MAJOR CONCERN", plus 8 "Major Concern: …" categories (below) | If there are significant ethics concerns that need an ethics expert, flag every major concern that applies. Otherwise select only the first checkbox. See the NeurIPS Ethics Guidelines. Do not both lower the score before the ethics review and flag. |
| 13 | Paper Formatting Concerns | text | – | List any major formatting or anonymity violations. Do not lower the overall score because of them; report them here. Follow the NeurIPS 2026 Paper Formatting Instructions. |
| 14 | Code of conduct acknowledgement | checkbox (type unconfirmed) | acknowledgement (option label unconfirmed) | "While performing my duties as a reviewer (including writing reviews and participating in discussions), I have and will continue to abide by the NeurIPS code of conduct … including the policies for LLM use." |
| 15 | Responsible reviewing acknowledgement | checkbox (type unconfirmed) | acknowledgement (option label unconfirmed) | "I acknowledge I have read the information about the 'responsible reviewing initiatives' and will abide by that." |

## Score meanings

**Quality / Clarity / Significance / Originality** (same scale for each):
- 4: excellent
- 3: good
- 2: fair
- 1: poor

**Overall**:
- 6: Strong Accept: Technically flawless paper with groundbreaking impact on one or more areas of AI, with exceptionally strong evaluation, reproducibility, and resources, and no unaddressed ethical considerations.
- 5: Accept: Technically solid paper, with high potential value on at least one sub-area of AI or moderate-to-high impact on more than one area of AI, with good-to-excellent evaluation, resources, reproducibility, and no unaddressed ethical considerations.
- 4: Borderline accept: Technically solid paper where reasons to accept outweigh reasons to reject, e.g., limited evaluation. Please use sparingly.
- 3: Borderline reject: Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. Please use sparingly.
- 2: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
- 1: Strong Reject: For instance, a paper with well-known results or unaddressed ethical considerations.

**Confidence**:
- 5: You are absolutely certain about your assessment. You are very familiar with the related work and checked the math/other details carefully.
- 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.
- 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
- 2: You are willing to defend your assessment, but it is quite likely that you did not understand the central parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
- 1: Your assessment is an educated guess. The submission is not in your area or the submission was difficult to understand. Math/other details were not carefully checked.

**Ethical concerns** (checkbox options, in order):
- NO or VERY MINOR ethics concerns only
- CLEAR MAJOR CONCERN: Check this box if there is a clear, major concern for which you do not need further clarifications. Detail the concern in the Strengths and Weaknesses section. Use another option below if you would benefit from a consultation with an expert.
- Major Concern: Improper research involving human subjects
- Major Concern: Data privacy, copyright, and consent
- Major Concern: Data quality and representativeness
- Major Concern: Safety and security
- Major Concern: Discrimination, bias, and unfairness
- Major Concern: Deception and harassment
- Major Concern: Environmental impact
- Major Concern: Human rights (including surveillance)

## Other policies relevant to feedback
- **Paper checklist: how reviewers should use it.** The checklist is mandatory and comes after the references and appendices in the PDF. Papers without it are desk rejected. Reviewers are told they may use it as a tool when preparing the review, and the checklist guidelines say reviewers "will be asked to use the checklist as one of the factors in their evaluation." Answering "no" or "n/a" is typically not grounds for rejection, as long as a proper justification is given. Reviewers are "specifically instructed to not penalize honesty concerning limitations." Reviewers should also think about whether critical points are missing and give them as feedback. Checklist items:
  1. Claims
  2. Limitations
  3. Theory, Assumptions and Proofs
  4. Experimental Result Reproducibility
  5. Open Access to Data and Code
  6. Experimental Setting/Details
  7. Experiment Statistical Significance
  8. Experiments Compute Resource
  9. Code of Ethics
  10. Broader Impacts
  11. Safeguards
  12. Licenses
  13. Assets
  14. Crowdsourcing and Research with Human Subjects
  15. IRB Approvals
  16. Declaration of LLM usage
- **Code**: NeurIPS does not require code, but every paper must give some reasonable path to reproducibility. "Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark)."
- **Limitations and broader impact**: a "broader impacts" section is not required, but authors should consider negative societal impact somewhere in the paper. Reward candor. The Limitations form field can simply say "yes" if limitations are handled adequately.
- **Supplementary material**: reviewers are not required to read it but are welcome to. Appendices come in the same PDF, and code and data come as a separate ZIP of up to 100MB.
- **Page limit**: 9 content pages. References, appendices, and the checklist do not count. Camera-ready papers get one more page. Minor overruns should not concern reviewers.
- **Rebuttal**: authors may not revise the paper or supplement during the response period. The per-review rebuttal limit is 10,000 characters, with no files and no links, except an anonymized code link sent to the AC if reviewers asked for code. Rebuttals may include new results, but "your original submission will serve as the basis for the reviewers' (and ACs') acceptance recommendations." ACs write an **initial meta-review before the author response** (new in 2026) naming the critical concerns. Reviewers see it too.
- **Ethics review**: reviewers may flag papers for the ethics committee. Ethics reviewers cannot reject papers, but PCs may reject on ethical grounds in extreme cases. If a concern is clear, such as work that increases the lethality of autonomous weapons, reviewers should flag it to the AC instead of requesting an ethics review.
- **LLM policy for reviewers (Main Track, 2026)**: reviewers "must not use LLMs except for papers where this is specifically allowed, and must only use the sanctioned LLM in such cases rather than other LLMs." Use is allowed only through the voluntary AI-Assisted Reviewing Experiment. It applies only where the authors opted the paper in and the reviewer volunteered. Each reviewer-paper pair is randomly assigned one condition:
  - Condition 1: no LLM
  - Condition 2: open-ended LLM
  - Condition 3: structured LLM
  
  In Conditions 2 and 3, only the LLM provided inside OpenReview may be used. "Except for this review experiment, NeurIPS does not sanction any other use of LLMs during the review process". Other use "may result in consequences for reviewers and their submitted papers, including desk rejection." The LLM is meant to support the reviewer, "not intended to replace reviewer judgment or produce a review on the reviewer's behalf." Reviewers who are allowed the sanctioned LLM should know that authors may have tuned their text to get favorable LLM outputs. Authors are banned from prompt injection.
  
  The Handbook says the experiment details "may change". It also says "every reviewer will have some papers" with LLM support. The experiment page, by contrast, describes participation as voluntary opt-in. This mismatch is unresolved; follow the experiment page and the assignment notices in OpenReview (unconfirmed which is final).
- **Responsible reviewing**: reviewer-authors cannot see reviews of their own papers until they finish all of their own reviews. ACs and SACs flag low-quality or placeholder reviews. Reviewers must engage with author responses. Grossly negligent reviewer-authors may have their own papers desk rejected at the meta-review stage. The 2026 responsible-reviewing blog post named in the form returns 404, and the Handbook's hyperlink points to the 2025 post (2026 details unconfirmed beyond the Handbook text).
- **Public reviews**: reviews, meta-reviews, and author discussions of accepted papers are made public, with reviewers kept anonymous. Authors of rejected papers can opt in to the same.
- **Author LLM use**: authors must describe LLM use when it is an important, original, or non-standard part of the method (checklist item 16). Using LLMs only for writing or editing need not be declared. Authors are responsible for all content, and hallucinated citations violate the Code of Conduct.
