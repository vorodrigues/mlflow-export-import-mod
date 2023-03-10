""" 
Import a list of experiment from a directory.
"""

import os
import json
import click
from concurrent.futures import ThreadPoolExecutor

import mlflow

from mlflow_export_import import click_doc
from mlflow_export_import.experiment.import_experiment import ExperimentImporter
from mlflow_export_import import utils


def _import_experiment(importer, exp_name, exp_input_dir):
    try:
        importer.import_experiment(exp_name, exp_input_dir)
    except Exception:
        import traceback
        traceback.print_exc()


def import_experiments(client, input_dir, use_src_user_id=False, use_threads=False): 
    path = utils._read_manifest_json_file(input_dir, "experiments.json")
    with open(path, "r", encoding="utf-8") as f:
        dct = json.loads(f.read())
    for exp in dct["experiments"]:
        print("  ",exp)

    importer = ExperimentImporter(client, use_src_user_id=use_src_user_id)
    max_workers = os.cpu_count() or 4 if use_threads else 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for exp in dct["experiments"]:
            exp_input_dir = os.path.join(input_dir,exp["id"])
            exp_name = exp["name"]
            executor.submit(_import_experiment, importer, exp_name, exp_input_dir)

@click.command()
@click.option("--input-dir", 
    help="Input directory.", 
    type=str,
    required=True
)
@click.option("--use-src-user-id", 
    help=click_doc.use_src_user_id, 
    type=bool, 
    default=False, 
    show_default=True
)
@click.option("--use-threads",
    help=click_doc.use_threads,
    type=bool,
    default=False,
    show_default=True
)

def main(input_dir, use_src_user_id, use_threads): 
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    client = mlflow.tracking.MlflowClient()
    import_experiments(client, input_dir, use_src_user_id, use_threads)

if __name__ == "__main__":
    main()
