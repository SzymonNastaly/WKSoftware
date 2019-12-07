import json
from operator import itemgetter
from django.shortcuts import render, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.views import SuccessURLAllowedHostsMixin

from .models import Competition, Run, Relay
from .forms import RunForm, AddForm, EditForm, CustomLoginForm

# test
from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login
)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView


index_response_link = "<br><a href='http://localhost:8000/'>Zurück</a>"
kampfrichter_response_link = "<br><a href='http://localhost:8000/kampfrichter/'>Zurück</a>"
create_response_link = "<br><a href='http://localhost:8000/schiedsrichter/erstellung'>Zurück</a>"
editinglist_response_link = "<br><a href='http://localhost:8000/schiedsrichter/bearbeitung/'>Zurück</a>"


def is_schiedsrichter(user):
    if user.get_username() == "Schiedsrichter" or user.get_username() == "szymonnastaly":
        return True
    else:
        return False
#Todo: better implemetation

def index(request):
    return render(request, 'Kampfrichter/index.html')


@login_required
def kampfrichter(request):
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['lauf']
            sex = form.cleaned_data['geschlecht']
            age = form.cleaned_data['alter']
            number = int(form.cleaned_data['laufnummer'])
            try:
                run_id = Run.objects.get(name=name, sex=sex, age=age, number=number).id
            except Run.DoesNotExist:
                return HttpResponse("Kein Lauf mit diesen Eigenschaften gefunden" + kampfrichter_response_link)
            except Exception as ex:
                return HttpResponse("Unbekannter Fehler: " + str(ex) + kampfrichter_response_link)
            handoff_ready = form.cleaned_data['wechsel_bereit']
            violation = form.cleaned_data['verstoß_existent']

            relays_queryset = Relay.objects.all()
            relays = [relay.run.id for relay in relays_queryset]

            if run_id in relays:
                relay = Relay.objects.get(pk=run_id)
                relay.handoff_ready = handoff_ready
                relay.save()

            run = Run.objects.get(pk=run_id)
            run.violation = violation
            try:
                run.save()
            except Exception as ex:
                return HttpResponse("Unbekannter Fehler: " + str(ex) + kampfrichter_response_link)
            return HttpResponse("Erfolgreich abgesendet" + kampfrichter_response_link)
        else:
            return HttpResponse("Etwas ist schiefgegangen" + kampfrichter_response_link)
    else:
        relays_queryset = Relay.objects.all()
        relays = [relay.run.id for relay in relays_queryset]
        # names of all relays
        relays_names = [relay.run.name for relay in relays_queryset]
        relays_json = json.dumps(relays_names, cls=DjangoJSONEncoder)  # json necessary for javascript to read it
        runform = RunForm()

        # describes if a run has a violation (boolean)
        runs_queryset = Run.objects.all()
        runs_data = {run.name + run.sex + run.age + str(run.number): run.violation for run in runs_queryset}
        runs_data_json = json.dumps(runs_data, cls=DjangoJSONEncoder)

        # describes if a relay handoff is ready (boolean)
        relays_data = {relay.run.name + relay.run.sex + relay.run.age + str(relay.run.number): relay.handoff_ready
                       for relay in relays_queryset}
        relays_data_json = json.dumps(relays_data, cls=DjangoJSONEncoder)

        return render(request, 'Kampfrichter/kampfrichter.html',
                      {'runform': runform, 'relays': relays_json, 'runs_data': runs_data_json,
                       'relays_data': relays_data_json})



@login_required
def schiedsrichter(request):
    relays_queryset = Relay.objects.all()
    relays = [relay.run.id for relay in relays_queryset]

    def is_relay(run_id):
        if run_id in relays:
            return True
        else:
            return False

    runs_queryset = Run.objects.all()
    total_data = [{"id": run.id, "name": run.name, "sex": run.sex, "age": run.age, "number": run.number,
                   "violation": run.violation, "is_relay": is_relay(run.id)} for run in runs_queryset]
    s_total_data = sorted(total_data, key=itemgetter("sex", "age", "name", "number"))
    # total_data_json = json.dumps(total_data, cls=DjangoJSONEncoder)

    # describes if a relay handoff is ready (boolean)
    relays_data = {relay.run.id: relay.handoff_ready for relay in relays_queryset}
    relays_data_json = json.dumps(relays_data, cls=DjangoJSONEncoder)

    return render(request, 'Kampfrichter/schiedsrichter.html', {"total_data": s_total_data,
                                                                "relays_data": relays_data})


@login_required
@user_passes_test(is_schiedsrichter)
def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            competition_id = int(form.cleaned_data["wettkampf"])
            name = form.cleaned_data["name"]
            sex = form.cleaned_data["geschlecht"]
            age = form.cleaned_data["alter"]
            number = form.cleaned_data["anzahl"]
            ist_staffel = form.cleaned_data["ist_staffel"]
            for i in range(1, number + 1):
                run = Run(competition_id=competition_id, name=name, sex=sex, age=age, number=i)
                run.save()
                if ist_staffel:
                    relay = Relay(run=run)
                    relay.save()
            return HttpResponse("success" + create_response_link)
        else:
            return HttpResponse("Etwas ist schiefgegangen" + create_response_link)

    addform = AddForm()
    return render(request, 'Kampfrichter/erstellung.html', {'AddForm': addform})


@login_required
@user_passes_test(is_schiedsrichter)
def editinglist(request):
    runs_queryset = Run.objects.all()
    total_data = [{"id": run.id, "name": run.name, "sex": run.sex, "age": run.age, "number": run.number,
                   "violation": run.violation} for run in runs_queryset]
    s_total_data = sorted(total_data, key=itemgetter("sex", "age", "name", "number"))
    # total_data_json = json.dumps(total_data, cls=DjangoJSONEncoder)

    return render(request, 'Kampfrichter/liste.html', {"total_data": s_total_data})

@login_required
@user_passes_test(is_schiedsrichter)
def deleterun(request, runid):
    """Deletion method that gets triggered by the deletion button in the editing list"""
    try:
        run = Run.objects.get(pk=runid)
        run.delete()
    except:
        return HttpResponse("Etwas ist schiefgegangen" + editinglist_response_link)
    else:
        return HttpResponse("Erfolgreich gelöscht" + editinglist_response_link)


@login_required
@user_passes_test(is_schiedsrichter)
def specificrun(request, runid):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            relays_queryset = Relay.objects.all()
            relays = [relay.run.id for relay in relays_queryset]

            def relay_check(run_id):
                if run_id in relays:
                    return True
                else:
                    return False

            competition_id = form.cleaned_data['wettkampf']
            name = form.cleaned_data['name']
            sex = form.cleaned_data['geschlecht']
            age = form.cleaned_data['alter']
            is_relay = form.cleaned_data['ist_staffel']

            run = Run.objects.get(pk=runid)

            #comparing old to new values
            try:
                if run.competition_id != competition_id:
                    run.competition_id = int(competition_id)
                if run.name != name:
                    run.name = name
                if run.sex != sex:
                    run.sex = sex
                if run.age != age:
                    run.age = age
                    print("different age")
                if relay_check(run.id) != is_relay:
                    # create new relay and link to run or delete
                    if is_relay:
                        relay = Relay(run=run)
                        relay.save()
                    if not is_relay:
                        relay = Relay.objects.get(pk=run.id)
                        relay.delete()
                run.save()
            except:
                return HttpResponse("Etwas ist schief gegangen" + editinglist_response_link)
            return HttpResponse("Erfolgreich Werte verändert von Lauf: " + str(run) + editinglist_response_link)
        return HttpResponse("Etwas ist schiefgegangen" + editinglist_response_link)

    else:
        run = Run.objects.get(pk=runid)
        # for run info on top of page
        run_data = {"id": run.id, "name": run.name, "sex": run.sex, "age": "15", "number": run.number,
                "violation": run.violation}

        # detects if a run is a relay
        try:
            relayset = Relay.objects.get(run_id=runid)
        except ObjectDoesNotExist:
            is_relay = False
        else:
            is_relay = True
        #I know this implementation is horrible

        # for bound data in form
        editform = EditForm(initial={"wettkampf": run.competition_id,"name": run.name, "geschlecht": run.sex, "alter": run.age,
                                 "ist_staffel": is_relay})

        return render(request, 'Kampfrichter/run.html', {"run": run_data, 'EditForm': editform})


def logoutconfirmation(request):
    return HttpResponse("Erfolgreich ausgeloggt" + index_response_link)


# LoginRequired mixin doesnt work on first try - what should do?
class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    form_class = CustomLoginForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context
