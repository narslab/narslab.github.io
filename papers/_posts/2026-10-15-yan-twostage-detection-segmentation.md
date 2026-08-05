---
layout: paper
title: "A two-stage detection and segmentation framework for pedestrian crosswalk inventory and condition assessment from aerial imagery"
image: /images/papers/2026-10-15-yan-twostage-detection-segmentation.png
authors: Xintong Yan, Zubin Bhuyan, Jimi Oke, Guanhe Wu, Yuanchang Xie
year: 2026
ref: Yan et al. 2026. Engineering Applications of Artificial Intelligence
journal: "Engineering Applications of Artificial Intelligence 182:115851."
volume: 182
pdf:
supplement:
doi: 10.1016/j.engappai.2026.115851
github:
---

# Abstract

Accurate crosswalk inventories are critical for supporting pedestrian and wheelchair-user safety and accessibility. Inclusion of detailed pavement marking data further enhances crosswalk condition assessment, lifecycle planning, and data-driven asset management. This study introduces a unified deep-learning-based artificial intelligence framework for large-scale crosswalk localization and condition assessment using high-resolution aerial imagery. The framework employs an innovative two-stage approach. The first stage is an oriented bounding box (OBB) module, which is an anchor-free detector designed to localize crosswalks at arbitrary orientations, providing highly accurate spatial positioning. This is followed by a segmentation stage, which incorporates a novel multi-scale attention (MSA) module. The MSA module is crucial for extracting pixel-level details of pavement markings, which are essential for subsequent crosswalk condition analysis. The outputs from both stages are then fed into a condition-assessment pipeline to calculate a normalized condition ratio. This ratio effectively quantifies crosswalk pavement marking degradation, offering a standardized metric across diverse crosswalk types. The efficacy of the proposed two-stage approach is rigorously validated on extensive and diverse datasets sourced from Massachusetts, Florida, and Washington. Performance metrics demonstrate superior capabilities of the proposed framework: the OBB detector achieved a mean average precision of 0.893 across intersection over union (IoU) thresholds from 0.50 to 0.95, and the segmentation model attained a mean intersection over union (mIoU) of 0.925. These results consistently outperform existing state-of-the-art baselines. Ultimately, the proposed framework successfully generates accurate, geographic information system (GIS)-ready vector crosswalk inventories, establishing a highly scalable and automated solution for advanced transportation infrastructure monitoring and proactive maintenance planning.
