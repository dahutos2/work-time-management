from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import SignUpForm, BS4ScheduleForm
from .models import User, Worktime
from django.urls import reverse_lazy
import datetime
from django.shortcuts import redirect
from django.views import generic
from . import mixins
from .forms import BS4ScheduleForm, SearchForm
from django.http import HttpResponse

# Create your views here.
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = User
    template_name="registration/index.html"

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserUpdate(UpdateView):
    template_name="registration/user_form.html"
    model = User
    fields = ["full_name","email"]
    success_url = "/"

    def get(self, request, **kwargs):
        if not User.objects.get(id=self.kwargs['pk'])==request.user:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

class MyWork(mixins.MonthCalendarMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'work_time/mywork.html'
    model = Worktime
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if year:
            context['date'] = datetime.date(year=int(year), month=int(month), day=int(day))
        return context

    def get(self, request, **kwargs):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if year:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
            if Worktime.objects.filter(date=date,name=request.user).exists():
                objects = Worktime.objects.filter(date=date,name=request.user)
                pk = [object.id for object in objects][0]
                return redirect('/update/{}'.format(pk))
        return super().get(request)

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        mywork = form.save(commit=False)
        mywork.date = date
        mywork.name = self.request.user
        mywork.save()
        return redirect('/work_time/', year=date.year, month=date.month, day=date.day)

class Update(mixins.MonthCalendarMixin, UpdateView):
    template_name = 'work_time/mywork_form.html'
    model = Worktime
    form_class = BS4ScheduleForm
    success_url = "/work_time/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if year:
            context['date'] = datetime.date(year=int(year), month=int(month), day=int(day))
        return context

    def get(self, request, **kwargs):
        if not Worktime.objects.get(id=self.kwargs['pk']).name==request.user:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

class Delete(DeleteView):
    model = Worktime
    # 削除したあとに移動する先（トップページ）
    success_url = "/work_time/"

    def get(self, request, **kwargs):
        if not Worktime.objects.get(id=self.kwargs['pk']).name==request.user:
            return HttpResponse('不正なアクセスです。')
        return super().get(request)

class WorkIndex(ListView):
        # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Worktime
    template_name="work_time/mywork_index.html"
    paginate_by = 5

    def get_queryset(self):
        query_set = Worktime.objects.filter(
            name=self.request.user).order_by('-date')

        return query_set

    def post(self, request, *args, **kwargs):
        form_value = [
            self.request.POST.get('startdate', None),
            self.request.POST.get('enddate', None),
        ]
        request.session['form_value'] = form_value

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        startdate = ''
        enddate = ''
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            startdate = form_value[0]
            enddate = form_value[1]
        default_data = {'startdate': startdate,
                        'enddate': enddate,
                        }
        test_form = SearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form
        context['date_range'] = ','.join([startdate,enddate])
        context['range'] = '〜'.join([startdate,enddate])
        context['objects'] = Worktime.objects.filter(
            name=self.request.user).order_by('-date')

        return context
