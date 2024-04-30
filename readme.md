# Automatic Lean4 Compilation

The **automatic-lean4-compilation** repository automates the compilation of Lean4 language statements stored in JSON files. Its primary goal is to ensure the grammatical correctness and logical consistency of statements and proofs in Lean4, while also providing compilation information.

This repository builds upon the foundation of [repl](https://github.com/leanprover-community/repl), a tool designed to interface directly with the Lean4 compiler in the terminal.

## Prerequisites

Before using this tool, ensure that the following prerequisites are met (Linux only):

- Install [elan](https://github.com/leanprover/elan) by running the following command:

  ```bash
  curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
  ```

- Install dependencies using the following commands:

  - Linux

  ```bash
  wget -q https://raw.githubusercontent.com/leanprover-community/mathlib4/master/scripts/install_debian.sh && bash install_debian.sh ; rm -f install_debian.sh && source ~/.profile
  ```

For other platforms, refer to [Lean4 setup documentation](https://lean-lang.org/lean4/doc/setup.html) for more details.

## Installation

To install **automatic-lean4-compilation**, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/rookie-joe/automatic-lean4-compilation.git
   ```

2. Navigate to the cloned directory:

   ```bash
   cd automatic-lean4-compilation
   ```

3. Run `lake update` to install the corresponding version of mathlib, as specified in the `lakefile.lean` and `lake-manifest.json` files.

4. Test the installation:

   - Run the following command to verify the Lean compiler and the REPL repository:

     ```bash
     echo '{  "cmd" : "def f := 2"  }'| lake exe repl
     ```

   - Additionally, you can test whether mathlib is correctly installed:

     ```bash
     echo '{"path": "test/test.lean", "allTactics": true}' | lake exe repl
     ```

   A successful installation will output `{"env": 0}` for both commands.

   Alternatively, you can run `test.sh` for a comprehensive check of the prerequisites.

## Usage

The quickest way to use the tool is by running the following command:

```bash
python3 pass_rate_new.py --input_path {input_path} --output_path {output_path}
```

- `input_path` should be a directory containing `*.json` files. Each JSON file should contain a dictionary with two keys: `"statement"` for the Lean4-based language to be compiled and `"working_file"` for the predependencies of the `"statement_proof"`, e.g., importing mathlib.

- `output_path` is recommended to be a text file that will display the compilation process and the final compilation pass rate for all items in `input_path`.

## Contribution

We're actively seeking more contributors to join our project! Your efforts are greatly appreciated and welcomed.


