from testimonials.models import Testimonial


def testimonial_context(request):
    testimonials = Testimonial.objects.filter(approved=True)

    context = {
        'testimonials': testimonials,
    }

    return context
