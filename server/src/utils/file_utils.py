class FileUtils:
    @staticmethod
    def read_file_content(file_path: str) -> str:
        """
        Read content from a file and return it as a string.

        Args:
            file_path (str): Path to the file to read

        Returns:
            str: Content of the file
        """
        with open(file_path, "r") as f:
            return f.read().strip()
