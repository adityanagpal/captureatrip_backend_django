import PyPDF2
import io
import logging
from drf_extra_fields.fields import Base64FileField, Base64ImageField
from rest_framework.renderers import JSONRenderer

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Specifically for serializers
class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
        except PyPDF2.utils.PdfReadError as e:
            logger.warning(e)
        else:
            return 'pdf'

class CustomBase64ImageField(Base64ImageField):
    ALLOWED_TYPES = (
        "jpeg",
        "jpg",
        "png",
        "gif",
        "webp"
    )

# Custom renderer for custom json format in APIs
class ApiFormatRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        status_code = renderer_context['response'].status_code
        error_dict = {}

        # If http status code not 2**
        if not str(status_code).startswith('2'):

            """
            Descend into different nested data structures, pick first/relevant values
            """
            if isinstance(data, (list, tuple)):
                try:
                    error_dict["error_message"] = "".join(data)
                    data = error_dict
                except:
                    data["error_message"] = "Something went wrong"
                
            
            elif isinstance(data, dict):
                
                if 'messages' in data.keys():
                    data["error_message"] = data["messages"][0]["message"]
                elif 'detail' in data.keys():
                    data["error_message"] = data["detail"]
                else:                    
                    try:
                        # Return first value
                        data["error_message"] = "".join(next(iter(data.values())))
                    except TypeError:
                        # Return first value from nested structure
                        for value in data.values():
                            if isinstance(value, list): # nested dict
                                nested = value[0]
                                for val in nested.values():
                                    data["error_message"] = "".join(val)
                            elif isinstance(value, str): # not nested
                                data["error_message"] = "".join(value)
                            else: # ignore if more nested dict
                                data["error_message"] = "Something went wrong"
                            
                            break; # run loop only once
                    except:
                        data["error_message"] = "Something went wrong"
            
            elif isinstance(data, str):
                try:
                    data["error_message"] = data
                except:
                    data["error_message"] = "Something went wrong"

        return super(ApiFormatRenderer, self).render(data, accepted_media_type, renderer_context)