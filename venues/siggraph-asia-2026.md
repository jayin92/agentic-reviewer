---
venue: SIGGRAPH Asia
year: 2026
full_name: ACM SIGGRAPH Conference and Exhibition on Computer Graphics and Interactive Techniques in Asia (SIGGRAPH Asia 2026, Kuala Lumpur, 1-4 December 2026), Technical Papers program (Journal track = ACM Transactions on Graphics; Conference track = SIGGRAPH Asia 2026 Conference Papers Proceedings)
source_urls:
  - https://asia.siggraph.org/2026/submissions/technical-papers/ethics-of-review-and-review-instructions/
  - https://asia.siggraph.org/2026/submissions/technical-papers/ (Call for Submissions, Submission Policy, Review Process, FAQ, Timeline)
  - https://asia.siggraph.org/2026/submissions/technical-papers/anonymity-policy/
  - https://asia.siggraph.org/2025/submissions/technical-papers/ethics-of-review-and-review-instructions/ (source of the "Review Scores" text, which is missing from the 2026 page; see note)
  - https://s2026.siggraph.org/technical-papers-reviewer-instructions-ethics/ (SIGGRAPH 2026 North America; same "Review Scores" text)
  - https://sa2022.siggraph.org/en/submissions/technical-papers/review-form/index.html (most recent publicly posted SIGGRAPH Asia review form; the 2023-2026 forms are only visible inside Linklings)
fetched: 2026-09-26
verified_by_human: false   # set to true after you check this file against the sources
---

# SIGGRAPH Asia 2026 reviewer profile

Timeline (Technical Papers CFP): abstract deadline Tue 5 May 2026; full submission (paper) deadline Tue 12 May 2026; upload deadline Wed 13 May 2026 (all 23:59 AoE). Reviews due Thu 25 June 2026; reviews visible to authors and rebuttal opens Mon 29 June; rebuttals due Fri 3 July; committee meeting 17-18 July; decisions Sun 19 July 2026. Review system: Linklings.

Process: each paper gets a primary and a secondary senior reviewer (committee members) and three or more tertiary reviewers. The secondary and tertiaries write full reviews (at least four per paper); the primary moderates the discussion. The preliminary recommendation is "conditionally accepted", "rejected", or "tabled" for the committee meeting. Outcomes: conditionally accepted Journal Paper, conditionally accepted Conference Paper, or rejected. No quota; the historic acceptance rate is about 20-30%.

## What reviewers are asked to evaluate
- The main question is whether the paper's overall contribution (its advance over the state of the art) merits acceptance to the Technical Papers program. All submissions, dual-track and journal-only, use one scale. Recommended order: first decide whether the paper merits acceptance at all. If the answer is yes, weakly or strongly, then judge its completeness and comprehensiveness to decide the track.
- Journal track (TOG): "original, well-validated, and comprehensively described research", meeting the ACM TOG criteria of excellence. Conference track: original research, but "the evidence supporting these advances (examples, experimental studies, comparisons, proofs, etc.) might not be as comprehensive". For the Conference track, reviewers should be open to new problems, to novel solutions likely to improve on the state of the art, and to work that opens new research directions, "even if the proposed work is not fully validated, lacks comprehensive ablations or analysis, and is only partially compared against alternative options." Journal-only submissions must meet the Journal criteria. The paper under review here is a dual-track submission (7-page format), so either track is possible.
- "An important factor in evaluating a paper is the degree to which it will inspire follow-on research" (Tony DeRose). Be fair, promote a broad range of substantial contributions, and look for what is good or stimulating about the paper.
- Keep an open mind for less common contribution types: systems papers (new integration of existing techniques), experimental studies (perceptual studies, measurements), new datasets and benchmarks, and analysis of existing techniques that will inspire follow-on research.
- Each accepted paper must be technically sound and make a substantial contribution. Minor flaws can be corrected and are not a reason to reject.
- Be specific. Related-work criticism must cite specific publications or public disclosures. "This is well known" or "common practice in industry" is "not sufficient nor acceptable". If no such source can be found, "entertain the possibility that the contribution is indeed novel."
- The explanation section is "one of the most important parts of your review". The discussion can matter more than the score. Reviews go back to the authors, so include specific feedback on how to improve the paper.
- Explain what you see as the paper's strengths and weaknesses and how you weigh them against each other.
- The SA2022 form (the last public one) also asks the reviewer to assess clarity of exposition, quality of references (and list missing ones), and reproducibility: whether the work could be reproduced from the paper, whether important algorithmic and system details are covered, and whether limitations and drawbacks are clear.
- Reviewers commit to reviewing all materials in approved formats (PDF, MP4 video, PNG/JPG images). Only the paper and the main accompanying video are mandatory. Other supplementary material is optional, viewed "only at the discretion of the reviewers".

## What reviewers are told NOT to do
- Do not reject for minor, correctable flaws.
- Do not require experimental comparisons unless the code or data is publicly available. When requesting a comparison, give public links to the code or data. If none exists, do not expect the authors to reimplement it (except for a minor change to a method with available code); limit the request to a discussion.
- Do not request comparisons to approaches that are non-trivial to implement or only hypothetical, or to adaptations of algorithms for related but distinct problems. A preferred alternative approach "might be a reason to write a follow-up paper on this new approach, not reject the one under review."
- Do not require comparisons that need non-standard resources (industrial-scale GPU clusters, unique measurement devices, high-end multimaterial 3D printers) unless the paper itself already uses them. Weigh expensive comparisons (perceptual experiments, substantial adaptation) against how likely they are to change the evaluation.
- Not everything needs an end-to-end application or a user study. Different contribution types need different validation.
- Do not let non-peer-reviewed material (arXiv and similar) that the authors missed count against the paper. Do not demand detailed comparisons to peer-reviewed papers published up to 4 weeks before the deadline.
- Do not say "this is well known" without citations.
- Do not try to discover author identities. Originality concerns go to the Technical Papers admin before the review is submitted.
- Do not expect new results or additional experiments in the rebuttal (SA2022 form: "authors should not be expected to produce new results or conduct additional experiments during the rebuttal period"). The 2026 FAQ allows text-only results that directly answer reviewer questions.
- Do not penalize submissions that lack code or data (FAQ: "The reviewers will be instructed not to penalize submissions without code and data"). The paper should still give enough information to recreate them.
- No belittling or sarcastic comments and no remarks on authors' personalities. Evaluate the work, not the authors. No casual or flippant reviews.
- Do not use LLMs to write reviews (see policy below). Do not share papers or videos with non-reviewers. Do not use ideas from reviewed papers.
- Requesting citations mainly to one's own work may break anonymity, so consider it carefully.

## Concurrent-work policy
- Non-peer-reviewed prepublications (arXiv, technical reports, theses): "The existence of these non-peer-reviewed materials should not negatively affect your review of the submission." Authors are "allowed, but not required, to cite them as concurrent work without the burden of having to detail how their work compares or differs." If such preprints are not cited, authors of conditionally accepted papers can be asked to cite them in the final revision. (CFP: authors are not required to discuss or compare with recent prepublications, but must cite those that inspired them.)
- Recent peer-reviewed publications: "authors should not be expected to include detailed comparisons to papers published up to 4 weeks before the SIGGRAPH Asia deadline in their submissions." These do count as prior work, and authors can be required to cite and discuss them in the final paper. The full-submission deadline was 12 May 2026, so papers published on or after about 14 April 2026 are exempt from detailed comparison.
- "SIGGRAPH 2026 papers are not published prior to the SIGGRAPH Asia 2026 deadline and are not considered prior work."
- Authors list their own publicly available, largely overlapping prepublications only in a "Prepublication" form field that reviewers cannot see, not in the paper.

## Review form
The official 2026 form is only visible inside Linklings. The 2026 CFP points to "the Review Form and Reviewer Instructions for the questions in the form", but no 2023-2026 review-form page is public (the review-form URLs for 2023-2026 return 404). The fields and order below come from the SIGGRAPH Asia 2022 public review form, which is the most recent one published. The 2026 guidelines confirm a single six-level score with the same labels, an "explanation section", and a "Private Comments" section. Whether the 2026 form is otherwise identical is unconfirmed. The 2024-2026 guidelines also say reviewers "may recommend whether to accept the paper for the Journal or Conference track" on dual-track submissions, which implies a track-recommendation input. Its label, options and position are unconfirmed.

| # | Field | Type | Scale / options | Instructions to reviewers |
|---|-------|------|-----------------|---------------------------|
| 1 | Description | text | – | "Briefly describe the paper and give your assessment of the scope and magnitude of it's contribution." |
| 2 | Clarity of Exposition | text | – | "Are the exposition and presentation clear? How could they be improved? Please be tolerant of papers that do not conform to the usual paper template." |
| 3 | Quality of References | text | – | "Are the references adequate? List any additional references that are needed." |
| 4 | Reproducibility | text | – | "Could the work be reproduced from the information in the paper? Are all important algorithmic or system details discussed adequately? Are the limitations and drawbacks of the work clear?" |
| 5 | Recommendation (under "Scored Review Questions") | score | 6 levels: Strong reject / Reject / Borderline reject / Borderline accept / Accept / Strong accept | "Please enter your recommendation, basing your rating on the paper as it was submitted." Guidelines: the same scale for Journal and dual-track papers; "The contribution of the paper is evaluated as a whole, including all aspects of the paper." |
| 6 | Final recommendation (post-rebuttal) | choice | Reject / Table / Accept / Accept – top 10% of papers | "Please enter your final recommendation for the paper, considering the authors' rebuttal and the reviewer discussion. Please mark "Table" if you believe that the reviewer discussion did not reach consensus, and more input / discussion is required for this submission." (SA2022; presence in 2026 unconfirmed) |
| 7 | Explanation of Rating | text | – | "Explain your rating by discussing the strengths and weaknesses of the submission, contributions, and the potential impact of the paper. Include suggestions for improvement and publication alternatives, if appropriate. Be thorough. Be fair. Be courteous. Provide evidence and references for your statements. Above all, be constructive. If the paper is a resubmission with reviewer continuity, please also give your assessment of how well the authors took into account comments from reviewers in the previous review cycle, and improved their work. ... Your evaluation will be forwarded to the authors during the rebuttal period. Please be judicious in asking questions to be answered during rebuttal – authors should not be expected to produce new results or conduct additional experiments during the rebuttal period." |
| 8 | Private Comments | text | – | "You may enter private comments for the papers committee here. These comments will not be sent to the paper author(s). Please do not mention any names or any other papers that are currently in review. You may use this field to comment on your reviewer expertise and confidence in evaluation." (The 2026 FAQ confirms a "Private Comments" section "only seen by the committee members"; it is also where you name a student or colleague who helped with the review.) |
| 9 | Track recommendation (dual-track submissions only) | choice | unconfirmed (presumably Journal / Conference) | Guidelines: "For dual-track submissions, the reviewer may recommend whether to accept the paper for the Journal or Conference track. The final recommendation ... is made by the Technical Papers committee." Label, options, whether it is a separate field, and its position are all unconfirmed. It may be expressed only in the Explanation. |

Not in the SA2022 form: there is no separate numeric expertise or confidence field (expertise and confidence go in Private Comments). Whether 2026 added one is unconfirmed.

## Score meanings
- Recommendation (SA2022 form labels; the 2024, 2025 and SIGGRAPH 2026 guidelines confirm the six level names):
  - Strong reject: "I would argue strongly against this paper"
  - Reject: "I recommend rejection"
  - Borderline reject: "I am not sure, but leaning negative"
  - Borderline accept: "I am not sure, but leaning positive"
  - Accept: "I recommend acceptance, possibly despite minor concerns"
  - Strong accept: "I would argue strongly for this paper"
- Final recommendation (SA2022): Reject; Table (discussion did not reach consensus; more input or discussion needed); Accept; Accept – top 10% of papers.
- Track guidance: "As the requirements for Journal papers are a superset of the requirements for conference papers, uniformly strong scores for a dual-track submission are an indication that the submission should be accepted as a Journal paper" (SA2025/SIGGRAPH 2026 add: "with Conference track more suitable for papers that may have a greater variation of scores").
- Note: the "Review Scores" section of the 2026 SIGGRAPH Asia reviewer page repeats the "Be Specific" paragraph by mistake and never states the scale. The scale above is taken from SA2025, SA2024 and SIGGRAPH 2026 (North America), which all give the same six labels. For SA2026 itself, the six-level scale is unconfirmed but very likely.

## Other policies relevant to feedback
- **LLM policy for reviewers** (SA2026 reviewer page): "Large language models (LLMs) are NOT allowed to be used for writing the reviews nor the meta-reviews/summaries at any step. This is true for any LLM, whether you run it locally or use an API." Reviewers may not ask an LLM to write content, may not share substantial content from the paper or review with an LLM (not even for translation), and may use an LLM only for background research or to check short phrases. LLM-based grammar checkers are allowed. Any AI-drafted text is therefore input to the human reviewer, who must write the submitted review in their own words and base it on their own judgment.
- **Author GenAI / prompt-injection policy**: authors must disclose any Generative AI use beyond grammar correction (ACM Authorship Policy). "Papers containing citations of non-existent material or obvious factual inaccuracies will be rejected when found." "The injection of hidden text/prompts to influence reviewers/automated tools is strictly prohibited and may lead to rejection without review." Reviewers should report any such injection or any fictitious references they find.
- **Supplementary material**: two parts. (A) Anonymous material to be published if the paper is accepted (videos, code, result images, user-study details, appendices; 500MB limit). (B) Anonymous review-only material (the authors' related papers under review, cover letters, resubmission cover letter). Reviewers must read the paper and watch the main video; everything else is at their discretion. Dual-track papers cannot include appendices in the main PDF, so appendices live in the supplement. Video: at most 5 minutes.
- **Page limits**: dual-track papers at most 7 pages excluding references, plus up to two figures-only pages after the references (figures and captions only, no tables). Unlimited references. Journal-only papers have no page limit. acmtog double-column format.
- **Code/data**: encouraged, not required, and reviewers must not penalize papers without it. Promised code or data must be released (deadline 2 Nov 2026). The paper should give enough detail to recreate them. URLs can generally be ignored. An anonymized code/data repository with a verifiable pre-deadline timestamp is allowed if necessary.
- **Rebuttal**: at most 1,000 words, plain text, self-contained, no URLs, images or video. It is for correcting factual errors and answering specific reviewer questions. New text-only results that directly answer a reviewer question are allowed (e.g., a runtime or a PSNR value). Unrelated new results are ignored. Authors can commit to adding results in the final revision. Questions for the rebuttal should therefore be answerable in text.
- **Resubmissions with reviewer continuity**: if the authors opted in, reviewers see the prior reviews, and the Explanation should assess how well the previous comments were addressed (a cover letter is in supplementary part B).
- **Anonymity**: double-blind. Reviewers must report policy violations or anonymity breaches that identify the authors. Authors cite their own published work in the third person.
- **Ethics**: authors follow the ACM Code of Ethics and the ACM policy on research with human participants. The committee judges technical merit and novelty only. Ethically problematic accepted papers are forwarded to an ACM ethics body.
- **Limitations**: the SA2022 Reproducibility field asks whether "the limitations and drawbacks of the work [are] clear". No separate limitations-section requirement or reproducibility checklist is specified for 2026.
- **Confidentiality / conflicts**: do not show the paper to others except someone helping with the review (name them in Private Comments). Recuse yourself for same institution, collaboration in the past 3 years, lifetime advisor/advisee, or scooping risk. Notes may be kept for possible reviewer-continuity resubmissions, but must be kept strictly separate from your own research.
- **Tone**: serious, constructive, thorough, respectful; evaluate the work, not the authors.
