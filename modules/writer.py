from os.path import join

def get_headers():
    """Gets field names based on original excel sheet"""
    with open(join('assets', 'fields.txt'), 'r') as ref:
        headers = [line.strip() for line in ref.readlines()] 
    return headers

def build_line(patient, headers):
    """Organizes patient data according to field order"""
    line = []
    
    for field in headers:
        line.append(patient.get_data(field))
        
    if len(line) == len(headers):
        return ','.join([ln for ln in line])
    else: print("SOMETHING WENT WRONG")

def write_file(patients, filter=None):
    """Takes complete list of patients and creates csv file with appropriate formatting using attributes"""
    outDir = 'Output'
    
    if filter:
        outFile = join(outDir, filter + '.csv')
    else:
        outFile = join(outDir,'complete.csv')
    
    headers = get_headers()
    lines = [','.join([ln.strip('\n') for ln in headers])]
    
    for patient in patients:
        lines.append(build_line(patient, headers))
        
    with open(outFile, 'w+') as f:
        f.write('\n'.join(lines))