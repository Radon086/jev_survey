# Jev Survey — Decision Model Evaluation

## Overview

This project evaluates Jev as a decision model using evaluation tasks provided for the assessment. It compares Jev's performance with GPT-based baselines across different answer formats.

The experiments cover:

- **Multiple-choice selection**
- **Binary (Yes/No) classification**
- **Ordinal scoring (1–5)**

The evaluation focuses on predictive performance, response latency, and API cost.

## Source Code Guide

| File | Description |
|---|---|
| `exp_foxconn.py` | Jev evaluation experiment |
| `exp_foxconn_gpt.py` | GPT baseline experiment |
| `exp_foxconn_gpt_sp.py` | Additional GPT experiment |
| `analyze_foxconn.py` | Analysis of Jev experiment results |
| `analyze_foxconn_gpt.py` | Analysis of GPT experiment results |
| `dataset.py` | Dataset handling |
| `parse_starter_set.py` | Parses the provided starter dataset |
| `test_jev.py` | Jev API test script |
| `test_gpt.py` | GPT API test script |
| `utils.py` | Shared utility functions |

## Results and Outputs

Experiment outputs are organized in the following directories:

- `output/exp/foxconn/` — Jev experiment outputs.
- `output_gpt/exp/foxconn/` — GPT experiment outputs.

The analysis scripts support inspection of the experiment results and comparison of model behavior.

## Evaluation Scope

The experiments use a limited assessment dataset. Results should be interpreted as preliminary evidence of model performance on these specific tasks, rather than proof of general-purpose decision-making ability.

## Execution Status

This repository is provided for source-code and experiment-result inspection. It is **not runnable as submitted** because the required API credentials and configuration have been removed.

To reproduce the experiments, the necessary credentials and configuration must be restored.
