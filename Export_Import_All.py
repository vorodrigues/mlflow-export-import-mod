# Databricks notebook source
# MAGIC %md # Export All
# MAGIC 
# MAGIC ## To be executed in source workspace
# MAGIC 
# MAGIC Widgets
# MAGIC * Base output directory
# MAGIC * Export source tags
# MAGIC * Notebook formats
# MAGIC * Use threads

# COMMAND ----------

dbutils.widgets.text("1. Output base directory", "") 
output_dir = dbutils.widgets.get("1. Output base directory")
output_dir = output_dir.replace("dbfs:","/dbfs")

dbutils.widgets.dropdown("2. Export source tags","no",["yes","no"])
export_source_tags = dbutils.widgets.get("2. Export source tags") == "yes"

all_formats = [ "SOURCE", "DBC", "HTML", "JUPYTER" ]
dbutils.widgets.multiselect("3. Notebook formats",all_formats[0],all_formats)
notebook_formats = dbutils.widgets.get("3. Notebook formats")

dbutils.widgets.dropdown("4. Use threads","no",["yes","no"])
use_threads = dbutils.widgets.get("4. Use threads") == "yes"

print("output_dir:",output_dir)
print("export_source_tags:",export_source_tags)
print("notebook_formats:",notebook_formats)
print("use_threads:",use_threads)

# COMMAND ----------

if len(output_dir)==0: raise Exception("ERROR: Output base directory is required")

# COMMAND ----------

import mlflow
from mlflow_export_import.bulk.export_all import export_all
export_all(output_dir, export_source_tags, notebook_formats, use_threads)

# COMMAND ----------

# MAGIC %md ### Display  exported files

# COMMAND ----------

import os
output_dir = output_dir.replace("dbfs:","/dbfs")
os.environ['OUTPUT_DIR'] = output_dir
output_dir

# COMMAND ----------

# MAGIC %sh echo $OUTPUT_DIR

# COMMAND ----------

# MAGIC %sh ls -lR $OUTPUT_DIR

# COMMAND ----------

# MAGIC %md # Import All
# MAGIC 
# MAGIC ## To be executed in destination workspace

# COMMAND ----------

dbutils.widgets.text("1. Input directory", "") 
input_dir = dbutils.widgets.get("1. Input directory")
input_dir = input_dir.replace("dbfs:","/dbfs")

dbutils.widgets.dropdown("2. Import source tags","no",["yes","no"])
import_source_tags = dbutils.widgets.get("2. Import source tags") == "yes"

dbutils.widgets.dropdown("3. Use threads","no",["yes","no"])
use_threads = dbutils.widgets.get("3. Use threads") == "yes"

print("input_dir:",input_dir)
print("import_source_tags:",import_source_tags)
print("use_threads:",use_threads)

# COMMAND ----------

if len(input_dir)==0: raise Exception("ERROR: Input directory is required")

# COMMAND ----------

from mlflow_export_import.bulk.import_models import import_all
import mlflow
import_all(
  client=mlflow.tracking.MlflowClient(),
  input_dir=input_dir,
  delete_model=False,
  import_source_tags=import_source_tags,
  use_threads=use_threads
)
