---
layout: paper
title: "A multiscale interpretability framework for identifying actionable road network features to mitigate congestion in highly congested cities"
image: /images/papers/2026-06-26-kumar-multiscale-interpretability-framework.jpg
authors: Nishant Kumar, Yatao Zhang, Nina Wiedemann, Jimi Oke, Martin Raubal
year: 2026
ref: Kumar et al. 2026. Scientific Reports
journal: "Scientific Reports."
volume:
pdf: /pdfs/papers/2026-kumar-multiscale-interpretability-framework.pdf
supplement:
doi: 10.1038/s41598-026-58442-w
github:
---

# Abstract

Transferring congestion mitigation strategies across cities remains challenging due to two compounding issues: road network features affect congestion differently in different cities, and their influence may vary across spatial scales. We propose a multiscale framework to identify “actionable” road network features, defined as those maintaining a consistent directional association with traffic congestion across varying spatial resolutions. Through systematic investigation of seven highly congested cities worldwide, our findings reveal strong city-specific signatures in feature importance, indicating supply-side planning must be tailored individually. However, the most consistently exacerbating features for demand-side consideration show notable similarities across cities. We emphasise that the directional associations identified reflect patterns in the training data and should not be interpreted as causal effects; the identified features are policy-relevant candidates subject to validation through counterfactual modelling. Feature attribution is model-dependent: results are derived from RF-based TreeSHAP and should be interpreted accordingly. In the short term, our results directly inform ongoing measures like congestion pricing and personalised route choice applications, making them more robust and publicly acceptable. Long-term, our insights encourage re-evaluating scepticism toward infrastructure planning and highlight opportunities for designing congestion-resistant future cities. Given the diverse city selection, common observations identified can likely be extrapolated to new cities when detailed analysis is constrained by data limitations. We provide key recommendations for researchers. First, data-driven congestion studies must explicitly interrogate microscopic spatial scales, because coarse-scale models can conceal scale-dependent reversals in feature influence that directly undermine policy robustness. Second, simulation-based counterfactual approaches should test road network features beyond known value ranges.
