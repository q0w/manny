FIELD_TEMPLATE = "{{ name }} = models.{{ type|title }}Field()"

DECIMAL_FIELD_TEMPLATE = "{{ name }} = models.{{ type }}Field(max_digits={{ max|default:'5' }}, decimal_places={{ " \
                         "places|default:'2' }}) "

CHAR_FIELD_TEMPLATE = "{{ name }} = models.{{ type }}Field(max_length={{max|default:'255'}})"

FOREIGN_KEY_TEMPLATE = '{{ name }} = models.{{ type }}Key({{ model|default:"\'self\'" }}, on_delete=models.{{ ' \
                       'delete|default:"CASCADE" }}) '

ONE_TO_ONE_FIELD_TEMPLATE = '{{ name }} = models.{{ type }}Field({{ model|default:"\'self\'" }}, on_delete=models.{{ ' \
                            'delete|default:"CASCADE" }}) '

MANY_TO_MANY_FIELD_TEMPLATE = '{{ name }} = models.{{ type }}Field({{ model|default:"\'self\'" }})'

MODEL_TEMPLATE = """
class {{ name }}(models.Model):{% for field in fields %}
    {{field}} {% endfor %}
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
"""

SERIALIZER_TEMPLATE = """
{% for key, value  in imports.items %}from {{ key }} import {{ value|join:", " }} 
{% endfor %}
{% for model in models %}
class {{ model }}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {{ model }}
        fields = '__all__'
        
{% endfor %}
"""
