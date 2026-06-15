from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views import View

from .career_paths_data import ALL_ROLES, CAREER_TRACKS, DEFAULT_ROLE_ID


def _build_thread_groups(tracks):
    return [
        {"label": t["label"], "items": [{"id": r["id"], "name": r["name"]} for r in t["roles"]]}
        for t in tracks
    ]


class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'dashboard/home.html')


class CareerPathsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, role_id=None):
        if role_id:
            active_role = ALL_ROLES.get(role_id)
            if not active_role:
                raise Http404
        else:
            active_role = ALL_ROLES[DEFAULT_ROLE_ID]

        # HTMX partial — return only the detail panel
        if request.headers.get('HX-Request'):
            return render(request, 'dashboard/career_path_detail.html', {
                'role': active_role,
            })

        return render(request, 'dashboard/career_paths.html', {
            'active_role': active_role,
            'thread_groups': _build_thread_groups(CAREER_TRACKS),
        })
