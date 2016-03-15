try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

try:
    from stepic_web.ask.qa.models import Question, Answer
    from stepic_web.ask.qa.forms import AskForm, AnswerForm
except ImportError:
    import sys
    sys.path.append("/home/box")
    from web.ask.qa.models import Question, Answer
    from web.ask.qa.forms import AskForm, AnswerForm

LIMIT = 10


def panginate(request, qs):
    try:
        page_num = int(request.GET.get("page", 1))
    except ValueError:
        raise Http404

    paginator = Paginator(qs, LIMIT)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page_num, page


def build_url(name, url_params):
    try:
        url = reverse(name)
    except NoReverseMatch:
        url = name

    if url_params:
        url += '?' + urlencode(url_params)
    return url


def test(request, *args, **kwargs):
    return render(request, "base.html")


def get_questions(request, question_type):
    new_questions = Question.objects.get_questions_by_type(question_type)
    page_num, page = panginate(request, new_questions)

    next_page_ref = build_url(question_type, {"page": page_num+1}) if page.has_next() else request.path
    prev_page_ref = build_url(question_type, {"page": page_num-1}) if page.has_previous() else request.path
    return render(request, "question_list.html", {"questions": page.object_list, "next_page_ref": next_page_ref,
                                                  "prev_page_ref": prev_page_ref})


def get_current_question(request, question_id):
    question = get_object_or_404(Question, id=int(question_id))

    user = User.objects.first()
    if request.method == "POST":
        text = request.POST["text"]
        question = request.POST["question"]
        form = AnswerForm(user, text=text, question=question)
        if form.is_valid():
            form.save()
    else:
        form = AnswerForm(user, question=question_id)
    answers = Answer.objects.filter(question=question)
    return render(request, "current_question.html", {"question": question, "answers": answers, "form": form})

# disable csrf defence, put it here just for stepic.org
#@csrf_exempt
def ask_question(request):
    user = User.objects.first()
    if request.method == "POST":
        text = request.POST["text"]
        title = request.POST["title"]
        form = AskForm(user, text=text, title=title)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm(user)
    return render(request, "ask_question.html", {"form": form})
