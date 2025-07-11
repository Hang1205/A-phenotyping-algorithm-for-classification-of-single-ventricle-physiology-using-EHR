# A-phenotype-algorithm-for-SVP-classification-using-electronic-health-records
<p align="center">
	<img src="figs/overview.png"/> <br />
	<em>
	Figure 1. Overview of the Pipeline
	</em>
</p>

## Instructions:
This repository contains the implementation of a phenotype algorithm for the classification of Single Ventricle Physiology (SVP) using Electronic Health Records (EHR). The algorithm employs a phenotype algorithm to analyze clinical data and identify patterns related to SVP, providing valuable insights for medical professionals and researchers.  We are currently optimizing the script to enhance its usability and performance.

## Overview:
Single Ventricle Physiology (SVP) is a complex congenital heart condition, and accurate classification of patients is crucial for diagnosis and treatment planning. This project aims to develop and validate a phenotype classification algorithm based on EHR data. The dataset used for testing includes patients who underwent ferumoxytol-enhanced MRI scans, with the results tested on additional congenital heart disease (CHD) datasets to ensure robustness.

## Features:
Dataset Integration: The method has been applied to a dataset of 1,020 patients and validated on a separate dataset of 2,500 CHD patients.

Cohort discovery: The algorithm categorizes patients with SVP, helping cohort discovery more effectively.

Generalization: The model can be adapted to new CHD datasets, offering flexibility for broader applications.

## Getting Started
Prerequisites:
Ensure you have the following installed:
- Python (>=3.7)

Libraries: 
- pandas.

## Dataset
The dataset for this project includes EHR data related to SVP classification. The data includes both structured(ICD codes, imaging) and unstructured information (imaging impressions, imaging narratives and provider notes).

Due to privacy restrictions, access to the dataset is not possible. However, I can guide you on how to request the necessary documents and outline the steps involved in processing the data.

## Running Experiments
```bash
python main.py --data_dir Data --save_dir Save
```
Output Structure...

## License

This project is licensed under the TDG-Attribution-NonCommercial-ShareAlike Academic Software License. See the [LICENSE](LICENSE) file for full details.

## Acknowledgments
The development of this algorithm was supported by UCLA Cardiovascular Imaging Research Lab https://cvirl.dgsom.ucla.edu/.
Special thanks to the contributors who helped shape the project.

## Citation
```bibtex
@article{xu2025phenotyping,
  title={A phenotyping algorithm for classification of single ventricle physiology using electronic health records},
  author={Xu, Hang and Renella, Pierangelo and Badiyan, Ramin and Hindosh, Ziad R and Elisarraras, Francisco X and Zhu, Bing and Satou, Gary M and Husain, Majid and Finn, J Paul and Hsu, William and others},
  journal={JAMIA open},
  volume={8},
  number={3},
  pages={ooaf035},
  year={2025},
  publisher={Oxford University Press}
}
```
