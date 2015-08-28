class {{model_name}}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{app_label}}_models.{{model_name}}
        fields = [{{model_fields}}]
