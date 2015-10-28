import openpyxl as pxl

import formula_list as fl

formulas = fl.get_formula_list()

# Dictionary to contain formula counts.
spreadsheet_formula_counts = {}


def get_testing_vector(filename):
    # Initialize the formula counts to zero.
    for formula in formulas:
        spreadsheet_formula_counts[formula] = 0

    wb = pxl.load_workbook(filename)

    # Get the list of sheets in the workbook.
    sheet_names = wb.get_sheet_names()
    for sheet_name in sheet_names:
        sheet = wb.get_sheet_by_name(sheet_name)

        # Iterate over the cells.
        for row in sheet.iter_rows():
            for cell in row:
                cell_string = str(cell.value)
                if cell_string.startswith('='):
                    formula_string = cell_string[1:cell_string.index('(')]
                    spreadsheet_formula_counts[formula_string] += 1

    formula_count = []
    for formula in formulas:
        formula_count.append(spreadsheet_formula_counts[formula])

    return formula_count


def main():
    print get_testing_vector('Test.xlsx')
    return 0


if __name__ == '__main__':
    main()