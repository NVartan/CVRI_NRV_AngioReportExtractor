import os
from os import listdir, getenv
from modules import meta, parser, writer
from dotenv import load_dotenv

from modules._paths import PROJECT_ROOT, ENV_FILE

load_dotenv(str(ENV_FILE))


def main():
    print("Hello from extractor!")

    dataDir = getenv('DATADIR')
    if dataDir and not os.path.isabs(dataDir):
        dataDir = os.path.join(PROJECT_ROOT, dataDir)

    patients = parser.create_subject(dataDir)

    for pt in patients:
        for file in pt.files:
            pt = parser.get_data(pt, file)
        pt = pt.validate_data()

        print(pt)

    writer.write_file(patients)


if __name__ == "__main__":
    main()
