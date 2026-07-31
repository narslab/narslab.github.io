---
layout: paper
title: "A Functional Bus Stop Typology: Explainable Machine Learning on Transit Data to Inform Policymaking"
image: /images/papers/2026-05-03-azhdari-functional-bus-stop.png
authors: Mahdi Azhdari, Jimi Oke, Eric J. Gonzales
year: 2026
ref: Azhdari et al. 2026. Data Science for Transportation
journal: "Data Science for Transportation 8(2):13."
volume: 8
pdf: /pdfs/papers/2026-azhdari-functional-bus-stop.pdf
supplement:
doi: 10.1007/s42421-026-00155-7
github:
---

# Abstract

Bus stops are critical elements of transit networks, shaping accessibility, reliability, and multimodal connectivity. While they simultaneously play different functional roles and are tightly connected within the wider system, there is a need for analyses that capture their functional relationships and roles in an integrated way. This paper develops a data-driven bus stop typology that combines operational performance, ridership and fare behavior, and multimodal context, and shows how it can support targeted, policy-relevant interventions. Using the Massachusetts Bay Transportation Authority (MBTA) bus network as a case study, we use Automated Fare Collection (AFC), Automated Passenger Counter (APC), and GIS data into a stop-level feature space that captures the diverse functional patterns of bus stops across operations, demand, and multimodal context. We apply a Gaussian Mixture Model (GMM) to standardized indicators to uncover four distinct stop types. To interpret and validate these roles, we use one-vs-rest Random Forest classifiers with SHAP explanations and a multiclass XGBoost model, which achieves high out-of-sample accuracy and near-perfect ROC–AUC, indicating that the clusters are robust and recoverable from their underlying indicators. The resulting typology distinguishes multi-route destinations, rail-adjacent distributors, high-demand hubs, and low-ridership locals, each with characteristic operational and spatial signatures. We then translate these types into actionable policy implications, providing a transferable framework to support evidence-based decisions and investment prioritization in bus stop planning and management.
