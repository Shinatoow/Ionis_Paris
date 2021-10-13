import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Sheets:
    """
    This class is used to ease the use of google sheet API.
    It requires a credentials.json file stored in the config folder.
    By default it will look for a sheet called "B12-ionis"
    """
    def __init__(self, name):
        """
        :name: the name of the worksheet
        """
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"
                 ]
        self.name = name
        credentials = ServiceAccountCredentials.from_json_keyfile_name("b12-ionis-cred.json", scope)
        client = gspread.authorize(credentials)
        # sheet = client.open("B12-ionis").sheet1
        self.client = client
        sheet = client.open("B12-ionis").worksheet(name)
        self.sheet = sheet

    def get_all_data(self):
        """
        Return all the data currently stored in the worksheet
        :return: An array containing a tuple by column
        """
        return self.sheet.get_all_records()

    def get_row(self, row_id):
        """
        This function will return the data contain in row_id row
        :row_id: Row name
        """
        return self.sheet.row_values(row_id)

    def get_col(self, col_id):
        """
        This function will return the data contain in column_id column
        :col_id: Column name
        """
        return self.sheet.col_values(col_id)

    def push(self, *args):
        """
        This function will create a row and push it to the google sheet
        """
        row = []
        for e in args:
            row.append(e)
        self.sheet.append_row(row)

