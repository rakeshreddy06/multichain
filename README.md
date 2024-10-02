# Secure Multiparty Computation for Market Basket Analysis

## Project Overview

This project implements a Secure Multiparty Computation (SMPC) model to analyze market basket data across different retail sectors, including convenience stores, department stores, and pharmacies. The goal is to determine the most frequently purchased item while preserving the privacy of each party's data.

## Features

- Utilizes SMPC techniques to maintain data privacy
- Analyzes market basket data from multiple retail sectors
- Determines the most frequently purchased item across all parties
- Preserves confidentiality of individual party data

## Requirements

- Python 3.11+

## Usage

To run the SMPC analysis, execute the following commands in three different terminal shells:

1. For Party 1:
   ```
   py .\SourceCode\party1.py --party 0 --nr_of_parties 3
   ```

2. For Party 2:
   ```
   py .\SourceCode\party2.py --party 1 --nr_of_parties 3
   ```

3. For Party 3:
   ```
   py .\SourceCode\party3.py --party 2 --nr_of_parties 3
   ```

## How It Works

(Provide a brief explanation of the SMPC process and how the analysis is performed)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or concerns, please open an issue or contact rakeshreddy5566@gmail.com.
