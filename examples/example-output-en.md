# Group Meeting Report - Molecular Property Prediction with Graph Neural Networks

Presenter: Zhang
Date: 2026-10-13

## 1. Progress This Week

- Completed the literature review: surveyed 5 representative GNN works (2023–2025) on molecular property prediction; selected **MPNN + attention pooling** as the baseline route.
- Completed the data pipeline: extracted 12,480 compound records from ChEMBL, standardized SMILES, and split 8:1:1 with a fixed seed of 42.
- Implemented the baseline model: a 3-layer message-passing GNN with global attention pooling, end-to-end train/val/test (`train.py`, `model/gnn.py`).
- Ran the first reproducible experiment: 5-fold cross-validation on the ESOL dataset.

## 2. Experiments / Results

**Valid results**
- Baseline reaches RMSE = 0.71 on the test set, better than the random-forest baseline (RMSE = 0.89).
- With lr 1e-3 + AdamW + cosine annealing, training converges stably and validation loss decreases monotonically within 30 epochs.

**Failed attempts (recorded honestly)**
- Adding 2D scaffold features raised validation RMSE to 0.83, likely due to overfitting from feature-dimension blow-up; shelved for now.
- Scaling to 5 message-passing layers caused clear over-smoothing — deep-node representations became almost indistinguishable. Planning to add residual connections to mitigate 【待验证】.

## 3. Current Blockers

- **Data-leakage risk**: the current row-wise random split may place different activity records of the same molecule across sets, making metrics optimistic.
  - Tried: checked duplicate SMILES, found ~3% duplicates; the concrete implementation of scaffold split is not yet decided 【待验证】.
- **GPU memory bottleneck**: OOM when batch size exceeds 64 (RTX 3090, 24GB).
  - Tried: gradient accumulation (effective batch = 128) runs, but training time increases ~40%.

## 4. Next Steps

1. Implement scaffold split and rerun the baseline to confirm whether leakage exists (2–3 days).
2. Add residual connections to the deep GNN to test whether over-smoothing is mitigated (2 days).
3. Add experiments on two public datasets (FreeSolv, Lipophilicity) to test generality (3 days).
4. Prepare figures: RMSE comparison bar chart and training curves, exported as publication-quality vector graphics.

## 5. Questions for Discussion

- How should the gap between scaffold split and random split be presented in the paper for rigor?
- Is it worth introducing 3D conformational features, or should we first solidify the 2D model?
- Besides residual connections, are there more widely accepted solutions to over-smoothing?

## Appendix

- **References**
  - Gilmer et al. (2017) *Neural Message Passing for Quantum Chemistry*
  - Yang et al. (2019) *Analyzing Learned Molecular Representations*
- **Key code changes**
  - `model/gnn.py`: added attention pooling, configurable number of MP layers
  - `data/preprocess.py`: added SMILES standardization and duplicate-molecule flagging
  - `train.py`: wired in gradient accumulation and cosine annealing

## Predicted Advisor Questions

1. Could your data split cause leakage? How much do metrics drop after switching to scaffold split?
2. Is the improvement over random forest statistically significant? Did you run a significance test?
3. Where does your model stand versus the SOTA, and what causes the gap?
4. What is the root cause of over-smoothing — did you verify it's the layer count and not something else?
5. What is your three-week timeline, and which step carries the most risk?
