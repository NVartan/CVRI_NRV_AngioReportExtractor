Extracts data from exported reports into specifically formatted csv file for further analysis

# Dependancies
python >= 3.13
dotenv>=0.9.9

# Setup and Use
1. Open a terminal and navigate to this directory via `cd path/to/directory`
2. Run `pip3 install -e .` or equivalent command for package manager alternative (tested with pipx)
3. Drop all data in `./Data` or set `DATADIR = /path/to/data` in .env
4. Run using the command `extractor`


# Coming Soon
- Ability to filter based on specific value ranges and fields