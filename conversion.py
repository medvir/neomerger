#!/usr/bin/env python3
''' Merges two NeoPrep log files into a single samplesheet
'''
import csv

# Creating a dictionary to be able to add "Sample_Well" for each sample
Adapters = {
    "ND006": "A", "ND013": "B", "ND012": "C", "ND014": "D", "ND005": "E",
    "ND015": "F", "ND019": "G", "ND021": "H", "ND001": "I", "ND010": "J",
    "ND020": "K", "ND008": "L", "ND025": "M", "ND011": "N", "ND018": "O",
    "ND023": "P", "ND002": "Q", "ND004": "R", "ND007": "S", "ND016": "T",
    "ND003": "U", "ND009": "V", "ND022": "W", "ND027": "X"
    }


def parse_sample_info(filename):
    ''' Reads from [Sample Information] to next separator
    '''
    ret_lines = []
    with open(filename) as f:
        parsing = False
        for l in f:
            if l.startswith('[Sample Information]'):
                parsing = True
            if parsing and l.strip() == '':
                break
            if parsing and not l.startswith('Start'):
                ret_lines.append(l.strip().split())
    return ret_lines[1:]


def merge(logfile_1=None, logfile_2=None, MSNumber=None,
          InvestigatorName='Stefan Schmutz',
          ExperimentName='Test', Date=None, Description='Test description',
          Reads='51'):
    '''Parse indices and writes samplesheet'''

    used_indices = []

    # SampleSheet for MiSeq without any samples
    with open(MSNumber, 'w') as csvfile:
        cw = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writerow(['[Header]'] + [None] * 7)
        cw.writerow(['IEMFileVersion', '4'] + [None] * 6)
        cw.writerow(['Investigator Name', InvestigatorName] + [None] * 6)
        cw.writerow(['Experiment Name', ExperimentName] + [None] * 6)
        cw.writerow(['Date', Date] + [None] * 6)
        cw.writerow(['Workflow', 'GenerateFASTQ'] + [None] * 6)
        cw.writerow(['Application', 'FASTQ Only'] + [None] * 6)
        cw.writerow(['Assay', 'TruSeq LT'] + [None] * 6)
        cw.writerow(['Description', Description] + [None] * 6)
        cw.writerow(['Chemistry', 'Default'] + [None] * 6)
        cw.writerow([None] * 8)
        cw.writerow(['[Reads]'] + [None] * 7)
        cw.writerow([Reads] + [None] * 7)
        cw.writerow([None] * 8)
        cw.writerow(['[Settings]'] + [None] * 7)
        cw.writerow(['ReverseComplement', '0'] + [None] * 6)
        cw.writerow(['Adapter',
                     'AGATCGGAAGAGCACACGTCTGAACTCCAGTCA'] + [None] * 6)
        cw.writerow(['AdapterRead2',
                     'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT'] + [None] * 6)
        cw.writerow([None] * 8)

        # Here start the [Data] rows
        cw.writerow(['[Data]'] + [None] * 7)
        cw.writerow(['Sample_ID', 'Sample_Name', 'Sample_Plate', 'Sample_Well',
                     'I7_Index_ID', 'index', 'Sample_Project', 'Description'])

        # The second part of the script opens the NeoPrep .log file,
        # reads the Sample_ID, _Name, I7_Index_ID and index-sequence and writes
        # it to the SampleSheet
        ret_1 = parse_sample_info(logfile_1)
        for n, r in enumerate(ret_1):
            assert int(r[0]) == n + 1
            Sample_ID = n + 1
            Sample_Name = r[2]
            I7_Index_ID = r[3]
            used_indices.append(I7_Index_ID)
            index = r[5]
            cw.writerow([Sample_ID, Sample_Name, None, Adapters[I7_Index_ID],
                         I7_Index_ID, index, None, None])

        # The third part adds all samples from another NeoPrep run which
        # indices are not used already
        ret_2 = parse_sample_info(logfile_2)
        for n2, r in enumerate(ret_2):
            assert int(r[0]) == n2 + 1, 'Missing samples'
            Sample_ID = n + n2 + 2  # n + 1 + n2 + 1
            Sample_Name = r[2]
            I7_Index_ID = r[3]
            index = r[5]
            if I7_Index_ID in used_indices:
                continue
            cw.writerow([Sample_ID, Sample_Name, None, Adapters[I7_Index_ID],
                         I7_Index_ID, index, None, None])


def parse_indices(logfile_1=None, logfile_2=None):
    '''Only parse indices'''

    used_indices_1 = []
    used_indices_2 = []

    # The second part of the script opens the NeoPrep .log file,
    # reads the Sample_ID, _Name, I7_Index_ID and index-sequence and writes
    # it to the SampleSheet
    ret_1 = parse_sample_info(logfile_1)
    for n, r in enumerate(ret_1):
        assert int(r[0]) == n + 1
        #Sample_ID = n + 1
        #Sample_Name = r[2]
        I7_Index_ID = r[3]
        used_indices_1.append(I7_Index_ID)
        #index = r[5]

    # The third part adds all samples from another NeoPrep run which
    # indices are not used already
    ret_2 = parse_sample_info(logfile_2)
    for n2, r in enumerate(ret_2):
        assert int(r[0]) == n2 + 1, 'Missing samples'
#        Sample_ID = n + n2 + 2  # n + 1 + n2 + 1
#        Sample_Name = r[2]
        I7_Index_ID = r[3]

#        index = r[5]
        if I7_Index_ID in used_indices_1:
            continue
        used_indices_2.append(I7_Index_ID)
    return used_indices_1, used_indices_2
