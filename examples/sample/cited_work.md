# Cited work: SparseSplat: Adaptive Gaussian Pruning for Real-Time Novel View Synthesis

## [14] [LightGaussian: Unbounded 3D Gaussian Compression with 15x Reduction and 200+ FPS](https://arxiv.org/abs/2311.17245) (2023)
Role: compared method · verified · core (read in full)

Prunes Gaussians by a global significance score, distills spherical harmonics and applies vector quantization, reaching 15x compression and more than 200 FPS.

- Citation accuracy: **misrepresented**: Submission §2: "heuristic, not learned". [14] §3.2 fine-tunes the score jointly during training.
- Baseline numbers: **not applicable**: Not in the results tables.
- Novelty overlap: **substantial**: Overlaps C1.

## [9] [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/abs/2308.04079) (2023)
Role: baseline · verified · core (read in full)

Introduces 3D Gaussian Splatting: anisotropic 3D Gaussians optimized with adaptive density control and a tile-based differentiable rasterizer, reaching real-time rendering at state-of-the-art quality. Reports 27.45 PSNR on Mip-NeRF 360.

- Citation accuracy: **accurate**: Described correctly in §2.
- Baseline numbers: **mismatch**: Submission Table 1: 27.21. Original Table 1: 27.45, same split and iteration count.
- Novelty overlap: **none**: Base method.

## [22] Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields (2022)
Role: dataset benchmark · verified · abstract-level check

## [31] Fast Splat Rendering on Mobile Devices (technical report) (2024)
Role: background · could not verify · abstract-level check
