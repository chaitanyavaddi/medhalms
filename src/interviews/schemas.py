from dataclasses import dataclass

from django.contrib import messages

from .models import Interview


@dataclass
class InterviewSchema:
    title:          str
    persona_prompt: str
    difficulty:     str
    max_duration:   int
    courses:        list
    questions:      list


    @classmethod
    def from_post(cls, request) -> "InterviewSchema":
        p = request.POST
        try:
            duration = int(p.get('max_duration', 30) or 30)
        except (ValueError, TypeError):
            duration = 30
        obj = cls(
            title          = p.get('title', '').strip(),
            persona_prompt = p.get('persona_prompt', '').strip(),
            difficulty     = p.get('difficulty', Interview.Difficulty.INTERMEDIATE),
            max_duration   = duration,
            courses        = p.getlist('courses'),
            questions      = [t.strip() for t in p.getlist('question_text') if t.strip()],
        )
        obj._request = request
        return obj

    def is_valid_title(self) -> bool:
        if not self.title:
            messages.error(self._request, 'Title is required.')
            return False
        return True

    def is_valid_persona(self) -> bool:
        if not self.persona_prompt:
            messages.error(self._request, 'Interviewer persona prompt is required.')
            return False
        return True

    def is_valid(self) -> bool:
        results = [self.is_valid_title(), self.is_valid_persona()]
        return all(results)
