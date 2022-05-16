from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from .forms import UserChangeForm
from .forms import CardForm, ModuleForm
from .forms import CardFormSet
from .forms import RegisterUserForm
from .models import Module, Card
from .models import AdvUser
from .models import Test, Question, Answer


def index(request):
    modules = Module.objects.all()
    tests = Test.objects.all()
    context = {'modules': modules, 'tests': tests}
    return render(request, 'main/index.html', context)


# Module

def show_module(request, pk):
    module = Module.objects.get(pk=pk)
    cards = Card.objects.filter(module=module)
    context = {'cards': cards, 'module': module}
    return render(request, 'main/module.html', context)


@login_required
def add_module(request):
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            formset = CardFormSet(request.POST, request.FILES, instance=module)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('profile')
    else:
        form = ModuleForm(initial={'author': request.user.pk})
        formset = CardFormSet()
    context = {'form': form, 'formset': formset}
    return render(request, 'main/module_add.html', context)


@login_required
def edit_module(request, pk):
    module = Module.objects.get(pk=pk)
    cards_formset = inlineformset_factory(Module, Card, fields='__all__')

    if request.method == "POST":
        module_form = ModuleForm(request.POST, instance=module)
        card_formset = cards_formset(request.POST, request.FILES, instance=module)
        if module_form.is_valid() and card_formset.is_valid():
            module_form.save()
            card_formset.save()

            return HttpResponseRedirect(reverse('module', kwargs={'pk': pk}))
    else:
        module_form = ModuleForm(instance=module)
        card_formset = cards_formset(instance=module)

    context = {'form': module_form, 'formset': card_formset}
    return render(request, 'main/module_edit.html', context)


def show_modules(request):
    modules = Module.objects.all()
    context = {'modules': modules}
    return render(request, 'main/modules.html', context)


@login_required
def delete_module(request, pk):
    module = Module.objects.get(pk=pk)
    module.delete()
    return redirect('profile')


# Test

def show_tests(request):
    tests = Test.objects.all()
    context = {'tests': tests}
    return render(request, 'main/tests.html', context)


def show_test(request, pk):
    test = Test.objects.get(pk=pk)
    questions = Question.objects.filter(test_id=test)
    context = {'test': test, 'questions': questions}
    return render(request, 'main/test.html', context)


def result_test(request, test_id):
    test = Test.objects.get(pk=test_id)
    questions = Question.objects.filter(test_id=test)
    chosen_answers = []

    for i in range(0, len(questions)):
        for answer in questions[i].answer_set.all():
            try:
                if str(answer.id) in request.POST[f'choice{i}']:
                    chosen_answers.append(answer)
            except (KeyError, Answer.DoesNotExist):
                context = {'test': test, 'questions': questions,
                           'error_message': 'Ответьте на все вопросы',
                           'pk': test.pk}
                return render(request, 'main/test.html', context)
    right_answers = []
    for answer in chosen_answers:
        if answer.is_right:
            right_answers.append(answer)
    context = {'test': test, 'questions': questions,
               'answers': chosen_answers,
               'right_answers': len(right_answers),
               'len_questions': len(questions)}
    return render(request, 'main/result_test.html', context)


# Auth

class UserLoginView(LoginView):
    template_name = 'main/login.html'


class UserRegisterView(CreateView):
    form_class = RegisterUserForm
    model = AdvUser
    template_name = 'main/register_user.html'
    success_url = reverse_lazy('register_done')


def register_done(request):
    return render(request, 'main/register_done.html')


# User

@login_required
def profile(request):
    modules = Module.objects.filter(author=request.user.pk)
    context = {'modules': modules}
    return render(request, 'main/profile.html', context)


class ChangeUserInfoView(LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/profile_change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('profile')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_profile(request, pk):
    user = AdvUser.objects.get(pk=pk)
    context = {'user_profile': user}
    return render(request, 'main/user_profile.html', context)
