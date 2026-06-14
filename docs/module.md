# {{ module | escape }}

```{eval-rst}
.. automodule:: {{ module }}
{% if module_doc %}
{{ module_doc }}
{% endif %}
{% for obj in objects %}
{% if obj.type == "class" %}

## {{ obj.name }}

```{eval-rst}
.. autoclass:: {{ obj.full_name }}
   :members:
   :undoc-members:
   :show-inheritance:
```
{% elif obj.type == "function" %}

## {{ obj.name }}

```{eval-rst}
.. autofunction:: {{ obj.full_name }}
```
{% endif %}
{% endfor %}
```
