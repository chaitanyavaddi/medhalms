import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from utils.view_helper import htmx, redirect_to

from .lab_options import DATABASE_OPTIONS, LANGUAGE_OPTIONS, WEB_OPTIONS
from .models import Lab
from .schemas import LabCreateSchema
from .service import LabService

OC_PARAMS = (
    "hideLanguageSelection=true&hideRun=true&hideNew=true&hideTitle=true"
    "&hideEditorOptions=true&hideNewFileOption=true&listenToEvents=true"
    "&codeChangeEvent=true&theme=dark"
)


def _embed_url(lab):
    return f"https://onecompiler.com/embed/{lab.oc_slug}?{OC_PARAMS}"


class CodingLabsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, lab_id=None):
        labs = LabService.get_user_labs(request.user)
        active_lab = None
        if lab_id:
            active_lab = get_object_or_404(Lab, id=lab_id, user=request.user)
        elif labs.exists():
            active_lab = labs.first()
        if htmx(request) and lab_id:
            response = render(request, 'ide/lab_detail.html', {
                'lab': active_lab,
                'embed_url': _embed_url(active_lab),
            })
            response['Cache-Control'] = 'no-store'
            return response
        return render(request, 'ide/main.html', {
            'labs': labs,
            'active_lab': active_lab,
            'embed_url': _embed_url(active_lab) if active_lab else None,
            'language_options': LANGUAGE_OPTIONS,
            'web_options': WEB_OPTIONS,
            'database_options': DATABASE_OPTIONS,
        })


class LabCreateModalView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'ide/new_lab_modal.html', {
            'language_options': LANGUAGE_OPTIONS,
            'web_options': WEB_OPTIONS,
            'database_options': DATABASE_OPTIONS,
            'data': {},
        })


class LabCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request):
        schema = LabCreateSchema.from_post(request)
        if not schema.is_valid():
            return render(request, 'ide/new_lab_modal.html', {
                'data': request.POST,
                'language_options': LANGUAGE_OPTIONS,
                'web_options': WEB_OPTIONS,
                'database_options': DATABASE_OPTIONS,
            })
        lab = LabService.create_lab(request.user, schema)
        return redirect_to(request, reverse('ide:lab', args=[lab.id]))


class LabSaveView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, lab_id):
        lab = get_object_or_404(Lab, id=lab_id, user=request.user)
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Bad request'}, status=400)
        files = data.get('files', [])
        if isinstance(files, list) and files:
            LabService.save_code(lab, json.dumps(files))
        return JsonResponse({'ok': True})


class LabDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, lab_id):
        lab = get_object_or_404(Lab, id=lab_id, user=request.user)
        lab.delete()
        return redirect_to(request, reverse('ide:index'))
