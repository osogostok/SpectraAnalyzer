from .parser_nmr import NMRSpectr
from .parser_ir import IRSpectr
import os

def parser(file_name):
    file_extension = os.path.splitext(file_name)[1]
    print("FILE NAME ", file_name)
    if file_extension == '.zip': 
        nmr = NMRSpectr(file_name)
        return "NMR", nmr.values_x, nmr.values_y
    elif file_extension == '.xlsx':
        ir = IRSpectr(file_name)
        return "IR", ir.values_x, ir.values_y
    else:
        
        raise ValueError("Unknown file extension: {}".format(file_extension))
        
