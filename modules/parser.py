import xml.etree.ElementTree as ET

def check_field(field):
    """Checks if a given field name exists in the list of excel fields. Exact wording and capitalization only!"""
    with open('assets/fields.txt', 'r') as f:
        fields = [i.strip('\n') for i in f.readlines()]
        if field in fields: return True
        else: return False
        
    #TODO add name checking for similar names. If similar present, return warning with found value suggested
        
def get_data(subject, file): #BUG only last value remains intact, everything else overwritten (during validation?)
    """Parses XML report into usable data and attaches it to the patient with field names mapped to the excel fields"""
    status = file.split('_')[-1].strip('.xml')
    status_map = [('NoPostDil.imp', 'Available Immediate Post Implantation View (Without BPD)'), ('NoPostDil.2nd', 'Available 2nd View (Without BPD)'), ('BeforePostDil.imp', 'Available before BPD Implantation View'), ('BeforePostDil.2nd', 'Available before BPD 2nd View'), ('AfterPostDil.imp', 'Available After BPD Implantation View'), ('AfterPostDil.2nd', 'Available After BPD 2nd View')]
    print(f'\nparsing {file}')
    
    tree = ET.parse(file)
    root = tree.getroot()
    
    study_info = root.find('./Models/StudyInfo')
    patient_info = root.find('./Models/PatientInfo')
    measurements = root.find('./Custom/Measurements')
    analysis = root.find('./Custom/ReportOptions')
    
    all_measures = measurements.findall('./Measurement')
    all_analysis = analysis.findall('./ReportOption')
    
    for i in all_measures:
        if check_field(f'{i.get('Label')}_{status}'):
            value = i.find('ReportableValue').get('Value')
            # print(value)
            subject.data.append((status, f"{i.get('Label')}_{status}", value))
    for i in all_analysis:
        if check_field(f'{i.get('Label')}_{status}'):
            value = i.get('Value')
            # print(value)
            subject.data.append((status, f"{i.get('Label')}_{status}", value))
    
    for i in status_map:
        if i[0] == status:
            subject.data.append((status, i[1], 'True'))    
        elif i[0] != status and i[0] not in [f.split('_')[-1].strip('.xml') for f in subject.files]:
            subject.data.append((status, i[1], 'False'))

    subject.data.append((status, "Patient ID", subject.pt_id))
    
    return subject #in data as list of tuples
        
def create_subject(dataDir):
    """Generates unified patient object from data files in 'Data' using unique patient ID in naming scheme"""
    from modules.meta import Patient
    from os import listdir

    patients = [i.split('_')[0] for i in listdir(dataDir) if '.xml' in i]
        
    s = [Patient(i) for i in set(patients)]
    
    return s