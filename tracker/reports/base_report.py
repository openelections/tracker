import csv
import pathlib
import os

class BaseReport:

    def __init__(self, outfile, data):
        self.outfile = outfile
        self.outdir = os.path.dirname(self.outfile)
        self.data = self._prepare_data(data)
        self.headers = self._headers(self.data)

    def write(self):
        pathlib.Path(self.outdir).mkdir(parents=True, exist_ok=True)
        with open(self.outfile, 'w') as csvfile:
            print("Data written to {}".format(self.outfile))
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

    def _prepare_data(self, data):
        "Customize data in subclasses as necessary"
        return data

    def _headers(self, data):
        "Customize headers in subclasss or default to keys from first data row"
        return data[0].keys()

