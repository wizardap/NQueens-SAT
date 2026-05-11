# N-Queens Problem solve with SAT solver
This repository contains a Python implementation of a solution to the N-Queens problem using a SAT solver. The N-Queens problem is a classic combinatorial problem that asks for all arrangements of N queens on an N x N chessboard such that no two queens threaten each other.
## Requirements
- Python 3.x
- PySAT library (can be installed via pip)
## Installation

1. Clone the repository:
```bash
git clone https://github.com/wizardap/NQueens-SAT.git
cd NQueens-SAT
```
2. Install virtual environment (optional but recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
## Usage
To solve the N-Queens problem for a specific value of N, run the following command:
```bash
python playground.py 
```
Change the encoding method in the `playground.py` file to use different encodings.