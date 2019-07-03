
class ImageData:
    '''Define Image Data class'''
    def __init__(self, uid='', folder='./'):

        self.image_id = uid
        self.filename = uid + '.png'
        self.folder = folder
        self.path = folder + self.filename
        # File information
        self.height = None     # int
        self.width = None      # int
        # Data information
        self.date_acquisition = None # datetime
        self.date_upload = None      # datetime
        self.observations = None     # Text field
        self.marks = None            # Text field
        self.patient_id = None       # Text field
        self.acquisition_data = None # Object
        self.us_type = None          # String
        # Annotations
        self.annotations = []
