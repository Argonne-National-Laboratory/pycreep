from pycreep import units

import numpy as np

class DataSet:
    """
        Superclass object providing a means to store and load data
        from a pandas dataframe

        Args:
            dataset:        data frame with data
    """
    def __init__(self, dataset):
        self.data = dataset
        self.fields = dict()

    def add_field_units(self, name, dname, dunits, ounits):
        """
            Add a field to the class, including unit conversion
            from the raw data

            Args:
                name:       field name
                dname:      name in data frame
                dunits:     units in data frame
                ounits:     output units
        """
        self.fields[name] = lambda self, dname=dname, dunits = dunits, ounits=ounits: units.convert(
                np.array(self.data[dname]), dunits, ounits)

    def add_heat_field(self, dname):
        """
            Add a standard field for the heat information and the map between
            the heat name and the corresponding indices

            Args:
                dname:      heat name in the dataset
        """
        self.fields["heats"] = lambda self, dname=dname: self.data[dname]
        self.heat_indices = {hi: self.heats.index[self.heats == hi] 
                for hi in set(self.heats)}
        
    def __getattr__(self, name):
        """
            Dynamically return the field with name

            Args:
                name:       field name
        """
        return self.fields[name](self)

