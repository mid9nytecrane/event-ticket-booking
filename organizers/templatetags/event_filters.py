from django import template 

register = template.Library()

@register.filter
def calculate_percentage(value, total):
    if total == 0:
        return 0
    try:
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError):
        return 0
    

@register.filter 
def format_percentage(value, total):
    if total == 0:
        return "0%"
    try:
        percentage =  (float(value) / float(total)) * 100 
        return f"{percentage:.0f}%"
    except (ValueError, TypeError):
        return "0%"
