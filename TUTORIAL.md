# UV Project Setup Tutorial

Based on https://docs.astral.sh/uv/guides/projects/

## Setup Instructions

• Open Git Bash and navigate to ProgramData:
```bash
cd C:\ProgramData
```

• Initialize uv project, run:
```bash
uv init my_uv_project
```

• Alternatively, if you already have an existing uv project, run: `uv sync` instead

• Navigate into folder "my_uv_project", then create a requirements.txt file with the following packages as an example:
```
tlpytools
numpy
pandas
numba
openmatrix
pyarrow
pyyaml
polars
```

• Add all of the packages specified into your project, run:
```bash
uv add -r requirements.txt
```

• Now, you should have a working custom python environment in the `.venv` subfolder
  - To point your script to this environment in VS Code, you can use this path:
    ```
    C:\ProgramData\my_uv_project\.venv\Scripts\python.exe
    ```
  - To activate this environment in git bash, you can use this activate file:
    ```bash
    source C:/ProgramData/my_uv_project/.venv/Scripts/activate
    ```

• Finally, review the main.py and use the example from the following link to try to read / write data from both the Azure SQL Server for sensitive data and from the Azure Data Lake:
https://github.com/TransLinkForecasting/my_uv_project/blob/master/main.py
