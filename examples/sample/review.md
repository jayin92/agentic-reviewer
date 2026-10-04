# Review: SparseSplat: Adaptive Gaussian Pruning for Real-Time Novel View Synthesis

Venue: CVPR 2026
Generated 2026-09-26 by EXAMPLE OUTPUT for a fictional paper, made to show the format. Not a real review.

## Overview
A solid efficiency paper whose main speed claim holds, but the novelty of the pruning score is overstated.
C1 closely matches LightGaussian's global significance score; the paper cites LightGaussian but describes it as "heuristic, not learned", which the fact-check found inaccurate.
The 3DGS baseline PSNR in Table 1 (27.21) is lower than the original paper's 27.45 on the same split.
Two strong 2025 pruning methods are not cited or compared.
Fixing the baseline numbers and adding one ablation on the regularizer would address most major concerns.

## Summary
The paper proposes SparseSplat, which learns a per-Gaussian importance score during 3D Gaussian Splatting training and prunes low-importance Gaussians, combined with a view-dependent opacity regularizer. On Mip-NeRF 360, Tanks and Temples and Deep Blending it reports 3.1x faster rendering and 58% fewer Gaussians at comparable PSNR.

## Strengths
- Clear and practically relevant goal: real-time rendering on consumer GPUs. (§1)
- Speed measurements are thorough, reported on three GPUs with warm-up and variance. (Table 3)
- Code and training configs are promised and hyperparameters are fully listed. (Appendix B)

## Major weaknesses
### W1. The learned importance score (C1) is close to LightGaussian's significance score
*novelty · §3.1, §2 · raised by novelty, theorist*

LightGaussian [14] computes a global significance from hit count × opacity × volume, and its §3.2 also fine-tunes the score jointly with training. The claimed difference, that SparseSplat's score is learned, amounts to one extra MLP head. §2 describes [14] as a "heuristic, not learned" method, which understates the overlap.

**How to fix:** Reposition C1 as an extension of [14]. Add a direct comparison with [14] at matched Gaussian counts, and an ablation that replaces your score with [14]'s score inside your pipeline.

### W2. 3DGS baseline PSNR is lower than the original paper reports
*experiments · Table 1 · raised by empiricist*

Table 1 lists 3DGS at 27.21 PSNR on Mip-NeRF 360. The original 3DGS paper reports 27.45 (its Table 1, same 7-scene split, 30k iterations). Most of the reported +0.18 dB gain of SparseSplat would disappear against the original number.

**How to fix:** Use the published 27.45 or explain the re-run setting (resolution, iterations, seed). Report mean ± std over 3 seeds for both methods.

### W3. No ablation isolating the opacity regularizer (C2) *(partially valid)*
*experiments · Table 4 · raised by empiricist, theorist*

Table 4 ablates pruning thresholds but always keeps the regularizer on, so its contribution to quality and speed cannot be separated.

**How to fix:** Add rows with the regularizer removed and with it added to vanilla 3DGS.

## Minor issues
### W4. Missing comparison to two 2025 pruning methods
*related work · §5 · raised by novelty*

[U1] and [U2] report higher compression at equal PSNR on the same benchmarks and were public well before the deadline.

**How to fix:** Cite both and add them to Table 1, or explain why they are not comparable.

### W5. Fig. 4 y-axis starts at 26.5 dB
*figures · Fig. 4 · raised by figures*

The truncated axis makes a 0.2 dB gap look like a large margin.

**How to fix:** Start the axis at a round value or add a note that it is truncated.

## Novelty
| Contribution | Verdict | Closest prior work | Evidence |
|---|---|---|---|
| C1: learned importance score for pruning | can refute | [14] LightGaussian (cited) | [14] §3.2 fine-tunes its significance score jointly with training, which is the core of C1. |
| C2: view-dependent opacity regularizer | unclear | [U3] (uncited) | [U3] uses a similar view-conditioned opacity penalty for anti-aliasing, not pruning. |
| C3: 3.1x faster rendering at equal PSNR | cannot refute | [U1] (uncited) | No prior work reports this speed at equal quality on these GPUs, though [U1] is close at 2.6x. |

The strongest novelty is the **combination** of pruning with the opacity regularizer and the resulting speed. The importance score on its own is incremental over [LightGaussian](https://arxiv.org/abs/2311.17245).

## Use of cited work
- **baseline numbers** [9] 3D Gaussian Splatting for Real-Time Radiance Field Rendering: Table 1 reports 27.21 PSNR for 3DGS; the original reports 27.45 on the same split.
  - Verification (valid): Both tables use the 7-scene split at 30k iterations; the submission gives no re-run details.
- **citation accuracy** [14] LightGaussian: Described as "heuristic, not learned", but [14] fine-tunes the score during training.
  - Verification (partially valid): The score formula is hand-designed, but it is refined by training (§3.2), so "not learned" is overstated.

## Reference-list problems
- [31] "Fast Splat Rendering on Mobile Devices (technical report)": could not verify; checked Semantic Scholar, OpenAlex, Crossref, DBLP, web search

"Could not verify" is not proof a reference is wrong. Books, theses and reports are often unindexed.

## Missing related work
**Missing baselines**
- [U1] [Example uncited pruning method A](https://arxiv.org/) (2025): Prunes 3DGS with a learned mask and reports 2.6x speed at equal PSNR on the same benchmarks.
- [U2] [Example uncited compression method B](https://arxiv.org/) (2025): Higher compression ratio at similar quality; directly comparable.

**Related techniques**
- [U3] [Example view-conditioned opacity work C](https://arxiv.org/) (2024): Uses a similar view-conditioned opacity penalty, for anti-aliasing instead of pruning.

## Questions for the authors
1. How was the 3DGS baseline in Table 1 trained, and why does it differ from the published 27.45 dB?
2. Does the importance score transfer to a pre-trained 3DGS model without retraining?
3. What is the training-time overhead of the extra MLP head?

## Revision plan
- [ ] **high**: Re-run or correct the 3DGS baseline in Table 1 and report 3 seeds for all methods. (addresses W2)
- [ ] **high**: Rewrite the description of LightGaussian in §2 and reposition C1 as an extension of it. (addresses W1)
- [ ] **high**: Add a regularizer ablation to Table 4. (addresses W3)
- [ ] **medium**: Cite and compare with [U1] and [U2]. (addresses W4)
- [ ] **low**: Redraw Fig. 4 with an untruncated axis. (addresses W5)

## Scores
**CVPR 2026 form (uncalibrated AI estimate):**

| Field | Value |
|---|---|
| Preliminary Recommendation | 3: Borderline |
| Confidence Level | 4: Confident but not absolutely certain |

The full form is in `review_form.txt`.

| Dimension (1-5) | Median |
|---|---|
| Originality of the ideas and approach | 2 |
| Importance of the research question addressed | 3.5 |
| Whether the claims are well supported by evidence | 2.5 |
| Soundness of the experiments | 2.5 |
| Clarity of writing and presentation | 4 |
| Value to the research community | 3 |
| Whether it is contextualized appropriately relative to prior work | 2 |

*AI-generated review. It may contain errors.*

## Appendix A: criticisms removed by fact-checking
- (clarity-impact, §5) The paper does not report memory usage.
  - refuted: Table 3 reports peak VRAM for all methods.
