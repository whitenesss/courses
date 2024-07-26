from rest_framework.serializers import ValidationError


class LinkToVideoValidator:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, value):
        field_value = value.get(self.fields)

        if not field_value.startswith("https://www.youtube.com/"):
            raise ValidationError('Invalid URL')

