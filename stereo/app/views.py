from django.shortcuts import render
from django.views import View
from django.db.models import F,Q, When
from .models import Participant, StereotypeQuestions, PersonalQuestion, AnswersPersonal, AnswersStereo, Country
from app.forms import ParticipantForm, ParticipantFormFinish
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect
import uuid
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class Home(View):

    def get(self,request):
        user_id_cookie = request.COOKIES.get('user_id_cookie')
        request.session['answers'] = ['']
        request.session['answerp'] = ['']

        if user_id_cookie is not None:
            #we have this user
            user = Participant.objects.get(user_id=user_id_cookie)
            name = user.name
            gender = user.gender
            form = ParticipantForm(initial={'name':name, 'gender':gender})
        else:
            #new user
            form = ParticipantForm()

        ctx = {'form':form}
        return render(request,'welcome_page.html',ctx)

    def post(self,request):
        form = ParticipantForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            gender = form.cleaned_data['gender']

            response = HttpResponseRedirect(reverse('s_form'))
            # unique user id & setting cookies
            user_id = uuid.uuid4()
            response.set_cookie(key='name_cookie', value=name, max_age=60 * 60 * 24 * 365)
            response.set_cookie(key='gender_cookie', value=gender, max_age=60 * 60 * 24 * 365)
            response.set_cookie(key='user_id_cookie', value=user_id, max_age=60 * 60 * 24 * 365)

            user = Participant.objects.create(user_id=user_id,name=name,gender=gender)
            return response
        else:
            return render(request,'welcome_page.html',{'form':form})

class StereotypeQ(View):
    def get(self,request):
        user_id_cookie = request.COOKIES.get('user_id_cookie')

        answer = request.GET.get("answer")

        if not 'answers' in request.session or not request.session['answers']:
            request.session['answers'] = [answer]
        else:
            answer_list = request.session['answers']
            answer_list.append(answer)
            request.session['answers'] = answer_list
        
        if user_id_cookie is not None:
            # we have this user
            questions_s = StereotypeQuestions.objects.all()

            page = request.GET.get('page', 1)
            paginator = Paginator(questions_s, 1)

            try:
                questions_s = paginator.page(page)
            except PageNotAnInteger:
                questions_s = paginator.page(1)
            except EmptyPage:
                questions_s = paginator.page(paginator.num_pages)

            ctx = {'questions_s': questions_s, 'user_id_cookie':user_id_cookie}
            return render(request, 'form_s.html', ctx)

        else:
            # new user
            form = ParticipantForm()
            ctx = {'form': form}
            return render(request, 'welcome_page.html', ctx)

class PersonalQ(View):
    def get(self,request):
        user_id_cookie = request.COOKIES.get('user_id_cookie')
        questions_p = PersonalQuestion.objects.all()

        answer = request.GET.get("answer")

        if not 'answerp' in request.session or not request.session['answerp']:
            request.session['answerp'] = [answer]
        else:
            answer_list = request.session['answerp']
            answer_list.append(answer)
            request.session['answerp'] = answer_list

        if user_id_cookie is not None:
            # we have this user

            page = request.GET.get('page',1)
            paginator = Paginator(questions_p,1)

            try:
                questions_p = paginator.page(page)
            except PageNotAnInteger:
                questions_p = paginator.page(1)
            except EmptyPage:
                questions_p = paginator.page(paginator.num_pages)

            ctx = {'questions_p':questions_p}
            return render(request,'form_p.html',ctx)

        else:
            # new user
            form = ParticipantForm()
            ctx = {'form': form}
            return render(request, 'welcome_page.html', ctx)



class TemplateTest(View):
    def get(self,request):
        ctx={}
        return render(request,'template_test.html',ctx)

class SubmitStereo(View):
    def get(self,request,answer):
        user_id_cookie = request.COOKIES.get('user_id_cookie')

        answer_list = request.session['answers']
        answer_list.append(f"{answer}")
        request.session['answers'] = answer_list

        stereo_answers = []
        for item in answer_list:
            if item == '1' or item == '2':
                stereo_answers.append(item)

        #participant | question personal | answer int
        user = Participant.objects.get(user_id=user_id_cookie)
        questions = StereotypeQuestions.objects.all()

        if len(stereo_answers) == 56:
            for index, value in enumerate(stereo_answers):
                value = int(value)
                q = questions[index]
                AnswersStereo.objects.create(participant=user,question_stereo=q,answer_stereo=value)
        else:
            pass # add error message with going back to start page & trying again from homepage
        ctx = {}
        return render(request,'submit_s.html',ctx)

class SubmitPersonal(View):
    def get(self,request, answer):
        user_id_cookie = request.COOKIES.get('user_id_cookie')

        if user_id_cookie is not None:

            answer_list = request.session['answerp']
            answer_list.append(f"{answer}")
            request.session['answerp'] = answer_list

            pers_answers = []

            for item in answer_list:
                if item == 'True' or item == 'False':
                    pers_answers.append(item)

            # participant | question personal | answer int
            user = Participant.objects.get(user_id=user_id_cookie)
            questions = PersonalQuestion.objects.all()

            if len(pers_answers) == 56:
                for index, value in enumerate(pers_answers):
                    value = bool(value)
                    q = questions[index]
                    AnswersPersonal.objects.create(participant=user,question_personal=q,answer_personal=value)
            else:
                pass # add error messge with going back to start page & trying again from this survey


            form = ParticipantFormFinish()
            name = "name"
            number = len(Participant.objects.all())

            ctx={"name":name, "number":number, "form":form}

            return render(request,'submit_p.html',ctx)
        else:
            # new user
            form = ParticipantForm()
            ctx = {'form': form}
            return render(request, 'welcome_page.html', ctx)

    def post(self,request):
        user_id_cookie = request.COOKIES.get('user_id_cookie')
        user = Participant.objects.get(user_id=user_id_cookie)

        form = ParticipantFormFinish(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            continent = form.cleaned_data['continent']
            country = form.cleaned_data['country']
            user.email = email
            user.continent = continent
            user.country = country

            #sciagniecie danych i przekazanie do wyswietlenia
            ctx = {}
            return render(request, 'results.html', ctx)

        else:
            # sciagniecie danych na now
            ctx = {}
            return render(request, 'results.html', ctx)

class Results(View):
    def get(self,request):
        user_id_cookie = request.COOKIES.get('user_id_cookie')
        user = Participant.objects.get(user_id=user_id_cookie)
        q_stereo = StereotypeQuestions.objects.all()

        if user.gender == 1:
            color = "deeppink"
        else:
            color = "deepskyblue"


        number = len(Participant.objects.all())
        perc_f = int(len(Participant.objects.filter(gender=1))/number)*100
        perc_m = int(len(Participant.objects.filter(gender=2))/number)*100

        #totals
        result_list = []
        for q in q_stereo:
            answer_s = 1 #women
            ans_s = AnswersStereo.objects.filter(question_stereo=q)
            ans_s_f = ans_s.filter(answer_stereo=answer_s)
            percentage_s = int(len(ans_s_f)/len(ans_s)*100)
            question_s = q.question
            answer_p = True
            qp = PersonalQuestion.objects.get(id=q.id)

                #personal women
            w_ans_p = AnswersPersonal.objects.filter(question_personal=qp).filter(participant__gender=1)
            w_ans_p_yes = w_ans_p.filter(answer_personal=answer_p)
            try:
                w_percentage_p = int(len(w_ans_p_yes)/len(w_ans_p)*100)
            except:
                w_percentage_p = 0
            question_p = qp.question

                #personal men
            m_ans_p = AnswersPersonal.objects.filter(question_personal=qp).filter(participant__gender=2)
            m_ans_p_yes = m_ans_p.filter(answer_personal=answer_p)
            try:
                m_percentage_p = int(len(m_ans_p_yes) / len(m_ans_p) * 100)
            except:
                m_percentage_p = 0

            result_list.append((question_s, answer_s, percentage_s, question_p, answer_p, m_percentage_p, w_percentage_p))

 # [(question, answer, percent)]
        # #q, a, p in tup
        ctx = {'number': number,
               'perc_f':perc_f, 'perc_m':perc_m,
               'result_list':result_list, 'color': color}

        return render(request,'results.html', ctx)

def load_countries(request):
    continent_id = request.GET.get('continent')
    countries = Country.objects.filter(continent_id=continent_id).order_by('country')

    return render(request,"country_drop.html",{"countries":countries})