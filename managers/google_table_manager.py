"""This file contains a GoogleTableManager implementation to work with Google
 spreadsheets"""
import gspread
from gspread import Spreadsheet
from constants import PARSE_SHEET, URL_COLUMN
# -------------------------------------------------------------------------


class GoogleTableManager:
    """This class provides functionality to work with Google Spreadsheets"""
    def __init__(self, auth_file: str, table_name: str) -> None:
        """Initialize the GoogleTableManager class
        :param auth_file: The path to the file with authentication information
        :param table_name: The name of the Google table to work with
        """
        self._connection = gspread.service_account(auth_file)
        self._table = self._open_table(table_name)

    def _open_table(self, table_name: str) -> Spreadsheet:
        """This closed method serves to open the Google table
        :param table_name: The name of the Google table
        :return: A Spreadsheet object
        """
        try:
            table = self._connection.open(table_name)
            return table
        except gspread.GSpreadException as e:
            print(f"Unable to open table, the error: {e}")

    def get_by_column(
            self, sheet_name: str = PARSE_SHEET, col_num: int = URL_COLUMN
    ) -> list[str] | None:
        """This method returns a list of lists representing sheet columns
        :param sheet_name: The name of the Google sheet
        :param col_num: The column number
        :return: A list of lists representing the columns of the Google sheet
        """
        try:
            result = self._table.worksheet(sheet_name).col_values(col_num)

        except gspread.GSpreadException as e:
            print(f"Unable to get column value, the error: {e}")
            result = None

        return result

    def upload_to_sheet(
            self,  col_range: str, data: list[list],
            sheet_name: str = PARSE_SHEET,) -> None:
        """This method upload the data to the chosen Google sheet
        :param sheet_name: The name of the Google sheet
        :param col_range: The range of columns in the Google sheet (for
        example: A2:B10 - uploads data to columns A2-B2, A3-B3 ...A10-B10)
        :param data: The data to upload
        """
        try:
            self._table.worksheet(sheet_name).update(col_range, data)

        except gspread.GSpreadException as e:
            print(f"Unable to upload data, the error: {e}")
