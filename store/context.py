from .models import Cart, SiteConfig
from .phase2 import current_customer
from .services import vnd


def shop(request):
    count = 0
    if request.session.session_key:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if cart:
            count = sum(line.qty for line in cart.lines.all())
    config = SiteConfig.load()
    return {
        "cart_count": count,
        "site_config": config,
        "hotline_digits": "".join(ch for ch in config.hotline if ch.isdigit()),
        "vnd": vnd,
        "customer": current_customer(request),
    }
