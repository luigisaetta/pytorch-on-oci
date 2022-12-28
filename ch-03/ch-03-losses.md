# Le Loss Function in PyTorch

## Quali sono le Loss Function che tratterò?

Loss Function per problemi di **regressione**:
* Mean Absolute Error Loss
* Mean Squared Error Loss

Si deve aver presente che nei problemi di regressione tipicamente non vi è attivazione sull'ultimo layer (l'output non è vincolato in un range).

Loss Function per problemi di **classificazione**:
* Negative Log-Likelihood Loss
* Cross Entropy Loss

|Tipologia         |Attivazione ultimo layer | Loss                  | Note                                |
|------------------|-------------------------|-----------------------|-------------------------------------|
| regressione      |   Nessuna               | nn.L1Loss   | Mean Absolute Error (MAE) |
| regressione      |   Nessuna               | nn.MSELoss  | Mean Squared Error (MAE)  |
| classificazione  |   Sigmoid               | nn.BCELoss  | Binary Cross Entropy      |
| classificazione  |   Nessuna               | nn.BCEWithLogitsLoss  | Binary Cross Entropy, ultimo layer senza sigmoid,<br>numericamente più stabile|
| classificazione multiclasse | log_softmax | nn.NLLLoss | ... |

## Referenze

[Neptune AI](https://neptune.ai/blog/pytorch-loss-functions)


