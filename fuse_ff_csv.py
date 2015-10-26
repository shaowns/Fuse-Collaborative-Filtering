import json
import csv

# Import stuff from other files.
import formula_list

formulas = formula_list.get_formula_list()

fuse_json_file_name = 'fuse-bin.analysis.dedup.poi-dec2014.json'
csv_output_file = 'fuse_formula_count.csv'


def process_json_metadata():
    output_file = open(csv_output_file,'w+')
    csv_writer = csv.writer(output_file, dialect='excel')

    with open(fuse_json_file_name, 'r') as fd:
        # IMPORTANT: One json record per line, not an array of json objects.
        for line in fd:
            json_record = json.loads(line)

            record_total = 0
            formula_counts = []
            for formula in formulas:
                key = 'count' + formula
                if key in json_record['POI']:
                    count = int(json_record['POI'][key])
                    record_total += count
                    formula_counts.append(count)
                else:
                    formula_counts.append(0)

                # Exclude the records that does not have any usage from the instance set.
            if record_total > 0:
                csv_writer.writerow(formula_counts)

    output_file.close()


def main():
    process_json_metadata()
    return 0

if __name__ == '__main__':
    main()