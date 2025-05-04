from rest_framework.renderers import BrowsableAPIRenderer

class ClearFormBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type, renderer_context)
        request = renderer_context['request']
        
        # Clear form data after successful POST
        if request.method == 'POST' and renderer_context['response'].status_code in [200, 201]:
            context['raw_data_form'] = None
            
        return context 