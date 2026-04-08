# Data

All datasets were constructed from **ChEMBL (V29)** using the IUBMB Enzyme Classification (EC) nomenclature tree. The EC hierarchy is used to define source (pre-training) and target (fine-tuning) datasets for each model. Compound clustering uses RDKit Butina (Tanimoto = 0.8) to maximize chemical diversity.

---

### MTHFD2 data files

| File | Description |
|------|-------------|
| [`MTHFD2_Active_Compounds.txt`](../MTHFD2_Active_Compounds.txt) | ChEMBL IDs of the 29 MTHFD2 active compounds |
| [`MTHFD2_Source_Active_Compounds.txt`](../MTHFD2_Source_Active_Compounds.txt) | ChEMBL IDs of the source family active compounds |
| [`MTHFD2_top_predictions.csv`](../MTHFD2_top_predictions.csv) | DrugBank virtual screening results for the MTHFD2 model (AUPRC scores across Mode 1, Mode 2 Layer 1, Mode 2 Layer 2) |

---

### SHMT2 data files

| File | Description |
|------|-------------|
| [`SHMT2_Active_Compounds.txt`](../SHMT2_Active_Compounds.txt) | ChEMBL IDs of the 6 SHMT1/2 active compounds |
| [`SHMT2_Source_Active_Compounds.txt`](../SHMT2_Source_Active_Compounds.txt) | ChEMBL IDs of the EC 2.1.–.– source family active compounds |
| [`SHMT2_top_predictions.csv`](../SHMT2_top_predictions.csv) | DrugBank virtual screening results for the SHMT2 model (AUPRC scores across Mode 1, Mode 2 Layer 1, Mode 2 Layer 2) |

---

## Virtual Screening Results

### MTHFD2 top-ranked DrugBank compounds

| DrugBank ID | Drug Name | Mode 1 | Mode 2 Layer 1 | Mode 2 Layer 2 | Validated |
|-------------|-----------|-------:|---------------:|---------------:|-----------|
| DB00389 | Carbimazole | 0.920 | 0.799 | 0.887 | **Yes** |
| DB00650 | Leucovorin | 0.983 | 0.865 | 0.962 | No |
| DB06813 | Pralatrexate | 0.973 | 0.956 | 0.950 | — |
| DB11611 | Lifitegrast | 0.968 | 0.910 | 0.943 | — |
| DB11596 | Levoleucovorin | 0.963 | 0.899 | 0.947 | — |
| DB11994 | Diacerein | 0.958 | 0.842 | 0.911 | — |
| DB08911 | Trametinib | 0.950 | 0.926 | 0.932 | No |
| DB00716 | Nedocromil | 0.956 | 0.913 | 0.886 | — |
| DB01148 | Flavoxate | 0.911 | 0.830 | 0.846 | No |
| DB13228 | Flosequinan | 0.896 | 0.858 | 0.905 | — |
| DB00440 | Trimethoprim | 0.873 | 0.830 | 0.899 | — |
| DB00555 | Lamotrigine | 0.864 | 0.975 | 0.832 | — |

### SHMT2 top-ranked DrugBank compounds

| DrugBank ID | Drug Name | Mode 1 | Mode 2 Layer 1 | Mode 2 Layer 2 | Validated |
|-------------|-----------|-------:|---------------:|---------------:|-----------|
| DB01087 | Primaquine | 1.000 | 0.999 | 1.000 | — |
| DB08865 | Crizotinib | 0.992 | 0.998 | 0.995 | **Yes** |
| DB11987 | GSK-2018682 | 0.969 | 0.937 | 0.967 | **Yes** |
| DB11632 | Opicapone | 0.967 | 0.956 | 0.963 | — |
| DB00718 | Adefovir dipivoxil | 0.945 | 0.979 | 0.981 | — |
| DB11718 | Encorafenib | 0.957 | 0.972 | 0.966 | — |
| DB12612 | Ozanimod | 0.759 | 0.738 | 0.754 | — |
| DB01007 | Tioconazole | 0.612 | 0.782 | 0.773 | — |
| DB14989 | Umbralisib | 0.607 | 0.663 | 0.693 | — |

"Validated" = tested in TGF-β–stimulated normal human lung fibroblasts.

---

## Data Availability

Raw ChEMBL data is publicly available at [https://www.ebi.ac.uk/chembl/](https://www.ebi.ac.uk/chembl/) (ChEMBL version 29).

All processed datasets used for model training and evaluation are provided in this repository. See the [Code page](code.md) for instructions on how to use these files with the training scripts.
