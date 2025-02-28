import os
from mlProject import logger
from mlProject.entity.config_entity import DataValidationConfig
import pandas as pd



class DataValidation:
    def __init__(self, config):
        """
        Initializes the DataValidation object with the provided configuration.
        
        Args:
            config: A configuration object containing:
                - unzip_data_dir: Path to the CSV data file.
                - all_schema: Dictionary of expected column names and their data types.
                - STATUS_FILE: Path to the file where validation status will be written.
        """
        self.config = config

    def validate_all_columns(self) -> bool:
        """
        Validates the following:
          1. All expected columns are present in the data.
          2. The data types of each column match what is expected.
          
        Writes the validation status (and any error messages) to the status file.
        
        Returns:
            bool: True if all validations pass; False otherwise.
        """
        try:
            # Load the CSV data into a DataFrame.
            data = pd.read_csv(self.config.unzip_data_dir)           

            logger.info(f"Data loaded from: {self.config.unzip_data_dir}")

            valid = True  # Flag indicating overall validation status
            messages = []  # List to collect error messages

            # 1. Check that all expected columns are present.
            expected_columns = list(self.config.all_schema.keys())
            missing_columns = [col for col in expected_columns if col not in data.columns]
            if missing_columns:
                error_msg = f"Missing columns: {missing_columns}"
                logger.error(error_msg)
                messages.append(error_msg)
                valid = False

            # 2. Validate that the data types of each column match the expected types.
            dtype_errors = []
            for col, expected_type in self.config.all_schema.items():
                if col in data.columns:
                    # Compare the string representation of the pandas dtype with the expected type.
                    if str(data[col].dtype) != expected_type:
                        dtype_errors.append(f"{col}: expected {expected_type}, got {data[col].dtype}")
            if dtype_errors:
                error_msg = f"Data type mismatches found: {dtype_errors}"
                logger.error(error_msg)
                messages.append(error_msg)
                valid = False

            # Write the validation status and any messages to the status file.
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {valid}\n")
                if messages:
                    f.write("\n".join(messages))

            if valid:
                logger.info("All validations passed successfully.")
            return valid

        except Exception as e:
            logger.exception("Exception occurred during validation")
            raise e


