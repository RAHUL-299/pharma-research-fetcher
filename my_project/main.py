import argparse
from pubmed_utils import fetch_paper_details, fetch_pubmed_ids, save_to_csv

# Main function
def main():
    """
    Main function to handle command-line arguments and execute the program.
    """
    parser = argparse.ArgumentParser(description="Fetch research papers with specific filters.")
    parser.add_argument("query", type=str, help="PubMed query.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results.", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    if not args.query.strip():
        print("Error: Query cannot be empty or whitespace.")
        return

    try:
        pubmed_ids = fetch_pubmed_ids(args.query, debug=args.debug)
        papers = fetch_paper_details(pubmed_ids, debug=args.debug)

        if args.file:
            save_to_csv(args.file, papers)
            print(f"Results saved to {args.file}")
        else:
            for paper in papers:
                print(paper)

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except RuntimeError as re:
        print(f"Runtime Error: {re}")
    except Exception as e:
        print("An unexpected error occurred:", str(e))

if __name__ == "__main__":
    main()

