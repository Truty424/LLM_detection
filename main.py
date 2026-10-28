
import argparse
import time
from pathlib import Path
from parser.repo_parser import RepoParser

# Model configuration
OLLAMA_BASE = "http://localhost:11434"
MODEL = "qwen2.5-coder:7b"
TEMPERATURE = 0
TIMEOUT = 180
NUM_CTX = 4096


def main():
    parser = argparse.ArgumentParser(
        description="Detect cryptographic assets in a local source code repository."
    )

    parser.add_argument(
        "repo_path",
        help="Path to the local repository"
    )

    parser.add_argument(
        "--output",
        default="results/results.txt",
        help="Path to the output file (default: results.txt)"
    )

    args = parser.parse_args()

    repo_path = Path(args.repo_path).expanduser().resolve()

    if not repo_path.is_dir():
        parser.error(f"Repository directory does not exist: {repo_path}")

    start_time = time.time()

    repo_parser = RepoParser(
        str(repo_path),
        args.output,
        OLLAMA_BASE,
        MODEL,
        TEMPERATURE,
        TIMEOUT,
        NUM_CTX
    )

    repo_parser.run()

    print(f"Execution time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
