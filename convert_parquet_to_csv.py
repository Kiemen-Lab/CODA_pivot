
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

    pth1 = r'\\10.99.134.183\kiemen-lab-data\collaborations\Deconvolve Visium\IPMN Luciane\IPMN1_PN_1PMN6_1F_4\binned_outputs'
    pth2 = r'\\10.99.134.183\kiemen-lab-data\collaborations\Deconvolve Visium\IPMN Luciane\IPMN2_S22_14734_5AA_3\binned_outputs'
    pth3 = r'\\10.99.134.183\kiemen-lab-data\collaborations\Deconvolve Visium\IPMN Luciane\IPMN3_S24_05795_3M_3\binned_outputs'
    pth4 = r'\\10.99.134.183\kiemen-lab-data\collaborations\Deconvolve Visium\IPMN Luciane\IPMN4_5CC_2\binned_outputs'

    convert_to_csv(os.path.join(pth1, 'square_002um','spatial','tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth1, 'square_008um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth1, 'square_016um', 'spatial', 'tissue_positions.parquet'))

    convert_to_csv(os.path.join(pth2, 'square_002um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth2, 'square_008um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth2, 'square_016um', 'spatial', 'tissue_positions.parquet'))

    convert_to_csv(os.path.join(pth3, 'square_002um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth3, 'square_008um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth3, 'square_016um', 'spatial', 'tissue_positions.parquet'))

    convert_to_csv(os.path.join(pth4, 'square_002um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth4, 'square_008um', 'spatial', 'tissue_positions.parquet'))
    convert_to_csv(os.path.join(pth4, 'square_016um', 'spatial', 'tissue_positions.parquet'))

