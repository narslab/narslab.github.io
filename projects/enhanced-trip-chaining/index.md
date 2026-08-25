---
layout: project
title: enhanced-trip-chaining/
project: enhanced-trip-chaining
repo: narslab/enhanced-trip-chaining
permalink: /:path/:basename:output_ext
---

# Enhanced Trip Chaining for Public Transit

This repository contains the Python code associated with the research paper titled "Enhanced Seasonal Typology-Informed Transit Trip Chaining via Mobile Boarding and Survey Data". The research focuses on developing an innovative trip-chaining framework for public transit systems, particularly those lacking advanced data collection capabilities. The framework leverages mobile ticketing data, typology analysis, and machine learning techniques to enhance the accuracy of trip inference.

## Key Features

* **Trip Chaining Framework**: The core of the repository is a Python-based trip-chaining framework that infers complete passenger trips from mobile ticketing data, including boarding, alighting, and transfer points.
* **Typology Analysis**: The framework incorporates passenger typology analysis to identify distinct travel behavior patterns, enabling the model to adapt to diverse passenger needs.
* **Seasonality Integration**: The model accounts for seasonal variations in travel behavior, ensuring accurate predictions throughout the year.
* **Spatial Error Correction**: A gradient boosting machine is used to learn and correct spatial errors in trip chaining predictions, further enhancing accuracy.

## Data Requirements

The code in this repository requires the following data:

* **Mobile Ticketing Data**: 
    * This dataset should include passenger identification numbers (IDs), timestamps, and GPS locations at ticket activation.
    * The data should cover a sufficient period to capture seasonal variations in travel behavior.
* **Survey Data (Optional)**:
    * This dataset can be used to calibrate and validate the trip-chaining model.
    * It should include passenger start and end locations, routes used, and transfer information.
* **General Transit Feed Specification (GTFS) Data**:
    * This dataset provides information about the transit network, including routes, stops, and schedules.
    * It is essential for aligning mobile ticketing data with the transit network and inferring trip details.

**Note:** Due to privacy concerns, the original data used in the research cannot be provided. However, the code is designed to be adaptable to similar datasets from other transit systems.

## Repository Structure

* **src/**: Houses the Python code implementing the trip-chaining framework, typology analysis, spatial error correction, and other relevant algorithms.
* **models/**: Stores trained machine learning models or instructions on how to train them.
* **README.md**: This file, providing an overview of the repository and instructions on how to use the code.

## Getting Started

1. Clone the repository: `git clone https://github.com/<your-username>/<repository-name>.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Prepare your data: Obtain and preprocess your mobile ticketing, survey (if available), and GTFS data according to the requirements specified above.
4. Adapt the code: Modify the code in `src/` to accommodate your specific data structure and any necessary customizations.
5. Run the trip-chaining framework: Execute the main Python script in `src/` to perform trip chaining, typology analysis, and spatial error correction on your data.

## Contributing

Contributions to this repository are welcome! If you have any suggestions, bug fixes, or new features, please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Citation

If you use this code or data in your research, please cite the following paper:

> Abdalazeem, M., & Oke, J. (2023). Enhanced seasonal typology-informed transit trip chaining via mobile boarding and survey data. *Data Science for Transportation*, 5. https://doi.org/10.1007/s42421-023-00082-x

## Contact

For any questions or inquiries, please contact the authors:

* Mohammed Abdalazeem: mamohammed@umass.edu
* Jimi Oke: jboke@umass.edu
