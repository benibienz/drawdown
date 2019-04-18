"""Reads Variable Meta Analysis tab

   The code in this file is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE
   version 3.0.

   Outputs of this utility are considered to be data and do not automatically
   carry the license used for the code in this utility. It is up to the user and
   copyright holder of the inputs to determine what copyright applies to the
   output.
"""

import os
import pathlib
import pandas as pd
from numpy import nan
from collections import OrderedDict
from tools.util import cell_to_offsets, empty_to_nan, to_filename, convert_bool

CSV_TEMPLATE_PATH = pathlib.Path(__file__).parents[1].joinpath('data', 'VMA', 'vma_template.csv')
pd.set_option('display.expand_frame_repr', False)

# dtype conversion map
COLUMN_DTYPE_MAP = {
    'SOURCE ID: Author/Org, Date, Info': lambda x: x,
    'Link': lambda x: x,
    'World / Drawdown Region': lambda x: x,
    'Specific Geographic Location': lambda x: x,
    'Thermal-Moisture Regime': lambda x: x,
    'Source Validation Code': lambda x: x,
    'Year / Date': lambda x: int(x) if x is not nan else x,
    'License Code': lambda x: x,
    'Raw Data Input': lambda x: float(x) if x is not nan else x,
    'Original Units': lambda x: x,
    'Conversion calculation': lambda x: float(x) if x is not nan else x,
    'Common Units': lambda x: x,
    'Weight': lambda x: x,
    'Assumptions': lambda x: x,
    'Exclude Data?': lambda x: convert_bool(x) if x is not nan else x,
}


def make_vma_df_template():
    """
    Helper function that generates a DataFrame with the same columns as the tables in
    the xls solution Variable Meta Analysis. This is the correct DataFrame format to
    input to the VMA python class. A researcher can thus use this function to create
    a new VMA table in python to populate with data if they want.
    """
    df = pd.read_csv(CSV_TEMPLATE_PATH, index_col=False, skipinitialspace=True, skip_blank_lines=True, comment='#')
    return df


class VMAReader:
    def __init__(self, wb):
        """
        xls_path: path to solution xls file
        """
        self.wb = wb
        self.df_template = make_vma_df_template()

    def read_xls(self, csv_path=None, alt_vma=False):
        """
        Reads the whole Variable Meta-analysis xls sheet.
        Note this currently only works for LAND solutions.
        csv_path: (pathlib path object or str) If specified, will write CSVs to path for each table
        alt_vma: False = process the primary VMA sheet 'Variable Meta-analysis',
                 True = process the alternate VMA sheet 'Variable Meta-analysis-DD' with fixed
                    values for Average, High, and Low.
        """
        if alt_vma:
            sheetname = 'Variable Meta-analysis-DD'
            fixed_summary = True
        else:
            sheetname = 'Variable Meta-analysis'
            fixed_summary = False

        self._find_tables(sheetname=sheetname)
        df_dict = OrderedDict()
        for title, location in self.table_locations.items():
            df, use_weight, summary = self.read_single_table(source_id_cell=location,
                    sheetname=sheetname, fixed_summary=fixed_summary)
            if df.empty:  # in line with our policy of setting empty tables to None
                df_dict[title] = (None, False, (nan, nan, nan))
            else:
                df_dict[title] = (df, use_weight, summary)

        if csv_path is not None:
            idx = pd.Index(data=list(range(1, len(df_dict) + 1)), name='VMA number')
            info_df = pd.DataFrame(columns=['Filename', 'Title on xls', 'Has data?', 'Use weight?',
                'Fixed Mean', 'Fixed High', 'Fixed Low'], index=idx)
            i = 1
            for title, values in df_dict.items():
                table = values[0]
                use_weight = values[1]
                (average, high, low) = values[2]
                path_friendly_title = to_filename(title)
                row = {'Filename': path_friendly_title, 'Title on xls': title,
                       'Has data?': False if table is None else True,
                       'Use weight?': use_weight,
                       'Fixed Mean': average, 'Fixed High': high, 'Fixed Low': low}
                info_df.loc[i, :] = row
                i += 1
                if table is not None:
                    table.to_csv(os.path.join(csv_path, path_friendly_title + '.csv'), index=False)
            info_df.to_csv(os.path.join(csv_path, 'VMA_info.csv'))
        return df_dict

    def normalize_col_name(self, name):
        """Substitute well-known names for variants seen in some solutions."""
        known_aliases = {
                'Manually Exclude Data?': 'Exclude Data?',
                'Manually Excluded?': 'Exclude Data?',
                'Weight by: Production': 'Weight',
                # someone did a global replace of 'version' with 'edition' in Conservation Ag.
                'Conedition calculation': 'Conversion calculation',
        }
        return known_aliases.get(name, name)

    def read_single_table(self, source_id_cell, sheetname, fixed_summary):
        """
        Reads a single Variable Meta-analysis table (e.g. Current Adoption).
        source_id_cell: xls location or offsets of SOURCE ID cell of table
        (e.g. 'C48' or cell_to_offsets('C48'), where C48 is the cell that starts 'SOURCE ID...')

        sheetname: typically 'Variable Meta-analysis' or 'Variable Meta-analysis-DD'
        fixed_summary: whether Average, High, and Low are fixed values to be extracted from Excel.
        """
        sheet = self.wb.sheet_by_name(sheetname)
        df = self.df_template.copy(deep=True)
        if isinstance(source_id_cell, str):  # for convenience + testing
            row1, col1 = cell_to_offsets(source_id_cell)
        else:  # for use with read_xls
            row1, col1 = source_id_cell
        max_sources = 86
        for r in range(max_sources):
            new_row = {}
            for c in range(15):
                if c == 14:
                    c += 1  # There is a blank column before the "Exclude Data?" column
                col_name = df.columns[c] if c != 15 else df.columns[-1]
                if r == 0:  # check col name before proceeding
                    first_cell = sheet.cell_value(row1, col1 + c)
                    name_to_check = self.normalize_col_name(first_cell.strip().replace('*', ''))
                    assert name_to_check == col_name, 'cell value: {} is not {}'.format(first_cell, col_name)
                cell_val = sheet.cell_value(row1 + 1 + r, col1 + c)  # get raw val
                cell_val = COLUMN_DTYPE_MAP[col_name](empty_to_nan(cell_val))  # conversions
                new_row[col_name] = cell_val
            if all(pd.isna(v) for k, v in new_row.items() if k not in ['Common Units', 'Weight']):
                last_row = r
                break  # assume an empty row (except for Common Units) indicates no more sources to copy
            else:
                df = df.append(new_row, ignore_index=True)
        else:
            raise Exception(
                'No blank row detected in table. Either there are {}+ VMAs in table, the table has been misused '
                'or there is some error in the code. Cell: {}'.format(max_sources, source_id_cell))
        if (df['Weight'] == 0).all():
            # Sometimes all weights are set to 0 instead of blank. In this case we want them to be NaN.
            df['Weight'] = df['Weight'].replace(0, nan)

        for r in range(last_row, last_row + 50):  # look past last row
            if sheet.cell_value(row1 + r, 18) == 'Use weight?':
                use_weight = convert_bool(sheet.cell_value(row1 + r + 1, 18))
                break
        else:
            raise ValueError("No 'Use weight?' cell found")

        if fixed_summary:
            # Find the Average, High, Low cells.
            for r in range(last_row, last_row + 50):
                if 'average' in str(sheet.cell_value(row1 + r, 17)).lower():
                    col = 19 if use_weight else 18
                    average = float(sheet.cell_value(row1 + r, col))
                    high = float(sheet.cell_value(row1 + r + 1, col))
                    low = float(sheet.cell_value(row1 + r + 2, col))
                    break
            else:
                raise ValueError(f"No 'Average' cell found for {source_id_cell}")
        else:
            average = high = low = nan

        return df, use_weight, (average, high, low)

    def _find_tables(self, sheetname):
        """
        Finds locations of all tables from the Variable Meta-analysis tab. They are not
        evenly spaced due to missing or extra rows, so to be safe we comb the following
        N rows from each table title. We also comb 10 rows ahead of each title to find
        the SOURCE ID cell, as this is also a varying spacing.

        Arguments:
            sheetname: name of the Excel Sheet. Some solutions use 'Variable Meta-analysis',
                some use 'Variable Meta-analysis-DD'.
        """

        table_locations = OrderedDict()
        sheet = self.wb.sheet_by_name(sheetname)
        row, col = 40, 2
        for table_num in range(1, 36):
            found = False
            for rows_to_next_table in range(200):
                title_from_cell = sheet.cell_value(row + rows_to_next_table, col)
                # print(title_from_cell)
                if title_from_cell.startswith('VARIABLE'):
                    # if the table has a generic VARIABLE title we assume there are no more variables to record
                    self.table_locations = table_locations
                    return  # search for tables ends here
                elif not title_from_cell:
                    continue

                # rather than recording titles we will check for vma number. We need to validate both the number and
                # ensure that the column where "common units" would be is empty, as the number alone is not enough
                # to uniquely identify a title row (table rows are also numbered)
                table_num_on_sheet = sheet.cell_value(row + rows_to_next_table, col - 2)
                common_units_check = not sheet.cell_value(row + rows_to_next_table, col + 11)
                if table_num_on_sheet == table_num and common_units_check:  # i.e. if title cell of table
                    for space_after_title in range(10):
                        offset = rows_to_next_table + space_after_title
                        if sheet.cell_value(row + offset, col) == 'SOURCE ID: Author/Org, Date, Info':
                            table_locations[title_from_cell] = (row + offset, col)
                            row += offset
                            found = True
                            # print('----------------------------FOUND {}'.format(title_from_cell))
                            break
                    else:
                        raise Exception('Cannot find SOURCE ID cell for {}'.format(title_from_cell))
                if found:
                    break
            else:
                print(table_locations)
                raise Exception('Cannot find table number {}'.format(table_num))
        self.table_locations = table_locations
