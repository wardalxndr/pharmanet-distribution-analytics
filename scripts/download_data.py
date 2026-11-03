"""Download the wholesale pharma dataset from Kaggle into data/.

Run from the project root:
    .venv\\Scripts\\python scripts\\download_data.py

Needs pip install kagglehub (already in requirements-dev or run pip manually).
If Kaggle asks for credentials: create a token at kaggle.com -> Settings -> API,
then set env vars KAGGLE_USERNAME and KAGGLE_KEY (or put kaggle.json in
%USERPROFILE%\\.kaggle\\).
"""

import os
import shutil

import kagglehub

DATASET = "krishangupta33/pharmaceutical-company-wholesale-retail-data"


def main():
    raw_path = kagglehub.dataset_download(DATASET)
    print("downloaded to:", raw_path)

    os.makedirs("data", exist_ok=True)
    for name in sorted(os.listdir(raw_path)):
        src = os.path.join(raw_path, name)
        dst = os.path.join("data", name)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            print("copied:", dst)


if __name__ == "__main__":
    main()
