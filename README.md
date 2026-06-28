Extracts data from exported reports into specifically formatted csv file for further analysis

# Dependancies
python >= 3.13
dotenv>=0.9.9


# To Use
1. Save all exported xml reports to a directory
2. Set the directory path in the included .env file
	`DATADIR = /path/to/data/dir`
3. Double click the "Extract" application

# Coming Soon
- Ability to filter based on specific value ranges and fieldsß
- Graphical interface for more user friendly operation

# Ideas for expansion
- Integration of analysis into the script
	- pro: one and done approach, less error prone during transfer through formats
	- con: excel file already has calculations set up, these would need to be recreated
- Automated measurements provided only the image files
	- pro: faster large scale processing with less manpower
	- con: time needed for development and testing, computationally more involved, likely still needs human oversight
- Extension into a predictive model via regression which takes provided values and returns likely result based on training set (data currently being analyzed)
	- pro: clinical value as pre-op tool
	- con: time needed for development and testing. Definitely a long term project.