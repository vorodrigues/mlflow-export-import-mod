# Databricks notebook source
# MAGIC %md # Export Run
# MAGIC 
# MAGIC ##### Overview
# MAGIC * Exports an run and its artifacts to a folder.
# MAGIC * Output file `run.json` contains top-level run metadata.
# MAGIC * Notebooks are also exported in several formats.
# MAGIC 
# MAGIC #### Output folder
# MAGIC ```
# MAGIC 
# MAGIC +-artifacts/
# MAGIC | +-plot.png
# MAGIC | +-sklearn-model/
# MAGIC | | +-model.pkl
# MAGIC | | +-conda.yaml
# MAGIC | |
# MAGIC +-run.json
# MAGIC ```
# MAGIC 
# MAGIC ##### Widgets
# MAGIC * Run ID 
# MAGIC * Output base directory - Base output folder of the exported run.
# MAGIC * Export source tags - Log source metadata such as:
# MAGIC   * mlflow_export_import.info.experiment_id
# MAGIC   * mlflow_export_import.metadata.experiment-name	
# MAGIC * Notebook formats:
# MAGIC   * Standard Databricks notebook formats such as SOURCE, HTML, JUPYTER, DBC. See [Databricks Export Format](https://docs.databricks.com/dev-tools/api/latest/workspace.html#notebookexportformat)  documentation.
# MAGIC   
# MAGIC #### Setup
# MAGIC * See Setup in [README]($./_README).

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

# MAGIC %md ### Setup

# COMMAND ----------

dbutils.widgets.text("1. Run ID", "") 
run_id = dbutils.widgets.get("1. Run ID")

dbutils.widgets.text("2. Output base directory", "") 
output_dir = dbutils.widgets.get("2. Output base directory")
output_dir += f"/{run_id}"

dbutils.widgets.dropdown("3. Export source tags","no",["yes","no"])
export_source_tags = dbutils.widgets.get("3. Export source tags") == "yes"
notebook_formats = get_notebook_formats(4)

print("run_id:", run_id)
print("output_dir:", output_dir)
print("export_source_tags:", export_source_tags)
print("notebook_formats:", notebook_formats)

# COMMAND ----------

if len(run_id)==0: raise Exception("ERROR: Run ID is required")
if len(output_dir)==0: raise Exception("ERROR: DBFS destination is required")
  
import mlflow

# COMMAND ----------

# MAGIC %md ### Display MLflow UI URI of Run

# COMMAND ----------

display_run_uri(run_id)

# COMMAND ----------

# MAGIC %md ### Remove any previous exported run data

# COMMAND ----------

dbutils.fs.rm(output_dir, True)

# COMMAND ----------

# MAGIC %md ### Export the run

# COMMAND ----------

from mlflow_export_import.run.export_run import RunExporter
exporter = RunExporter(mlflow.tracking.MlflowClient(), export_source_tags, notebook_formats)
exporter.export_run(run_id, output_dir)

# COMMAND ----------

# MAGIC %md ### Display  exported run files

# COMMAND ----------

import os
output_dir = output_dir.replace("dbfs:","/dbfs")
os.environ['OUTPUT_DIR'] = output_dir

# COMMAND ----------

# MAGIC %sh echo $OUTPUT_DIR

# COMMAND ----------

# MAGIC %sh ls -l $OUTPUT_DIR

# COMMAND ----------

# MAGIC %sh cat $OUTPUT_DIR/run.json

# COMMAND ----------

# MAGIC %sh ls -lR $OUTPUT_DIR/artifacts

# COMMAND ----------

# MAGIC %md # Import Run

# COMMAND ----------

# MAGIC %md ### Setup

# COMMAND ----------

# dbutils.widgets.text("1. Destination experiment name", "") 
# experiment_name = dbutils.widgets.get("1. Destination experiment name")
experiment_name = '/Users/victor.rodrigues@databricks.com/Others/tests/mlflow_export_import/imports/suave-flea-imported'

# dbutils.widgets.text("2. Input directory", "") 
# input_dir = dbutils.widgets.get("2. Input directory")
input_dir = output_dir
 
print("input_dir:",input_dir)
print("experiment_name:",experiment_name)

# COMMAND ----------

if len(input_dir)==0: raise Exception("ERROR: Input directory is required")
if len(experiment_name)==0: raise Exception("ERROR: Destination experiment name is required")

# COMMAND ----------

# MAGIC %md ### Import the run

# COMMAND ----------

import mlflow
from mlflow_export_import.run.import_run import RunImporter
importer = RunImporter(mlflow.tracking.MlflowClient())
run, _ = importer.import_run(experiment_name, input_dir)
run.info.run_id

# COMMAND ----------

# MAGIC %md ### Display MLflow UI URIs

# COMMAND ----------

display_run_uri(run.info.run_id)
