from .models import Run, Relay, Competition

runs_queryset = Run.objects.all()

pre_runs = list(set([run.name for run in runs_queryset]))
runs = [(name, name) for name in pre_runs]  # distinct list of run names

pre_ages = list(set([run.age for run in runs_queryset]))
ages = [(age, age) for age in pre_ages]  # distinct list of ages, that apply to competition

pre_age_classes = ['Männer', 'Frauen', 'U23', 'U20', 'U18', '15', '14', 'U16', '13', '12', 'U14', '11', '10', 'U12',
                   '9', '8', 'U10', '7', '6', 'U8']
age_classes = [(age, age) for age in pre_age_classes]
#age_classes_whitespace = [("","")]
#age_classes_whitespace.extend(age_classes)

competitions_queryset = Competition.objects.all()
competitions = [(run.id, run.name) for run in competitions_queryset]
