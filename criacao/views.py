from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth import get_user,authenticate,login
from django.template import RequestContext, context
from django.views.generic.edit import CreateView
from criacao.forms import CabecagadoCreateForm, CriaCreateForm

from criacao.models import boi, cabeca_transacionada, cabecagado, cria, matriz, transacao,brinco

import plotly.graph_objects as go
import datetime 


def DetailView(request, pk):
    context = {'id':pk,
    'pesos':ficha_medica.objects.get(cabecagado_id=pk).pesos,
    'datas':ficha_medica.objects.get(cabecagado_id=pk).datas,
    'observacoes':cabecagado.objects.get(id=pk).observacoes,
    'vacinas': vacinas.objects.get(ficha_medica_id = ficha_medica.objects.get(cabecagado_id=pk))}
    return render(request,"detailview.html",context)



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

def LandView(request):
    return render(request,"landpage.html")

def HomeView(request):
    user = get_user(request)
    if request.method =="GET":
        if user.is_anonymous:
            return redirect("login")
        transacoes = transacao.objects.order_by("data")[:5]
        descricoes = []
        for t in transacoes:
            n = cabeca_transacionada.objects.filter(cabecagado__transacao=t).count()
            descricoes.append(f"{'Compra' if t.tipo else 'Venda'} de {n} cabeças {'de' if t.tipo else 'para'} {t.envolvido}")
        context = {"n_matrizes": matriz.objects.filter(cabecagado__esta_vivo=True).count(),
                   "n_crias": cria.objects.filter(cabecagado__esta_vivo=True).count(),
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
            nf = (cria.objects.filter(cabecagado__esta_vivo=True)&cria.objects.filter(cabecagado__nascimento__lt=data_lim)&cria.objects.filter(cabecagado__sexo=cabecagado.FEMALE)).count() - acum_f
            nm = (cria.objects.filter(cabecagado__esta_vivo=True)&cria.objects.filter(cabecagado__nascimento__lt=data_lim)&cria.objects.filter(cabecagado__sexo=cabecagado.MALE)).count() - acum_m
            acum_f += nf
            acum_m += nm
            yf.append(nf)
            ym.append(nm)
            i += 1
        trace1 = go.Bar(x=x, y=yf,name = "Fêmeas")
        trace2 = go.Bar(x=x, y=ym,name = "Machos")

        layout=go.Layout(title="Bezerros prontos para desmame (próximos meses)", yaxis={'title':'Número de bezerros'})
        figure=go.Figure(data=[trace1,trace2],layout=layout)
    
        context['graph'] = figure.to_html(full_html=False)

        return render(request,"home.html",context)
    if request.method == "POST":
        return HttpResponseNotFound("")
        

def CabecaListView(request):
    if request.method == "GET":
        boi_checked = False
        matriz_checked = False
        cria_checked = True
        order_by_selected = False
        brinco_selected = False
        order_by_text = False
        category_filter = "ativos"
        category_text = "Ativos"
        brincos_set = cabecagado.objects.all()
        if request.GET.get("filtered"):
            if request.GET.get("boi_checked"):
                boi_checked = True
            if request.GET.get("matriz_checked"):
                matriz_checked = True
            if not request.GET.get("cria_checked"):
                cria_checked = False
            if request.GET.get("cor") != "all":
                brinco_selected = brinco.objects.get(id=int(request.GET.get("cor"))),
                brinco_selected = brinco_selected[0]
                brincos_set = cabecagado.objects.filter(brinco = brinco_selected)
            category_filter = request.GET.get("categoria")
            category_text = category_filter.capitalize()

            order_by_selected = request.GET.get("order_by")
            if order_by_selected == "crescente":
                order_by_selected = order_by_selected
                order_by_text = "Brinco - Crescente"
            elif order_by_selected == "maisnovo":
                order_by_selected = order_by_selected
                order_by_text = "Idade - Mais novo"
            elif order_by_selected == "maisvelho":
                order_by_selected = order_by_selected
                order_by_text = "Idade - Mais velho"
            elif order_by_selected == "decrescente":
                order_by_selected = order_by_selected
                order_by_text = "Brinco - Decrescente"
            order_by_selected = request.GET.get("order_by")

        context = {"boi": "checked" if boi_checked else "",
                   "matriz": "checked" if matriz_checked else "",
                   "cria": "checked" if cria_checked else "",
                   "brincos": brinco.objects.all(),
                   "brinco_selected" : brinco_selected,
                   "order_by_selected": order_by_selected,
                   "order_by_text":order_by_text,
                   "category":category_filter,
                   "category_text": category_text
                   }
        
        if category_filter == "ativos":
            status_set = cabecagado.objects.filter(esta_vivo=True)&cabecagado.objects.filter(vendido=False)
        elif category_filter == "mortos":
            status_set = cabecagado.objects.filter(esta_vivo=False)
        elif category_filter == "vendidos":
            status_set = cabecagado.objects.filter(vendido=True)
        cabecas_set = cabecagado.objects.none()
        if boi_checked:
            cabecas_set = cabecas_set.union(cabecagado.objects.filter(tipo=cabecagado.BOI))
        if matriz_checked:
            cabecas_set = cabecas_set.union(cabecagado.objects.filter(tipo=cabecagado.MATRIZ))
        if cria_checked:
            cabecas_set = cabecas_set.union(cabecagado.objects.filter(tipo=cabecagado.CRIA))

        final_set = cabecas_set.intersection(brincos_set,status_set)

        if order_by_selected:
            if order_by_selected == "crescente":
                final_set = final_set.order_by('n_etiqueta')
            elif order_by_selected == "maisnovo":
                final_set = final_set.order_by('-nascimento')
            elif order_by_selected == "maisvelho":
                final_set = final_set.order_by('nascimento')
            elif order_by_selected == "decrescente":
                final_set = final_set.order_by('-n_etiqueta')
        else:
            final_set = final_set.order_by('-nascimento')
        context["cabecas"] = final_set
        

        

        return render(request,"cabecaslist.html",context)
    

def Criar_cabeça(request):
    if request.method=="GET":
        sel = "bezerro_sel"
        context = {}
        if request.GET.get("selected"):
            opt =int(request.GET.get("Tipo"))
            sel = ["boi_sel","vaca_sel","bezerro_sel"][opt-1]
            context["form"] = CabecagadoCreateForm(initial={"nascimento":datetime.date.today().strftime("%d/%m/%Y")})
            if opt == 3:
                context["form_"] = CriaCreateForm()
        context[sel]="selected"
        return render(request,"cabecacreate.html",context)