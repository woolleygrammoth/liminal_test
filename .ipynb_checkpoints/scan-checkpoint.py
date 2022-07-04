from numpy import array

class Scan: 
    """
    An extendible structure to contain information from scans, 
    initialization: 
        waveforms: A list of lists containing 2-tuples. Each list contains all the data and metadata for a single waveform; 
                    each tuple in the waveform contains the field name and its associated value. 
        
        The attributes of this structure are: 
            data: numpy.array (the desired scan described by its constituent waveforms)
            test_id: str
            project_name: str
            timestamp: str
            exp_group: str
            serial_number: str
            sample_state: str
            n_rows: int
            n_columns: int
            row_spacing: float
            col_spacing: float
            score: float
            sample_rate: int
            
            these are all the fields that uniquely describe a scan;
            notice that individual waveform-specific fields have been excluded. 

        **extensions: to include new fields during initialization, do so using these kwargs
    """

    def __init__(self, waveforms: list, **extensions):
        scan_data = []
        for wave in waveforms: 
            data = wave.pop()[1] #extract waveform data as an array
            scan_data.append(data)
        self.data = array(scan_data)

        # prepare metadata for assigning to attributes
        field_dict = {}
        for field in waveforms[0]: #metadata comes from just the first waveform to eliminate redundancy
            field_dict.update({field[0]: field[1]})

        # drop unnecessary waveform-specific fields
        for field in ['delay', 'measurement_id', 'duration', 'position_x', 'position_y']: 
            field_dict.pop(field)
        for key, value in field_dict.items(): 
            setattr(self, key, value)

        # extend using kwargs
        for key, val in extensions.items(): 
            setattr(self, key, val)
        




