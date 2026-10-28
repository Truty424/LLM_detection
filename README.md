# LLM-based Cryptographic Asset Detection

## Overview

This project implements an LLM-based approach for detecting cryptographic assets in source code. It uses a locally deployed language model through Ollama to analyse Java source files and identify cryptographic assets and their properties.

The project was developed as part of a master's thesis investigating the use of large language models for cryptographic asset detection.

## Supported Libraries and Asset Types

The tool supports the detection of cryptographic assets associated with the following Java libraries:

- `java.security`
- `javax.crypto`

The detection is limited to the following CycloneDX cryptographic asset types:

- **Algorithm**
- **Related Crypto Material**

## Requirements

- Python 3
- [Ollama](https://ollama.com/)
- Qwen2.5-Coder 7B model
- A locally available Java source code repository

## Setup

Clone this repository:

```bash
git clone https://github.com/Truty424/LLM_detection.git
cd LLM_detection
```

Install and start Ollama, then download the required model:

```bash
ollama pull qwen2.5-coder:7b
```

Ensure that the Ollama service is running locally.

## Usage

Run the tool by providing the path to a locally available source code repository:

```bash
python main.py /path/to/local/repository
```

To specify a custom output file:

```bash
python main.py /path/to/local/repository --output results.txt
```

The tool analyses Java source files and saves the detected cryptographic information to the specified output file.

## Model Configuration

The default configuration uses `qwen2.5-coder:7b` with temperature set to `0` and a context window of `4096` tokens. These settings can be modified in `main.py`.
