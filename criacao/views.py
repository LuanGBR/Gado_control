from django.core import validators
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.contrib.auth import get_user,authenticate,login
from django.template import RequestContext, context
from django.views.generic.edit import CreateView
from criacao.forms import CabecagadoCreateForm, CriaCreateForm, PesosCreateForm, VacinasCreateForm, TransacaoCreateForm, CabecagadoEditForm

from criacao.models import boi, cabeca_transacionada, cabecagado, cria, matriz, transacao,brinco, ficha_medica, vacinas

from django.contrib.auth.decorators import login_required

import plotly.graph_objects as go
import datetime 
from django.core import serializers
from datetime import timedelta
import json



def DetailView(request, pk):
    if request.user.is_authenticated:
        tipo = cabecagado.objects.get(id=pk).tipo
        identificacao = cabecagado.__str__(cabecagado.objects.get(id=pk))
        vacinas_list = []
        vacina_dic = {}
        l = vacinas.objects.get(ficha_medica_id = ficha_medica.objects.get(cabecagado_id = pk).id)
        vacinas_list.append({"febre_aftosa":l.febre_aftosa})
        vacinas_list.append({"brucelose":l.brucelose})
        vacinas_list.append({"clostridioses":l.clostridioses})
        vacinas_list.append({"botulismo":l.botulismo})
        vacinas_list.append({"leptospirose":l.leptospirose})
        vacinas_list.append({"raiva":l.raiva})
        vacinas_list.append({"ibr_bvd":l.ibr_bvd})
        if( tipo == "Boi"):
            context = {'id':pk,
            'tipo' : tipo,
            'identificacao':identificacao,
            'pesos':ficha_medica.objects.get(cabecagado_id=pk).pesos_timeseries,
            'observacoes':cabecagado.objects.get(id=pk).observacoes,
            'vacinas':vacinas_list
            }
            resposta_json = json.dumps(context,indent=3)
            return HttpResponse(resposta_json,content_type='aplication/json')

        elif(tipo == "Bezerro"):
            context = {'id':pk,
            'tipo' : tipo,
            'identificacao':identificacao,
            'matriz': cria.objects.get(cabecagado_id=pk).matriz_id,
            'pesos':ficha_medica.objects.get(cabecagado_id=pk).pesos_timeseries,
            'observacoes':cabecagado.objects.get(id=pk).observacoes,
            'vacinas':vacinas_list
            }
            resposta_json = json.dumps(context,indent=3)
            return HttpResponse(resposta_json,content_type='aplication/json')

        else:
            nascimentos_crias = []
            crias = cria.objects.filter(matriz_id = matriz.objects.get(cabecagado_id=pk).id)
            for c in crias:
                nascimentos_crias.append(cabecagado.objects.get(id = c.cabecagado_id).nascimento)
            numdeltas = len(nascimentos_crias)-1
            sumdeltas = timedelta(seconds=0)
            if len(nascimentos_crias) > 1:
                for i in range(len(nascimentos_crias)-1):
                    delta = abs(nascimentos_crias[i+1] - nascimentos_crias[i])
                    sumdeltas += delta
                media = sumdeltas/numdeltas
            else:
                media = 0
            context = {'id':str(pk),
            'tipo' : str(tipo),
            'identificacao':str(identificacao),
            'nascimentos_crias':str(nascimentos_crias),
            'tempo_crias':str(media),
            'gestacoes': str(cria.objects.filter(matriz_id = matriz.objects.get(cabecagado_id=pk).id).count()),
            'pesos':str(ficha_medica.objects.get(cabecagado_id=pk).pesos_timeseries),
            'observacoes':str(cabecagado.objects.get(id=pk).observacoes),
            'vacinas':vacinas_list
            }
            resposta_json = json.dumps(context,indent=3)
            return HttpResponse(resposta_json,content_type='aplication/json')

    else:
        return redirect(f"/login") 


def TransacaoEdit(request,pk):
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {'id':pk}
            context['form'] = TransacaoCreateForm()
            return render(request, "transacoesEdit.html",context)
        if request.method =="POST":
            t = transacao()
            t.id = pk
            stringTransacao = request.POST.get('tags')
            cabecas_transacionadas = str(stringTransacao).split(",")
            array_cabecas = [cabeca_transacionada() for i in range(len(cabecas_transacionadas))]
            t.valor = request.POST.get('valor')
            t.envolvido = request.POST.get('envolvido')
            t.data = request.POST.get('data')
            t.tags = stringTransacao
            t.tipo = request.POST.get('tipo')
            t.save()
            antigoRegistro = cabeca_transacionada.objects.filter(transacao_id=pk).delete()
            for i in range(len(array_cabecas)):
                array_cabecas[i].transacao_id = pk
                array_cabecas[i].cabecagado_id = cabecagado.objects.get(id=int(cabecas_transacionadas[i])).id            
                array_cabecas[i].save()
            return redirect(f"/transacao/{t.id}/view")
    else:
        return redirect(f"/login") 


def TransacaoCreate(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {}
            context['form'] = TransacaoCreateForm()
            return render(request, "transacoesCreate.html",context)
        if request.method =="POST":
            t = transacao()
            stringTransacao = request.POST.get('tags')
            cabecas_transacionadas = str(stringTransacao).split(",")
            array_cabecas = [cabeca_transacionada() for i in range(len(cabecas_transacionadas))]
            t.valor = request.POST.get('valor')
            t.envolvido = request.POST.get('envolvido')
            t.data = request.POST.get('data')
            t.tags = stringTransacao
            t.tipo = request.POST.get('tipo')
            t.save()
            #if tipo == "Compra":
            #    pass
            #elif tipo == "Venda":
            #    for 

            for i in range(len(array_cabecas)):
                array_cabecas[i].transacao_id = t.id
                array_cabecas[i].cabecagado_id = cabecagado.objects.get(id=int(cabecas_transacionadas[i])).id
                array_cabecas[i].save()
            return redirect(f"/transacao/{t.id}/view")
    else:
        return redirect(f"/login") 


def TransacaoList(request):
    if request.user.is_authenticated:
        #context = {"transacoes":transacao.objects.all()}
        transacoes = transacao.objects.all()
        transacoes_list = []
        for t in transacoes:
            transacoes_list.append({'id':t.id,'envolvido':t.envolvido,'data':str(t.data)})
        context = {
            "transacoes":transacoes_list
        }

        resposta_json = json.dumps(context,indent=4)
        return HttpResponse(resposta_json)#,content_type='aplication/json')
    else:
        return redirect(f"/login") 


def TransacaoDetail(request, pk):
    if request.user.is_authenticated:
        transacionadas = []
        transacionadas = cabeca_transacionada.objects.filter(transacao_id = pk)
        tags = []
        for i in transacionadas:
            tags.append(str(cabecagado.__str__(cabecagado.objects.get(id=i.cabecagado_id))))
            if i != transacionadas[len(transacionadas)-1]:
                tags.append(", ")
        tags = "".join(tags)
        tipo = transacao.objects.get(id=pk).tipo
        context = {
            'id': pk,
            'tipo': tipo,
            'valor': transacao.objects.get(id=pk).valor,
            'data': str(transacao.objects.get(id=pk).data),
            'envolvido': transacao.objects.get(id=pk).envolvido,
            'tags': tags
        }
        
        resposta_json = json.dumps(context,indent=3)
        return HttpResponse(resposta_json,content_type='aplication/json')
        
    else:
        return redirect(f"/login") 


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
    if request.method =="GET":
        # user = get_user()
        # if user.is_anonymous:
        #     return redirect("login")
        transacoes = transacao.objects.order_by("data")[:5]
        descricoes = []
        for t in transacoes:
            n = cabeca_transacionada.objects.filter(transacao=t).count()
            descricoes.append(f"{'Compra' if t.tipo else 'Venda'} de {n} cabeças {'de' if t.tipo else 'para'} {t.envolvido}")
        transacoes_list=[]
        for u,v in zip(map(lambda x: x.id, transacoes),descricoes):
            transacoes_list.append({"id":u,"descricão":v})


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
        resposta = {"n_matrizes" : (matriz.objects.filter(cabecagado__esta_vivo=True)&matriz.objects.filter(cabecagado__vendido=False)).count(),
                    "n_bois" : (boi.objects.filter(cabecagado__esta_vivo=True)&boi.objects.filter(cabecagado__vendido=False)).count(),
                    "n_bezerros_male" : (cria.objects.filter(cabecagado__esta_vivo=True)&cria.objects.filter(cabecagado__vendido=False)&cria.objects.filter(cabecagado__sexo=cabecagado.MALE)).count(),
                    "n_bezerros_female" : (cria.objects.filter(cabecagado__esta_vivo=True)&cria.objects.filter(cabecagado__vendido=False)&cria.objects.filter(cabecagado__sexo=cabecagado.FEMALE)).count(),
                    "graph":{
                        "title": "Bezerros prontos para desmame (próximos meses)",
                        "x_label" : "",
                        "y_label" : 'Número de bezerros',
                        "x_series" : x,
                        "male_y_series" : ym,
                        "female_y_series": yf
                        },
                    "transactions":transacoes_list
                    }
        resposta_json = json.dumps(resposta,indent=4)
        return HttpResponse(resposta_json)#,content_type='aplication/json')
    if request.method == "POST":
        return HttpResponseNotFound("") 
        

def CabecaListView(request):
    if request.user.is_authenticated:
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
<<<<<<< HEAD

            set_json = serializers.serialize("json",final_set)
            return HttpResponse(set_json,content_type='aplication/json')

=======
            resposta = []
            for i in final_set:
                resposta.append({"id":i.id,"tipo":i.tipo,"sexo":i.sexo,"n_etiqueta":i.n_etiqueta,"cor_brinco":i.brinco.cor_nome,"idade":i.idade()})
            resposta = {"Cabecas":resposta}
            resposta = json.dumps(resposta,indent=4)
            
            return HttpResponse(resposta)
>>>>>>> 68f09ae1621d7a1e6841eabb1ef910fb31f7b0ab
    else:
        return redirect(f"/login")           
    

def Criar_cabeça(request):
    if request.user.is_authenticated:
        if request.method=="GET":
            sel = "bezerro_sel"
            opt = 3
            context = {}
            if request.GET.get("selected"):
                opt =int(request.GET.get("Tipo"))
                sel = ["boi_sel","vaca_sel","bezerro_sel"][opt-1]
                context["form"] = CabecagadoCreateForm(initial={"nascimento":datetime.date.today().strftime("%d/%m/%Y")})
                if opt == 1:
                    context["form"].fields["sexo"].disabled = True
                    context["form"].fields["sexo"].initial = cabecagado.MALE
                elif opt == 2:
                    context["form"].fields["sexo"].disabled = True
                    context["form"].fields["sexo"].initial = cabecagado.FEMALE
                elif opt == 3:
                    context["form_"] = CriaCreateForm()
                context["form_vac"] = VacinasCreateForm()
                context["form_pesos"] = PesosCreateForm()
                context["mensagem"]="Adicionando " + ["novo touro:","nova vaca:","novo bezerro:"][opt-1]
            context[sel]="selected"
            context["tipo"]=str(opt)
            return render(request,"cabecacreate.html",context)
        if request.method=="POST":
            s = request.POST.get("tipo")
            cabeca = cabecagado()
            cabeca.n_etiqueta = request.POST.get("n_etiqueta")
            cabeca.brinco = brinco.objects.get(id=request.POST.get("brinco"))
            cabeca.nascimento = request.POST.get("nascimento")
            if s == "1":
                cabeca.sexo = cabecagado.MALE
            elif s == "2":
                cabeca.sexo = cabecagado.FEMALE
            elif s == "3":
                cabeca.sexo = request.POST.get("sexo")
            cabeca.tipo = [cabecagado.BOI,cabecagado.MATRIZ,cabecagado.CRIA][int(request.POST.get("tipo"))-1]
            cabeca.author = get_user(request)
            cabeca.save()
            ficha = ficha_medica()
            ficha.cabecagado = cabeca
            ficha.pesos_timeseries = request.POST.get("timeseries")
            ficha.save()
            vac = vacinas()
            vac.ficha_medica = ficha
            vac.febre_aftosa = bool(request.POST.get("febre_aftosa"))
            vac.brucelose = bool(request.POST.get("brucelose"))
            vac.clostridioses = bool(request.POST.get("clostridioses"))
            vac.botulismo = bool(request.POST.get("botulismo"))
            vac.leptospirose = bool(request.POST.get("leptospirose"))
            vac.raiva = bool(request.POST.get("raiva"))
            vac.ibr_bvd = bool(request.POST.get("ibr_bvd"))
            vac.ficha_medica = ficha
            vac.save()
            if s == "1":
                obj = boi()
                obj.cabecagado = cabeca
            elif s == "2":
                obj = matriz()
                obj.cabecagado = cabeca
            elif s =="3":
                obj = cria()
                obj.cabecagado = cabeca
                obj.matriz = matriz.objects.get(id=request.POST.get("matriz"))
            obj.save()
            return redirect(f"/cabeca/{cabeca.id}/view")
    else:
        return redirect(f"/login") 
def EditView(request,pk):
    if request.method=="GET":
        context={}
        cabeca = cabecagado.objects.get(id=pk)
        initial = {"nascimento":cabeca.nascimento,
                   "tipo" : cabeca.tipo,
                   "sexo": cabeca.sexo,
                   "n_etiqueta":cabeca.n_etiqueta,
                   "brinco":cabeca.brinco,
                   "esta_vivo":cabeca.esta_vivo,
                   "observacoes":cabeca.observacoes,
                   "vendido":cabeca.vendido,
                    "morte":cabeca.morte,
                    "causa_mortis":cabeca.causa_mortis
                   }
        context["form"] = CabecagadoEditForm(initial=initial)
        if cabeca.tipo == "Boi":
            opt = 1
        elif cabeca.tipo == "Bezerro":
            context["form"].fields["tipo"].disabled = True
            opt = 3
            context["form_"] = CriaCreateForm(initial={"matriz":cabeca.cria.matriz})
        elif cabeca.tipo == "Vaca":
            opt = 2
            context["form"].fields["tipo"].disabled = True
        context["form"].fields["tipo"].disabled = True
        context["form_vac"] = VacinasCreateForm()
        context["form_pesos"] = PesosCreateForm()
        context["mensagem"]="Editando " + ["touro ","vaca ","bezerro "][opt-1] + str(cabeca)
        context["tipo"]=str(opt)
        return render(request,"cabecaedit.html",context)
    if request.method == "POST":
        cabeca = cabecagado.objects.get(id=pk)  #Puxa a cabeca do tabela cabecagado pelo ID
        s = str(request.POST.get("tipo"))            #Pega o novo tipo
        cabeca.n_etiqueta = request.POST.get("n_etiqueta")  #Define o novo número da etiqueta para a cabeca
        cabeca.brinco = brinco.objects.get(id=str(request.POST.get("brinco")))
        data = request.POST.get("nascimento")
        cabeca.nascimento = data
        checkBoxVivo = str(request.POST.get("esta_vivo"))
        checkBoxVendido = request.POST.get("vendido")
        if checkBoxVivo == 'on':
            cabeca.esta_vivo = True
        else:
            morte = request.POST.get("morte")
            cabeca.morte = morte
            cabeca.causa_mortis = str(request.POST.get("causa_mortis"))
        if checkBoxVendido == 'on':
            cabeca.esta_vivo = False
            cabeca.vendido = True        
        else:
            cabeca.vendido = False
        cabeca.observacoes = request.POST.get("observacoes")
        cabeca.sexo = request.POST.get("sexo")
        cabeca.author = get_user(request)
        cabeca.save()
        ficha = ficha_medica.objects.get(cabecagado_id=pk)
        ficha.cabecagado = cabeca
        ficha.pesos_timeseries = request.POST.get("timeseries")
        ficha.save()
        vac = vacinas.objects.get(ficha_medica_id=int(ficha_medica.objects.get(cabecagado_id=pk).id))
        vac.febre_aftosa = bool(request.POST.get("febre_aftosa"))
        vac.brucelose = bool(request.POST.get("brucelose"))
        vac.botulismo = bool(request.POST.get("botulismo"))
        vac.clostridioses = bool(request.POST.get("clostridioses"))
        vac.raiva = bool(request.POST.get("raiva"))
        vac.leptospirose = bool(request.POST.get("leptospirose"))
        vac.ibr_bvd = bool(request.POST.get("ibr_bvd"))
        vac.save()
        
        if s =="Bezerro":
            obj = cria.objects.get(cabecagado_id=pk)
            obj.matriz = matriz.objects.get(id=request.POST.get("matriz"))
            obj.save()
        return redirect(f"/cabeca/{cabeca.id}/view")