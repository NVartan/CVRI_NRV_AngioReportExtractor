from os import listdir, getenv
from modules import meta, parser, writer
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Hello from extractor!")
    #TODO: Extract constants from .env file for easier customization
    
    dataDir = getenv('DATADIR')
    
    patients = parser.create_subject(dataDir)
    
    for pt in patients:
        for file in pt.files:
            pt = parser.get_data(pt, file)            
        pt = pt.validate_data()
        
    writer.write_file(patients)
        


if __name__ == "__main__":
    main()
