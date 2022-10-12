from email import message
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm, UserDeleteForm
from django.contrib.auth import login, authenticate, logout ,get_user_model
from django.db.models import Avg, Sum
from django.contrib.auth.decorators import login_required
from users.models import Profile
from projects.models import Project, Category, Donation, Rate
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes , force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views.generic import DetailView, TemplateView
from django.urls import reverse, reverse_lazy

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('/')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('users/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = SignUpForm()

    return render(
        request=request,
        template_name="registration/signup.html",
        context={"form": form}
        )



@login_required
def userProfile(request, uid):
    user2 = get_object_or_404(User, id=uid)
    categories = Category.objects.all()
    projects = Project.objects.all().filter(user_id=uid)
    for p in projects:

        donation_sum = p.donation_set.all().aggregate(Sum("amount"))['amount__sum']
        p.donation_sum = donation_sum if donation_sum else 0
        p.delete_flag = True if p.donation_sum <= p.target * 0.25 else False

    context = {
        'userprofile': user2,
        'userProject': projects,
        'categories': categories,
        'donations': Donation.objects.all().filter(user_id=uid),
        'latestFiveList': Project.objects.extra(order_by=['created_at'])
    }
    return render(request, "users/profile.html", context)


@login_required
def editProfile(request, uid):
    if request.user.profile.id != uid:
        raise Http404("Not Found")
    user2 = get_object_or_404(User, id=uid)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user2)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=user2.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:profile', uid=uid)

    else:
        u_form = UserUpdateForm(instance=user2)
        p_form = ProfileUpdateForm(instance=user2.profile)
    context = {
        "userprofile": user2,
        # "categories": categories,
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, "users/edit_profile.html", context)


@login_required
def deleteuser(request, uid):
    user2 = get_object_or_404(User, id=uid)
    if request.method == 'POST':
        delete_form = UserDeleteForm(request.POST, instance=user2)
        user2.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('/')
    else:
        delete_form = UserDeleteForm(instance=user2)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'users/delete_account.html', context)



class Dashboard(TemplateView):
    model = Category 
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projects': Project.objects.order_by('id'),
            'categories': Category.objects.order_by('id')
        })
        return context

    def post(self, request, *args, **kwargs):
        if 'delete_project' in request.POST.keys():
            project_id = self.kwargs['pk']
            try:
                project = Project.objects.filter(pk = project_id)
            except: 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            project.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        elif 'delete_category' in request.POST.keys():
            category_id = self.kwargs['pk']
            try:
                category = Category.objects.filter(pk = category_id)
            except: 
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            category.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return super().post(self, request, *args, **kwargs)


def feature_it(request):
    project = get_object_or_404(Project, pk = request.POST['project'])
    project.is_featured = True
    project.save()
    return redirect(reverse('home'))