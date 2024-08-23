import os


def save_receipt(text: str, receipt_path: str) -> None:
    try:
        # Find if the directory exists, if not, create it
        directory = os.path.dirname(receipt_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the receipt
        with open(receipt_path, 'w') as f:
            f.write(text)
    except OSError as e:
        raise IOError(f"An error occurred while trying to save the receipt to '{receipt_path}': {e}")
