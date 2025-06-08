import os
import pandas as pd

def convert_tsv_to_csv(input_filename):
    """
    Converts a TSV file to a CSV file.

    Args:
        input_filename (str): Path to the input TSV file.

    Returns:
        str: Path to the output CSV file.
    """
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"File not found: {input_filename}")

    # Read the TSV file
    df = pd.read_csv(input_filename, sep='\t')

    # Define output CSV filename
    output_filename = input_filename.replace(".tsv", ".csv")

    # Save as CSV
    df.to_csv(output_filename, index=False)

    print(f"Converted: {input_filename} → {output_filename}")
    return output_filename

if __name__ == '__main__':

    # Example run to convert a TSV file to CSV
    pth = r'\\10.99.134.183\kiemen-lab-data\admin\papers\fiducial point registration\final data\MDACC data\raw images\COMET'
    convert_tsv_to_csv(os.path.join(pth, 'COMET_FullPanel_50258-16.tsv'))
