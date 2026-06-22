from .lab_options import ALL_OPTIONS
from .models import Lab


class LabService:
    @staticmethod
    def get_user_labs(user):
        return Lab.objects.filter(user=user, is_embed=False)

    @staticmethod
    def create_lab(user, schema, is_embed=False) -> Lab:
        option = ALL_OPTIONS[schema.oc_slug]
        return Lab.objects.create(
            user        = user,
            name        = schema.name,
            language    = option['name'],
            oc_slug     = schema.oc_slug,
            category    = schema.category,
            logo_domain = option['logo_domain'],
            is_embed    = is_embed,
        )

    @staticmethod
    def save_code(lab: Lab, code: str) -> None:
        lab.code = code
        lab.save(update_fields=['code', 'updated_at'])
