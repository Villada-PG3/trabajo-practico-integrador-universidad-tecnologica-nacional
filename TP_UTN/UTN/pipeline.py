from django.db import IntegrityError

def create_alumno(strategy, details, user=None, social=None, *args, **kwargs):
    """
    Pipeline step: ensure an Alumno exists for the Django user.
    Runs after the User is created/found.
    """
    if user is None:
        return

    # import here to avoid app-loading issues
    from .models import Alumno

    # If the Alumno already exists, do nothing
    try:
        if hasattr(user, 'alumno'):
            return
    except Exception:
        # defensive: if related accessor isn't available, ignore and continue
        pass

    # Build basic values
    nombre = details.get('fullname') or f"{details.get('first_name','')} {details.get('last_name','')}".strip() or user.username
    email = details.get('email') or getattr(user, 'email', '')

    # Try to get picture or other extras if available (not required)
    picture = None
    if social is not None:
        extra = getattr(social, 'extra_data', {}) or {}
        picture = extra.get('picture')

    # Create or get the Alumno safely
    try:
        alumno, created = Alumno.objects.get_or_create(
            user=user,
            defaults={
                'nombre': nombre,
                'email': email,
            }
        )
    except IntegrityError:
        # fallback for race conditions or DB issues
        alumno = Alumno.objects.filter(user=user).first()

    # Optionally save picture into a known field if your model has one (not required)
    # if picture and hasattr(alumno, 'foto'):
    #     alumno.foto = picture
    #     alumno.save(update_fields=['foto'])

    return