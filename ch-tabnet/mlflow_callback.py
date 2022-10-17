import torch
import pytorch_tabnet

from pytorch_tabnet.callbacks import Callback

import mlflow

#
# callback for MLflow integration
#
class MLCallback(Callback):
    def on_train_begin(self, logs=None):
        
        mlflow.set_tracking_uri(MLF_TRACK_URI)
        mlflow.set_experiment(MLF_EXP_NAME)
       
        mlflow.start_run(run_name = MLF_RUN_NAME)
        
        mlflow.log_params(params)
        
    def on_train_end(self, logs=None):
        
        mlflow.end_run()
        
    def on_epoch_end(self, epoch, logs=None):
    
        # send to MLFlow
        mlflow.log_metric("train_auc", logs['train_auc'])
        mlflow.log_metric("valid_auc", logs["valid_auc"])
        mlflow.log_metric("loss", logs["loss"])
        