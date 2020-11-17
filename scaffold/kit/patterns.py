FIELD_TEMPLATE = "$name = models.${type}Field()"

DECIMAL_FIELD_TEMPLATE = "$name = models.${type}Field(max_digits=${max}, decimal_places=${places})"

CHAR_FIELD_TEMPLATE = "$name = models.${type}Field(max_length=${max})"

MODEL_TEMPLATE = """
class ${name}(models.Model):
    ${field}
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
"""

LIST_VIEW_TEMPLATE = """
class ${name}ListView(ListView):
    model = $name
    template_name = '${name}_list.html'
"""
