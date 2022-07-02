from rest_framework import serializers


class HandleAdditionalValidationMessage(object):
    def __init__(self, blank_message=None, **kwargs):
        super().__init__(**kwargs)
        if blank_message:
            self.error_messages["blank"] = blank_message


class IMCharField(HandleAdditionalValidationMessage, serializers.CharField):
    pass


class IMEmailField(HandleAdditionalValidationMessage, serializers.EmailField):
    pass
