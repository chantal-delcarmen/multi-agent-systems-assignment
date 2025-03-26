import subprocess
import sys
import platform
import zipfile
import os
import shutil
import venv
import argparse

# Color codes for terminal output
RED = "\033[31m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def check_version() -> bool:
    """
    Check if the Python version is compatible.

    Returns:
        bool: True if version is compatible, False otherwise
    """
    if sys.version_info[:2] != (3, 12):
        print(f"{RED}Wrong Python version installed! Requires Python 3.12.{RESET}")
        return False
    return True


def create_virtual_environment(venv_path: str = ".venv") -> bool:
    """
    Create a virtual environment.

    Args:
        venv_path (str): Path to create the virtual environment

    Returns:
        bool: True if venv creation successful, False otherwise
    """
    try:
        # Remove existing venv if it exists
        if os.path.exists(venv_path):
            print(f"{YELLOW}Removing existing virtual environment...{RESET}")
            shutil.rmtree(venv_path)

        # Create new virtual environment
        print(f"{GREEN}Creating virtual environment...{RESET}")
        venv.create(venv_path, with_pip=True)
        return True
    except Exception as e:
        print(f"{RED}Error creating virtual environment: {e}{RESET}")
        return False


def get_pip_executable(venv_path: str = ".venv") -> str:
    """
    Get the path to pip executable in the virtual environment.

    Args:
        venv_path (str): Path to the virtual environment

    Returns:
        str: Path to pip executable
    """
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "pip")
    return os.path.join(venv_path, "bin", "pip")


def install_requirements(
    venv_path: str = ".venv", req_file: str = "requirements.txt"
) -> bool:
    """
    Install requirements in the virtual environment.

    Args:
        venv_path (str): Path to the virtual environment
        req_file (str): Path to requirements file

    Returns:
        bool: True if installation successful, False otherwise
    """
    try:
        pip_executable = get_pip_executable(venv_path)

        # Read requirements
        with open(req_file, "r") as file:
            requirements = [req.strip() for req in file.readlines() if req.strip()]

        if not requirements:
            print("No requirements found.")
            return True

        # Install requirements
        print(f"{GREEN}Installing requirements...{RESET}")
        for package in requirements:
            print(f"Installing {package}...")
            result = subprocess.run(
                [pip_executable, "install", package], capture_output=True, text=True
            )

            if result.returncode == 0:
                print(f"{GREEN}Successfully installed {package}.{RESET}")
            else:
                print(f"{RED}Error installing {package}: {result.stderr}{RESET}")

        return True
    except Exception as e:
        print(f"{RED}Error installing requirements: {e}{RESET}")
        return False


def delete_clients():
    """
    Delete existing client directories.
    """
    dir_path = "./client/"
    try:
        for item in os.listdir(dir_path):
            if item.endswith("-client"):
                item_path = os.path.join(dir_path, item)
                shutil.rmtree(item_path)
    except Exception as e:
        print(f"{RED}Error deleting clients: {e}{RESET}")


def client_is_installed(client_dir: str) -> bool:
    """
    Check if client is already installed.

    Args:
        client_dir (str): Directory to check for client installation

    Returns:
        bool: True if client is installed, False otherwise
    """
    try:
        return any(
            file.endswith((".app", ".exe", ".AppImage"))
            for file in os.listdir(client_dir)
        )
    except Exception:
        return False


def install_client():
    """
    Install client based on the current operating system.
    """

    # Determine OS
    os_name = platform.system().lower()
    if os_name == "darwin":
        os_name = "mac"
    elif os_name == "windows":
        os_name = "win"
    elif os_name == "linux":
        os_name = "linux"

    zip_path = f"./client/{os_name}-client/{os_name}-client.zip"
    extract_path = "./client/"

    # Check if client is already installed
    if client_is_installed(extract_path):
        print("Client is already installed.")
        return

    try:
        # Python zip extract breaks on other systems for some reason
        if os_name == "win":
            with zipfile.ZipFile(zip_path, "r") as z_file:
                z_file.extractall(extract_path)

        else:
            command = ["unzip", "-o", zip_path, "-d", extract_path]
            _ = subprocess.run(command, check=True, stdout=subprocess.DEVNULL)

        # Clean up other client versions
        delete_clients()

        print(f"{GREEN}Client successfully installed.{RESET}")
    except Exception as e:
        print(f"{RED}Error installing client: {e}{RESET}")


def main():
    parser = argparse.ArgumentParser(description="Project Setup Script")
    _ = parser.add_argument(
        "--no-venv", action="store_true", help="Skip virtual environment creation"
    )
    _ = parser.add_argument(
        "--no-requirements", action="store_true", help="Skip requirements installation"
    )
    _ = parser.add_argument(
        "--no-client", action="store_true", help="Skip client installation"
    )

    args = parser.parse_args()

    # Version check
    if not check_version():
        sys.exit(1)

    # Virtual Environment Setup
    if not args.no_venv:  # pyright: ignore[reportAny]
        if not create_virtual_environment():
            sys.exit(1)

    # Requirements Installation
    if not args.no_requirements:  # pyright: ignore[reportAny]
        if not install_requirements():
            sys.exit(1)

    # Client Installation
    if not args.no_client:  # pyright: ignore[reportAny]
        install_client()

    print(f"{GREEN}Setup completed successfully!{RESET}")


if __name__ == "__main__":
    main()
