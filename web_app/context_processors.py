"""Context processor for metric unit system preference"""

METRIC = "metric"
IMPERIAL = "imperial"


def unit_system(request):
    """
    Inject unit system preference into every template context.
    Default is metric (liters/kg/Celsius) — India-first.
    Toggle stored in session.
    """
    system = request.session.get("unit_system", METRIC)
    return {
        "unit_system": system,
        "is_metric": system == METRIC,
    }
