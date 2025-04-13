import os

# Get current working directory
base_path = os.getcwd()

# Define your project name
project_name = "my_project"
project_root = os.path.join(base_path)

# Folder and file structure
structure = {
    "": ["main.py", "requirements.txt", "README.md"],
    "config": ["config.yaml"],
    "data": ["sample_data.csv"],
    "src": ["__init__.py", "utils.py", "core.py"],
    "tests": ["__init__.py", "test_core.py"],
    "notebooks": ["analysis.ipynb"]
}

# Create the directories and files
for folder, files in structure.items():
    folder_path = os.path.join(project_root, folder)
    os.makedirs(folder_path, exist_ok=True)

    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, "w") as f:
            # Fill in default content based on file type
            if file == "main.py":
                f.write('from src.core import run_pipeline\n\nif __name__ == "__main__":\n    run_pipeline()\n')
            elif file == "requirements.txt":
                f.write("# Add your dependencies here\n")
            elif file == "README.md":
                f.write("# My Project\n\nSimple Python project structure.\n")
            elif file == "config.yaml":
                f.write("# Configuration settings\n")
            elif file == "sample_data.csv":
                f.write("id,name\n1,Alice\n2,Bob\n")
            elif file == "utils.py":
                f.write("def helper_function():\n    print('Helper function')\n")
            elif file == "core.py":
                f.write("def run_pipeline():\n    print('Running project pipeline...')\n")
            elif file == "test_core.py":
                f.write("def test_example():\n    assert 1 + 1 == 2\n")
            elif file.endswith(".ipynb"):
                f.write("{\"cells\": [], \"metadata\": {}, \"nbformat\": 4, \"nbformat_minor\": 2}")
            else:
                f.write("")
