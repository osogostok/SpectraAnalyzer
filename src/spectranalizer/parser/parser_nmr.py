import os
import zipfile
import numpy as np
import nmrglue as ng
import matplotlib.pyplot as plt
import shutil


class NMRSpectr():
    def __init__(self, zip_file_path):
        self.temp_folder = "./temp_extracted_data"
        self.zip_file_path = zip_file_path
        self.data_folder = None
        self.values_x = None
        self.values_y = None

        self.read_zip()
        self.precess_pdata()

    def read_zip(self):
        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            os.makedirs(self.temp_folder, exist_ok=True)
            zip_ref.extractall(self.temp_folder)
            archive_name = os.path.splitext(os.path.basename(self.zip_file_path))[
                0]
            self.extracted_folder = os.path.join(
                self.temp_folder, archive_name)

    def precess_pdata(self):
        for root, dirs, files in os.walk(self.extracted_folder):
            if "pdata" in dirs:
                pdata_folder = os.path.join(root, "pdata", "1")
                if os.path.isdir(pdata_folder):
                    dic, data = ng.bruker.read_pdata(
                        pdata_folder, scale_data=True)

                    udic = ng.bruker.guess_udic(dic, data)
                    uc = ng.fileiobase.uc_from_udic(udic)
                    ppm_scale = uc.ppm_scale()

                    self.values_x = ' '.join(map(str, data))
                    self.values_y = ' '.join(map(str, ppm_scale))

        shutil.rmtree(self.extracted_folder)
        if self.values_x is None or self.values_y is None:
            raise ValueError(
                "The data in the file does not match the expected data.")
