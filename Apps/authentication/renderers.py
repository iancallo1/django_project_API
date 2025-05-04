from rest_framework.renderers import BrowsableAPIRenderer

class ClearFormBrowsableAPIRenderer(BrowsableAPIRenderer):
    """
    Custom renderer that clears the form after successful POST requests
    """
    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type, renderer_context)
        request = renderer_context.get('request')
        response = renderer_context.get('response')
        
        if request and response and request.method == 'POST' and response.status_code in [200, 201]:
            context['raw_data_form'] = None
            
        return context 