#Deep Learning with Transfer Learning Overcomes Data Scarcity in Drug–Target Interaction Prediction for One-Carbon Metabolism Enzymes

**Alperen Dalkiran<sup>2</sup>, Kun Woo D. Shin<sup>1</sup>, M. Volkan Atalay<sup>3</sup>, Angelo Y. Meliton<sup>1</sup>, Yufeng Tian<sup>1</sup>, Takugo Cho<sup>1</sup>, Parker S. Woods<sup>1</sup>, Obada R. Shamaa<sup>1</sup>, Robert B. Hamanaka<sup>1</sup>, Rengül Cetin-Atalay<sup>1</sup>, and Gökhan M. Mutlu<sup>1</sup>**

<sup>1</sup> Department of Medicine, Section of Pulmonary and Critical Care Medicine, The University of Chicago, Chicago, IL, USA
<sup>2</sup> School of Informatics, University of Edinburgh, Edinburgh, UK
<sup>3</sup> Department of Information Systems and Supply Chain Management, Loyola University Chicago, Chicago, IL, USA

---

## Abstract

Predicting drug–target interactions (DTIs) with deep learning offers exciting opportunities to accelerate drug discovery, yet performance is often constrained by the scarcity of target-specific training data. This is a particular challenge for mitochondrial one-carbon (1C) pathway enzymes, which are attractive therapeutic targets but remain pharmacologically understudied.

Mitochondrial 1C metabolism supplies glycine, reducing equivalents, and 1C units critical for nucleotide synthesis, and has emerged as a key pathway in the pathogenesis of cancer and fibrosis. Two key 1C enzymes, **SHMT2** and **MTHFD2**, support collagen production in fibroblasts; blocking either enzyme prevents glycine and collagen increases after stimulation with the profibrotic cytokine TGFβ.

Here, we developed deep learning models leveraging **transfer learning** to predict interactions between approved drugs and SHMT2 or MTHFD2, despite minimal target-specific training data. Models were first pre-trained on large datasets from related enzyme families and subsequently fine-tuned to these specific targets. Virtual screening of the DrugBank approved drug library identified six candidates, three of which — **Carbimazole**, **Crizotinib**, and **GSK-2018682** — dose-dependently reduced TGF-β–induced collagen production and glycine accumulation in human lung fibroblasts. This work demonstrates how transfer learning–based methods can facilitate the identification of repurposable drugs targeting metabolic pathways with limited DTI data.

---

## Validated Drug Candidates

| Drug | DrugBank ID | Predicted Target | Inhibits Collagen & Glycine |
|------|-------------|------------------|-----------------------------|
| Carbimazole | DB00389 | MTHFD2 | **Yes** |
| Crizotinib | DB08865 | SHMT2 | **Yes** |
| GSK-2018682 | DB11987 | SHMT2 | **Yes** |
| Leucovorin | DB00650 | MTHFD2 | No |
| Flavoxate | DB01148 | MTHFD2 | No |
| Trametinib | DB08911 | MTHFD2 | No |

---

## Site Contents

| Page | Description |
|------|-------------|
| [Data](data.md) | DTI datasets organized by Table 1 (MTHFD2) and Table 2 (SHMT2), with download links |
| [Code](code.md) | Scripts, dependencies, and step-by-step commands to run all scripts |

---

## Manuscript

*(Link to published paper will be added upon acceptance.)*

---


