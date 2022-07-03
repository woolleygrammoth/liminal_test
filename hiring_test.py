import sqlite3
import io
import json
from pprint import pprint
import numpy as np

from scan import Scan

class LocalDB:
    def __init__(self, fname="hiring_test.db"):
        self._register_adapters()
        self.fname = str(fname)

    def _execute(self, sql, args=None):
        """
        General sql execute. Pass it an sqlite3 string and optional list of args
        and it will return an iterable cursor
        """

        with sqlite3.connect(self.fname, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            conn.execute("PRAGMA journal_mode = wal")
            cursor = conn.cursor()
            if args:
                return cursor.execute(sql, args)
            else:
                return cursor.execute(sql)

    def _register_adapters(self):
        """
        We use a "custom" ARRAY colum. This function defines
        how we convert the the values in this column to and from Python data types.

        ARRAY is a byte-for-byte representation of a numpy array stored as BLOB.
        It is predictably read into Python as a `numpy.ndarray`.
        """

        ###########################################
        # register numpy array adapter
        ###########################################

        def adapt_array(arr):
            out = io.BytesIO()
            np.save(out, arr)
            out.seek(0)
            return sqlite3.Binary(out.read())

        def convert_array(text):
            out = io.BytesIO(text)
            out.seek(0)
            return np.load(out)

        sqlite3.register_adapter(np.ndarray, adapt_array)
        sqlite3.register_converter("ARRAY", convert_array)

    def fetch_data(self, **kwargs) -> list: 
        """
            Returns a list of scans from the database filtered by the kwargs. Potential kwargs include: 
            - `serial_number: str` Return data where `tests.serial_number` is equal to this value
            - `project_name: str` Return data where `tests.project_name` is equal to this value
            - `before: str` Only return values with `timestamp` below (before) this value.
            - `after: str` Only return values with `timestamp` above (after) this value.
                - the `before` and `after` kwargs must be formatted as such: 'YYYY-MM-DD HH-MM-SS.FFFFFF'
            - `limit: int` Return at most this many entries
        """
        # construct the proper query
        query = 'SELECT * FROM tests '
        conditions = []
        limit = None
        for field, val in kwargs.items(): 
            if field == 'serial_number': 
                conditions.append(f'serial_number="{val}"')
            elif field == 'project_name': 
                conditions.append(f'project_name="{val}"')
            elif field == 'before': 
                conditions.append(f'timestamp<="{val}"')
            elif field == 'after': 
                conditions.append(f'timestamp>="{val}"')
            elif field == 'limit': 
                limit = val
            
        if conditions: 
            query += 'WHERE ' + ' AND '.join(conditions) + ' '
        query += ';'
        
        cursor = self._execute(query)
        col_names = [x[0] for x in cursor.description]
        
        # group results by test_id, i.e. according to which scan they belong to
        cursor_list = [row for row in cursor] # to deal with the fact that cursor can only be consumed once
        all_test_ids = [row[1] for row in cursor_list]
        unique_test_ids = set(all_test_ids)
        grouped_waveforms = []
        for value in unique_test_ids: 
            current_group = []
            for row in cursor_list: 
                if row[1] == value: 
                    labeled_data = [(key, val) for key, val in zip(col_names, row)]
                    current_group.append(labeled_data)
            grouped_waveforms.append(current_group)
        
        # create a scan for each group 
        scans = []
        for group in grouped_waveforms: 
            scans.append(Scan(group))

        #return the possibly limited number of scans
        if limit: 
            scans = scans[:limit]
        return scans

    def test_counts(self) -> list: 
        """
        This method will return a `list` where each element is a tuple of two elements:
            - A distinct `project_name`
            - A count of `test_ids that fall under that project.
        Note: this method will return a count of unique waveforms that fall under each project, 
                not a count of scans, each of which may contain many waveforms. 
        """
        query = 'SELECT project_name, COUNT(*) FROM tests GROUP BY project_name'
        cursor = self._execute(query)
        counts = []
        for row in cursor: 
            counts.append(row)
        return counts

            




# some quick usage examples.

if __name__ == "__main__":
    # instantiate
    db = LocalDB()

    print("## show table counts ##")
    print(list(db._execute("SELECT count(*) FROM tests;")))
    print("## ##\n")

    print("## matching columns to names, seeing the info ##")
    cursor = db._execute("SELECT * FROM tests LIMIT 1;")
    col_names = [x[0] for x in cursor.description]
    data = [{col: val for col, val in zip(col_names, row)} for row in cursor]
    pprint(data)
    print("## ##\n")

    # test new methods
    kwargs = {'limit': 2, 'timestamp': '2021-11-16 13:14:37.764268-08:00'}
    db.fetch_data(**kwargs)
    # print(db.test_counts())