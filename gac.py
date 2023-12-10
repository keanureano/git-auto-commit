import os
import openai


def main():
    """
    Main function.
    """

    loadEnvVariables()
    openai.api_key = os.getenv("OPENAI_API_KEY")


def loadEnvVariables(file_path=".env"):
    """
    Load environment variables from a file.
    """

    try:
        with open(file_path) as f:
            for line in f:
                if "=" in line:
                    key, value = map(str.strip, line.split("=", 1))
                    os.environ[key] = value.replace("\\n", "\n")

    except FileNotFoundError:
        raise FileNotFoundError(
            f"{file_path} not found. Create a '.env' file and set OPENAI_API_KEY."
        )


if __name__ == "__main__":
    main()
