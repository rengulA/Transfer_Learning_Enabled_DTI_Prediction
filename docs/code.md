# Code

All scripts used in this study are provided in the root of this repository. The pipeline uses Python with PyTorch for model training and Chemprop for molecular feature encoding.

---

## Repository Structure

```
.
├── mainTraining.py                # Train DFNN — entry point with all CLI arguments
├── feedForwardDNNDTIFiveFold.py   # DFNN training loop (5-fold CV, train/test, transfer learning)
├── models.py                      # FC_2_Layer and FC_3_Layer model definitions
├── data_processing.py             # Dataset classes and data loaders
├── evaluation_metrics.py          # MCC, AUROC, AUPRC, Precision, Recall, F1 computation
│
├── MTHFD2_source_smiles.csv       # Source SMILES for MTHFD2 (EC 1.5.1.- / EC 3.5.4.-)
├── MTHFD2_smiles.csv              # Target SMILES for MTHFD2
├── training_files/MTHFD2_source/  # Source DTI pairs, Chemprop + ECFP4 features, fold indices
├── training_files/MTHFD2/         # Target DTI pairs, Chemprop + ECFP4 features, fold indices
│
├── SHMT2_source_smiles.csv        # Source SMILES for SHMT2 (EC 2.1.-.-)
├── SHMT2_smiles.csv               # Target SMILES for SHMT2
├── training_files/SHMT2_source/   # Source DTI pairs, Chemprop + ECFP4 features, fold indices
├── training_files/SHMT2/          # Target DTI pairs, Chemprop + ECFP4 features, fold indices
│
├── trained_models/MTHFD2_source/  # Trained source model for MTHFD2
└── trained_models/SHMT2_source/   # Trained source model for SHMT2
```

---

## Dependencies

Install the following before running any scripts:

| Package | Version |
|---------|---------|
| Python | 3.x |
| PyTorch | 1.12.1 |
| Pandas | 1.3.5 |
| scikit-learn | 1.1.2 |
| NumPy | 1.22.4 |
| RDKit | 2022.9.1 |



## Train the DFNN Model

`mainTraining.py` is the main entry point. All training configurations are controlled via command-line arguments.

### Key arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--td` | `MTHFD2` | Target dataset directory name |
| `--sd` | `MTHFD2_source` | Source dataset directory name (for transfer learning) |
| `--cf` | `chemprop` | Compound features: `chemprop` (300-dim) or `ecfp4` (1024-dim) |
| `--model` | `fc_2_layer` | Model: `fc_2_layer` (used in this study) or `fc_3_layer` |
| `--chln` | `1200_300` | Hidden layer neuron counts, underscore-separated |
| `--lr` | `0.0001` | Learning rate |
| `--bs` | `256` | Batch size |
| `--epoch` | `100` | Number of training epochs |
| `--do` | `0.1` | Dropout rate |
| `--tlf` | `0` | Transfer learning flag: `0` = scratch, `1` = transfer |
| `--ff` | `0` | Freeze flag: `0` = fine-tune all, `1` = freeze layer(s) |
| `--fl` | `1` | Which hidden layer(s) to freeze: `1`, `2`, or `12` |
| `--sf` | `0` | Subset flag: `0` = use full data, `1` = use random subset |
| `--ss` | `10` | Subset size (number of active+inactive compounds) |
| `--ip` | — | Input path (root directory containing dataset folders) |
| `--op` | — | Output path (for result files) |
| `--nc` | `2` | Number of output classes (2 for binary) |


---

## Running the Scripts

Run the following commands from the repository root directory.

**Stage I — Train source model (from scratch)**
```bash
python mainTraining.py --td MTHFD2_source
```

**Stage I — Train target model (from scratch)**
```bash
python mainTraining.py --td MTHFD2
```

**Stage II — Mode 1: Full fine-tuning**
```bash
python mainTraining.py --td MTHFD2 --sd MTHFD2_source --tlf 1
```

**Stage II — Mode 2: Freeze layer 1**
```bash
python mainTraining.py --td MTHFD2 --sd MTHFD2_source --tlf 1 --ff 1 --fl 1
```

**Stage II — Mode 2: Freeze layer 2**
```bash
python mainTraining.py --td MTHFD2 --sd MTHFD2_source --tlf 1 --ff 1 --fl 2
```

---


