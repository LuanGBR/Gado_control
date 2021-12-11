from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth import get_user,authenticate,login
from django.template import RequestContext

from criacao.models import cabeca_transacionada, cria, matriz, transacao

import plotly.graph_objects as go
import datetime 



# Create your views here.
def LoginView(request):
    if request.method =="GET":
        return render(request,"login.html")
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return redirect("login")

def IndexView(request):
    return render(request,"landpage.html")

def HomeView(request):
    user = get_user(request)
    if request.method =="GET":
        if user.is_anonymous:
            return redirect("login")
        transacoes = transacao.objects.order_by("data")[:5]
        descricoes = []
        for t in transacoes:
            n = cabeca_transacionada.objects.filter(transacao=t).count()
            descricoes.append(f"{'Compra' if t.tipo else 'Venda'} de {n} cabeças {'de' if t.tipo else 'para'} {t.envolvido}")
        context = {"n_matrizes": matriz.objects.filter(esta_vivo=True).count(),
                   "n_crias": cria.objects.filter(esta_vivo=True).count(),
                   "transacoes_descricoes":  zip(transacoes,descricoes)
                   }
        meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
        hoje = datetime.date.today()
        mes_atual = hoje.month-1
        i=0
        x = []
        ym = []
        yf = []
        acum_f = 0
        acum_m = 0
        while i<6:
            data_lim = hoje - datetime.timedelta(days=30*(7-i))
            x.append(meses[(mes_atual+i)%12])
            nf = (cria.objects.filter(esta_vivo=True)&cria.objects.filter(nascimento__lt=data_lim)&cria.objects.filter(sexo=False)).count() - acum_f
            nm = (cria.objects.filter(esta_vivo=True)&cria.objects.filter(nascimento__lt=data_lim)&cria.objects.filter(sexo=True)).count() - acum_m
            acum_f += nf
            acum_m += nm
            yf.append(nf)
            ym.append(nm)
            i += 1
        trace1 = go.Bar(x=x, y=yf,name = "Fêmeas")
        trace2 = go.Bar(x=x, y=ym,name = "Machos")

        layout=go.Layout(title="Bezerros prontos para desmame (por mês)", yaxis={'title':'Número de bezerros'})
        figure=go.Figure(data=[trace1,trace2],layout=layout)
    
        context['graph'] = figure.to_html(full_html=False)

        return render(request,"home.html",context)
    if request.method == "POST":
        return HttpResponseNotFound("")
        
