
import os
import pandas as pd

def convert_to_csv(input_filename):
    """
        Converts a Visium tissue_positions.parquet file to a CSV file.

        Args:
            input_filename (str): Path to the input parquet file.

        Returns:
            str: Path to the output CSV file.
        """
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"File not found: {input_filename}")

    # Read the parquet file
    df = pd.read_parquet(input_filename)

    # Define output CSV filename
    output_filename = input_filename.replace(".parquet", ".csv")

    # Save as CSV
    df.to_csv(output_filename, index=False)

    print(f"Converted: {input_filename} → {output_filename}")

if __name__ == '__main__':

    # example run to convert all three parquet files for Visium HD to csv files
    pth = r'C:\Users\Ashley\Documents\Visium_HD_sample_1\binned_outputs'
    convert_to_csv(os.path.join(pth, 'square_002um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth, 'square_008um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth, 'square_016um', 'spatial', 'tissue_positions.parquet'))


