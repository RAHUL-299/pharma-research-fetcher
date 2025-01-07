# **PubMed Paper Fetcher**

## **Description**
A Python program to fetch research papers from PubMed based on a user-specified query. The program interacts with the PubMed API to search for research papers, retrieve their details, and save the results to a CSV file for further analysis. 

It is designed to help researchers quickly access relevant publications, especially identifying papers with authors affiliated with pharmaceutical or biotech companies.

---

## **Project Organization**

### **1. Module (`pubmed_utils.py`)**
Contains the core logic for interacting with the PubMed API. It defines functions to:
- Fetch PubMed IDs based on a query.
- Retrieve detailed information for a list of PubMed IDs.
- Parse and filter non-academic authors based on their affiliations.
- Save the fetched details to a CSV file.

### **2. Command-line Interface (CLI) Program (`main.py`)**
The `main.py` script is the entry point of the application. It:
- Accepts command-line arguments to specify search queries, debug options, and output file names.
- Calls functions from `pubmed_utils.py` to fetch, display, or save the research paper details.

---

## **Installation**

### **Prerequisites**
- Python 3.8 or later
- Poetry (for dependency management)

### **Steps**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/RAHUL-299/pharma-research-fetcher
   cd pharma-research-fetcher
   ```

2. **Install Dependencies**
   If Poetry is not installed, you can install it using:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   Then, install project dependencies:
   ```bash
   poetry install
   ```

3. **Activate Virtual Environment**
   ```bash
   poetry shell
   ```

---

## **How to Execute the Program**

### **Basic Usage**
Run the program from the command line:
```bash
 poetry run get-papers-list "your query here"
```

### **Saving Results**
To save the results to a CSV file, use the `-f` flag:
```bash
poetry run python my_project/main.py "cancer research" -f results.csv
```

### **Debug Mode**
Enable debug mode to print detailed logs:
```bash
poetry run python my_project/main.py "cancer research" -d
```

### **Arguments**
- **`query`** (Positional): The PubMed search query (e.g., `"cancer research"`).
- **`-f` / `--file`** (Optional): The filename to save the results as a CSV file.
- **`-d` / `--debug`** (Optional): Enable debug mode to print detailed logs.

---

## **Code Structure**
```bash
project/
├── my_project_rahulM/                # Main package directory
│   ├── __init__.py            # Marks the directory as a Python package
│   ├── pubmed_utils.py        # Core logic for PubMed API interaction
│   └── main.py                # Command-line interface (CLI) program
├── pyproject.toml             # Poetry configuration file
├── README.md                  # Project documentation (this file)
├── poetry.lock                # Lock file for dependencies
└── .gitignore                 # Ignored files for version control
```

---

## **Tools and Libraries Used**

### **Python Libraries**
- **`requests`**: For making HTTP requests to the PubMed API.  
  [Requests Documentation](https://docs.python-requests.org/en/master/)
- **`argparse`**: For parsing command-line arguments.
- **`xml.etree.ElementTree`**: For parsing XML data from the PubMed API.

### **Development Tools**
- **`Poetry`**: Dependency management and packaging.  
  [Poetry Documentation](https://python-poetry.org/docs/)
- **`pytest`**: A testing framework used for writing and running test cases.  
  [Pytest Documentation](https://docs.pytest.org/)

### **LLM Assistance**
This project was developed with assistance from **OpenAI's GPT-4**, which helped in:
- Refactoring code for readability and maintainability.
- Designing robust error-handling mechanisms.
- Helpd in creatng this README.md file with spoof reading, strcture tweaks, and word typos to make it more functonal!

Learn more about GPT-4: [https://openai.com/gpt](https://openai.com/gpt)

---

## **Contributing**
We welcome contributions to improve this project! Please:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a detailed description of your changes.

Ensure your code follows the existing style and passes all tests.

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for more details.
