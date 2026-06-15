from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View

from .career_paths_data import (
    ALL_ROADMAPS, DEFAULT_ROLE_ID, DEFAULT_SKILL_ID,
    ROLE_GROUPS, ROLE_IDS, SKILL_GROUPS,
)


def _thread_groups(groups):
    return [
        {"label": g["label"], "items": [{"id": i["id"], "name": i["name"]} for i in g["items"]]}
        for g in groups
    ]


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'dashboard/home.html')


class CareerPathsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, roadmap_id=None, tab=None):
        if roadmap_id:
            roadmap = ALL_ROADMAPS.get(roadmap_id)
            if not roadmap:
                raise Http404
            # Infer tab from which set the id belongs to
            active_tab = 'skills' if roadmap_id not in ROLE_IDS else 'roles'
        else:
            active_tab = tab or 'roles'
            default_id = DEFAULT_SKILL_ID if active_tab == 'skills' else DEFAULT_ROLE_ID
            roadmap = ALL_ROADMAPS[default_id]

        # HTMX partial — return only the detail panel
        if request.headers.get('HX-Request'):
            response = render(request, 'dashboard/career_path_detail.html', {'role': roadmap})
            response['Cache-Control'] = 'no-store'
            return response

        groups = SKILL_GROUPS if active_tab == 'skills' else ROLE_GROUPS
        return render(request, 'dashboard/career_paths.html', {
            'active_role': roadmap,
            'thread_groups': _thread_groups(groups),
            'tab': active_tab,
        })
