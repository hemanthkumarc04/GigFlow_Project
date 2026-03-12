from django import template

register = template.Library()

@register.filter
def dual_currency(value):
    try:
        usd = float(value)
        inr = usd * 84.0
        return f"₹{inr:,.2f} (${usd:,.2f})"
    except (ValueError, TypeError):
        return value
