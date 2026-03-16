# Notebook Structure

This project keeps production-style code in `src/embedding_retrieval` and uses notebooks only for interactive experiments.

## Recommended notebooks

- `00_setup.ipynb`
  Loads the project path, imports the retrieval module, and validates the environment.
- `01_quick_experiment.ipynb`
  Runs a small ingestion and search flow against sample documents.
- `02_model_comparison.ipynb`
  Compares embedding providers, chunk sizes, and top-k settings.
- `03_dataset_eval.ipynb`
  Evaluates retrieval quality against a fixed query set.
- `04_rag_eval.ipynb`
  Retrieves context and sends it to the configured LLM.

## Rules

- Keep reusable logic in `src/`, not in notebook cells.
- Treat notebooks as experiment entry points and result logs.
- Reset and rerun all cells when results look inconsistent.
- Use one notebook per purpose instead of one large scratchpad.
