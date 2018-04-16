from rest_framework import serializers


class MdmBaseSerializer(serializers.ModelSerializer):

    def get_resource_type(self, obj):
        return self.Meta.model.__name__