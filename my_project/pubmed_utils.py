import requests
import csv
import re
import xml.etree.ElementTree as ET
from typing import List, Dict

# Constants for the PubMed API
PUBMED_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Function to fetch PubMed IDs based on a query
def fetch_pubmed_ids(query: str, debug: bool = False) -> List[str]:
    """
    Fetches PubMed IDs for a given query.

    Args:
        query (str): The search query for PubMed.
        debug (bool): If True, prints debug information.

    Returns:
        List[str]: A list of PubMed IDs.
    """
    if not query.strip():
        raise ValueError("Query cannot be empty or whitespace.")

    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 100
    }
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(PUBMED_BASE_URL, params=params)
            response.raise_for_status()
            if debug:
                print("Fetching PubMed IDs with query:", query)
                print("Response:", response.text)
            data = response.json()
            if "esearchresult" not in data or "idlist" not in data["esearchresult"]:
                raise ValueError("Invalid response structure from PubMed API.")
            return data["esearchresult"]["idlist"]
        except requests.exceptions.RequestException as e:
            if attempt < 2:  # Retry for transient errors
                print(f"Retrying due to error: {e}")
            else:
                raise RuntimeError(f"Failed to fetch PubMed IDs after 3 attempts: {e}")

# Function to fetch detailed information for PubMed IDs
def fetch_paper_details(pubmed_ids: List[str], debug: bool = False) -> List[Dict[str, str]]:
    """
    Fetches detailed information for a list of PubMed IDs.

    Args:
        pubmed_ids (List[str]): A list of PubMed IDs.
        debug (bool): If True, prints debug information.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing paper details.
    """
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(PUBMED_FETCH_URL, params=params)
            response.raise_for_status()
            if debug:
                print("Fetching details for PubMed IDs:", pubmed_ids)
                print("Response:", response.text)
            return parse_paper_details(response.text, debug=debug)
        except requests.exceptions.RequestException as e:
            if attempt < 2:  # Retry for transient errors
                print(f"Retrying due to error: {e}")
            else:
                raise RuntimeError(f"Failed to fetch paper details after 3 attempts: {e}")

# Function to parse XML data and extract required fields
def parse_paper_details(xml_data: str, debug: bool = False) -> List[Dict[str, str]]:
    """
    Parses XML data to extract paper details.

    Args:
        xml_data (str): XML response from PubMed API.
        debug (bool): If True, prints debug information.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing paper details.
    """
    papers = []
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse XML data: {e}")

    for article in root.findall(".//PubmedArticle"):
        paper = {
            "PubmedID": article.findtext(".//PMID") or "Unknown",
            "Title": article.findtext(".//ArticleTitle") or "Unknown",
            "Publication Date": "",
            "Non-academic Author(s)": "None",
            "Company Affiliation(s)": "None",
            "Corresponding Author Email": "None"
        }
        day = article.findtext(".//PubDate/Day", "")
        month = article.findtext(".//PubDate/Month", "")
        year = article.findtext(".//PubDate/Year", "")

        if day and month and year:
            paper["Publication Date"] = f"{year}/{month}/{day}"
        elif year:
            paper["Publication Date"] = year

        authors = []
        affiliations = []

        for author in article.findall(".//Author"):
            name = author.findtext("LastName", "") + ", " + author.findtext("ForeName", "")
            affiliation = author.findtext(".//Affiliation", "")
            email = ""

            email_match = re.search(r"[\w.-]+@[\w.-]+", affiliation)
            if email_match:
                email = email_match.group(0)
                paper["Corresponding Author Email"] = email

            authors.append(name)
            affiliations.append(affiliation)

        non_academic_authors = filter_non_academic_authors(authors, affiliations)
        if non_academic_authors:
            paper["Non-academic Author(s)"] = "; ".join([author["name"] for author in non_academic_authors])
            paper["Company Affiliation(s)"] = "; ".join([author["company"] for author in non_academic_authors])

        papers.append(paper)

    if debug:
        print("Parsed Papers:", papers)

    return papers

# Function to identify non-academic authors and their companies
def filter_non_academic_authors(authors: List[str], affiliations: List[str]) -> List[Dict[str, str]]:
    """
    Identifies non-academic authors based on company keywords.

    Args:
        authors (List[str]): List of author names.
        affiliations (List[str]): List of affiliations.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing non-academic author names and their companies.
    """
    filtered_authors = []
    company_keywords = [
        "Inc", "Ltd", "Corp", "Corporation", "Pharma", "Biotech",
        "Biopharma", "HealthTech", "Lab", "Research Institute",
        "Company", "Therapeutics", "Healthcare"
    ]

    for name, affiliation in zip(authors, affiliations):
        if any(keyword in affiliation for keyword in company_keywords):
            filtered_authors.append({
                "name": name,
                "company": affiliation
            })

    return filtered_authors

# Function to save results to a CSV file
def save_to_csv(filename: str, papers: List[Dict[str, str]]):
    """
    Saves paper details to a CSV file.

    Args:
        filename (str): Name of the output CSV file.
        papers (List[Dict[str, str]]): List of paper details.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"
        ])
        writer.writeheader()
        writer.writerows(papers)
