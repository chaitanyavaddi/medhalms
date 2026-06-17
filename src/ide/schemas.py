from dataclasses import dataclass

from django.contrib import messages

from .lab_options import ALL_OPTIONS


@dataclass
class LabCreateSchema:
    name:     str
    oc_slug:  str
    category: str

    @classmethod
    def from_post(cls, request) -> "LabCreateSchema":
        p = request.POST
        obj = cls(
            name     = p.get('name', '').strip(),
            oc_slug  = p.get('oc_slug', '').strip(),
            category = p.get('category', '').strip(),
        )
        obj._request = request
        return obj

    def is_valid_name(self) -> bool:
        if not self.name:
            messages.error(self._request, 'Lab name is required.')
            return False
        if len(self.name) > 100:
            messages.error(self._request, 'Lab name must be 100 characters or fewer.')
            return False
        return True

    def is_valid_language(self) -> bool:
        if not self.oc_slug or self.oc_slug not in ALL_OPTIONS:
            messages.error(self._request, 'Please select a language to continue.')
            return False
        if self.category not in ('language', 'web', 'database'):
            messages.error(self._request, 'Invalid category.')
            return False
        return True

    def is_valid(self) -> bool:
        results = [self.is_valid_name(), self.is_valid_language()]
        return all(results)
