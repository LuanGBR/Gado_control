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
    if not request.user.is_authenticated():
        return redirect(f"/login")
    tipo = cabecagado.objects.get(id=pk).tipo
    identificacao = cabecagado.__str__(cabecagado.objects.get(id=pk))
    vacinas_list = []
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
        'identificacao': identificacao,
        'n_etiqueta':cabecagado.objects.get(id=pk).n_etiqueta,
        'pesos': ficha_medica.objects.get(cabecagado_id=pk).pesos_timeseries,
        'observacoes': cabecagado.objects.get(id=pk).observacoes,
        'vacinas': vacinas_list,
        'nascimento':cabecagado.objects.get(id=pk).nascimento.strftime("%Y-%m-%d"),
        'sexo': cabecagado.objects.get(id=pk).sexo,
        'esta_vivo':cabecagado.objects.get(id=pk).esta_vivo,
        'vendido':cabecagado.objects.get(id=pk).vendido,
        "ultimo_peso": cabecagado.objects.get(id=pk).get_last_peso(),
        "brinco":{"cor_HEX": cabecagado.objects.get(id=pk).brinco.cor,
                    "cor_nome": cabecagado.objects.get(id=pk).brinco.cor_nome}
        }
        resposta_json = json.dumps(context,indent=3)
        return HttpResponse(resposta_json,content_type='aplication/json')

    elif(tipo == "Bezerro"):
        context = {'id':pk,
        'tipo' : tipo,
        'sexo': cabecagado.objects.get(id=pk).sexo,
        'esta_vivo':cabecagado.objects.get(id=pk).esta_vivo,
        'vendido':cabecagado.objects.get(id=pk).vendido,
        'identificacao':identificacao,
        'n_etiqueta':cabecagado.objects.get(id=pk).n_etiqueta,
        'matriz': cria.objects.get(cabecagado_id=pk).matriz_id,
        'pesos':ficha_medica.objects.get(cabecagado_id=pk).pesos_timeseries,
        'observacoes':cabecagado.objects.get(id=pk).observacoes,
        'vacinas':vacinas_list,
        'nascimento':cabecagado.objects.get(id=pk).nascimento.strftime("%Y-%m-%d"),
        "ultimo_peso": cabecagado.objects.get(id=pk).get_last_peso(),
        "brinco":{"cor_HEX": cabecagado.objects.get(id=pk).brinco.cor,
                    "cor_nome": cabecagado.objects.get(id=pk).brinco.cor_nome}
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
        for i in range(len(nascimentos_crias)):
            nascimentos_crias[i] = nascimentos_crias[i].strftime("%Y-%m-%d")
        if media != 0:
            context = {'id':str(pk),
            'tipo' : str(tipo),
            'n_etiqueta':cabecagado.objects.get(id=pk).n_etiqueta,
            'sexo': cabecagado.objects.get(id=pk).sexo,
            'esta_vivo':cabecagado.objects.get(id=pk).esta_vivo,
            'vendido':cabecagado.objects.get(id=pk).vendido,
            'nascimento':cabecagado.objects.get(id=pk).nascimento.strftime("%Y-%m-%d"),
            'identificacao':str(identificacao),
            'nascimentos_crias':nascimentos_crias,
            'tempo_crias':media.days,
            'gestacoes': str(cria.objects.filter(matriz_id = matriz.objects.get(cabecagado_id=pk).id).count()),
            'pesos':str(ficha_medica.objects.get(cabecagado_id=pk).pesos_timeseries),
            'observacoes':str(cabecagado.objects.get(id=pk).observacoes),
            'vacinas':vacinas_list,
            "ultimo_peso": cabecagado.objects.get(id=pk).get_last_peso(),
            "brinco":{"cor_HEX": cabecagado.objects.get(id=pk).brinco.cor,
                        "cor_nome": cabecagado.objects.get(id=pk).brinco.cor_nome}
            }
        else:
            context = {'id':str(pk),
            'tipo' : str(tipo),
            'n_etiqueta':cabecagado.objects.get(id=pk).n_etiqueta,
            'sexo': cabecagado.objects.get(id=pk).sexo,
            'esta_vivo':cabecagado.objects.get(id=pk).esta_vivo,
            'vendido':cabecagado.objects.get(id=pk).vendido,
            'nascimento':cabecagado.objects.get(id=pk).nascimento.strftime("%Y-%m-%d"),
            'identificacao':str(identificacao),
            'nascimentos_crias':nascimentos_crias,
            'tempo_crias':media,
            'gestacoes': str(cria.objects.filter(matriz_id = matriz.objects.get(cabecagado_id=pk).id).count()),
            'pesos':str(ficha_medica.objects.get(cabecagado_id=pk).pesos_timeseries),
            'observacoes':str(cabecagado.objects.get(id=pk).observacoes),
            'vacinas':vacinas_list,
            "ultimo_peso": cabecagado.objects.get(id=pk).get_last_peso(),
            "brinco":{"cor_HEX": cabecagado.objects.get(id=pk).brinco.cor,
                        "cor_nome": cabecagado.objects.get(id=pk).brinco.cor_nome}
            }

        resposta_json = json.dumps(context,indent=4)
        return HttpResponse(resposta_json,content_type='aplication/json')


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
        if request.method =="POST":
            t = transacao()
            TransacaoInfo = json.loads(request.body.decode('utf-8'))
            t.valor = TransacaoInfo['valor']
            t.envolvido = TransacaoInfo['envolvido']
            t.data = TransacaoInfo['data']
            t.tipo = TransacaoInfo['tipo']
            t.save()
            if t.tipo == "Compra":
                novas_cabecas = TransacaoInfo["novas_cabecas"].split(";")
                for c in novas_cabecas:
                    atributos = c.split(',') #ordem: n_etiqueta, nascimento, sexo, tipo, brinco_id
                    gado = cabecagado()
                    gado.n_etiqueta = str(atributos[0])
                    gado.nascimento = str(atributos[1])
                    gado.tipo = str(atributos[3])
                    if gado.tipo == "Vaca":
                        gado.sexo = "Fêmea"
                    elif gado.tipo == "Boi":
                        gado.sexo = "Macho"
                    else:
                        gado.sexo = str(atributos[2])
                    gado.brinco_id = int(atributos[4])
                    gado.author_id = get_user(request).id
                    gado.save()
                    line = cabeca_transacionada()
                    line.transacao = t
                    line.cabecagado = gado
                    line.save()
                     #   n_etiqueta, nascimento, sexo, tipo, brinco_id
            elif t.tipo == "Venda":
                id_list = TransacaoInfo["id_list"]
                for v in id_list:
                    gado = cabecagado.objects.get(id = v)
                    gado.vendido = 1
                    gado.save()
                    line = cabeca_transacionada()
                    line.transacao = t
                    line.cabecagado = gado
                    line.save()
            return redirect(f"/transacao/{t.id}/view")
    else:
        return redirect(f"/login")


def TransacaoList(request):
    if request.user.is_authenticated:
        transacoes = transacao.objects.order_by("data")
        descricoes = []
        for t in transacoes:
            n = cabeca_transacionada.objects.filter(transacao=t).count()
            descricoes.append(f"{'Compra' if t.tipo=='Compra' else 'Venda'} de {n} cabeças {'de' if t.tipo else 'para'} {t.envolvido}")
        transacoes_list=[]
        for u,v in zip(transacoes,descricoes):
            transacoes_list.append({"id":u.id,"descricao":v,"valor":u.valor,"tipo":u.tipo,"data":str(u.data)})

        resposta_json = json.dumps({"transacoes":transacoes_list},indent=4)
        return HttpResponse(resposta_json,content_type='aplication/json')
    else:
        return redirect(f"/login")


def TransacaoDetail(request, pk):
    if request.method == "GET":
        if request.user.is_authenticated:
            t = transacao.objects.get(id=pk)
            n = cabeca_transacionada.objects.filter(transacao=t).count()
            descricao = f"{'Compra' if t.tipo=='Compra' else 'Venda'} de {n} cabeças {'de' if t.tipo else 'para'} {t.envolvido}"
            transacionadas = cabeca_transacionada.objects.filter(transacao_id = pk)
            cabecas = []
            for i in transacionadas:
                animal = i.cabecagado
                cabecas.append({"id" : animal.id,
                                "n_etiqueta" : animal.n_etiqueta,
                                "tag": str(animal),
                                "tipo": animal.tipo,
                                "brinco":{ "cor_nome":animal.brinco.cor_nome,
                                        "cor_hex":animal.brinco.cor}
                                })
            tipo = transacao.objects.get(id=pk).tipo
            context = {
                'id': pk,
                "descricao":descricao,
                'tipo': tipo,
                'valor': t.valor,
                'data': str(t.data),
                'envolvido': t.envolvido,
                "cabecas": cabecas
            }

            resposta_json = json.dumps(context,indent=4)
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
            return redirect("/dashboard")
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
            descricoes.append(f"{'Compra' if t.tipo=='Compra' else 'Venda'} de {n} cabeças {'de' if t.tipo else 'para'} {t.envolvido}")
        transacoes_list=[]
        for u,v in zip(transacoes,descricoes):
            transacoes_list.append({"id":u.id,"descricao":v,"valor":u.valor,"tipo":u.tipo,"data":str(u.data)})


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
        if request.method == "GET":
            boi_checked = False
            matriz_checked = False
            cria_checked = True
            brincos_set = cabecagado.objects.all()
            if request.GET.get("boi_checked") == "1":
                boi_checked = True
            if request.GET.get("matriz_checked") == "1":
                matriz_checked = True
            if not request.GET.get("cria_checked") == "1":
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
            resposta = []
            for i in final_set:
                resposta.append({"id":i.id,"tipo":i.tipo,"sexo":i.sexo,"n_etiqueta":i.n_etiqueta,"cor_brinco":i.brinco.cor_nome,"idade":i.idade()})
            resposta = {"Cabecas":resposta}
            resposta = json.dumps(resposta,indent=4)

            return HttpResponse(resposta)



def Criar_cabeça(request):
        if request.method=="GET":
            brincos = []
            matrizes = []
            for i in matriz.objects.all():
                matrizes.append({"id":i.id,"identificacao":str(i)})
            for i in brinco.objects.all():
                brincos.append({"id":i.id, "cor_nome":i.cor_nome, "cor_HEX":i.cor})

            resposta = { "matrizes":matrizes,"brincos":brincos}
            return HttpResponse(json.dumps(resposta,indent=4),content_type="application/json")
        if request.method=="POST":
            data = json.loads(request.body.decode('utf-8'))
            s = data["tipo"]
            cabeca = cabecagado()
            cabeca.n_etiqueta = data["n_etiqueta"]

            cabeca.brinco = brinco.objects.get(id=data["brinco"])
            cabeca.nascimento = data["nascimento"]
            if s == "1":
                cabeca.sexo = cabecagado.MALE
            elif s == "2":
                cabeca.sexo = cabecagado.FEMALE
            elif s == "3":
                cabeca.sexo = data["sexo"]
            cabeca.tipo = [cabecagado.BOI,cabecagado.MATRIZ,cabecagado.CRIA][int(data["tipo"])-1]
            cabeca.author = get_user(request)
            cabeca.observacoes = data["observacoes"]
            cabeca.save()
            ficha = ficha_medica()
            ficha.cabecagado = cabeca
            ficha.save()
            vac = vacinas()
            vac.ficha_medica = ficha
            vac.febre_aftosa = bool(data["febre_aftosa"])
            vac.brucelose = bool(data["brucelose"])
            vac.clostridioses = bool(data["clostridioses"])
            vac.botulismo = bool(data["botulismo"])
            vac.leptospirose = bool(data["leptospirose"])
            vac.raiva = bool(data["raiva"])
            vac.ibr_bvd = bool(data["ibr_bvd"])
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
                obj.matriz = matriz.objects.get(id=data["matriz"])
            obj.save()
            return redirect(f"/cabeca/{cabeca.id}/view")

def EditView(request,pk):
    if request.method=="GET":
        cabeca = cabecagado.objects.get(id=pk)
        ficha = ficha_medica.objects.get(cabecagado=cabeca)
        vac = vacinas.objects.get(ficha_medica=ficha)
        resposta = {"cabeca":{
                        "nascimento":cabeca.nascimento.strftime("%Y-%m-%d"),
                        "tipo" : cabeca.tipo,
                        "sexo": cabeca.sexo,
                        "n_etiqueta":cabeca.n_etiqueta,
                        "brinco":cabeca.brinco.id,
                        "esta_vivo":cabeca.esta_vivo,
                        "observacoes":cabeca.observacoes,
                        "vendido":cabeca.vendido,
                        "morte":cabeca.morte.strftime("%Y-%m-%d") if cabeca.morte else None,
                        "causa_mortis":cabeca.causa_mortis
                        },
                    "ficha medica": {
                        "pesos_timeseries": ficha.pesos_timeseries
                        },
                    "vacinas": {
                        "febre_aftosa" : vac.febre_aftosa,
                        "brucelose" : vac.brucelose,
                        "clostridioses" : vac.clostridioses,
                        "botulismo" : vac.botulismo,
                        "leptospirose" : vac.leptospirose,
                        "raiva" : vac.raiva,
                        "ibr_bvd" : vac.ibr_bvd
                        }
                   }

        resposta = json.dumps(resposta,indent=4)
        return HttpResponse(resposta)
    if request.method == "POST":
        cabeca = cabecagado.objects.get(id=pk)  #Puxa a cabeca do tabela cabecagado pelo ID
        data = json.loads(request.body.decode('utf-8'))
        s = {"Boi":"1","Vaca":"2","Bezerro":"3"}[cabeca.tipo]             #Pega o novo tipo
        cabeca.n_etiqueta = data["n_etiqueta"]  #Define o novo número da etiqueta para a cabeca
        cabeca.brinco = brinco.objects.get(id=str(data["brinco"]))
        data_nascimento = data["nascimento"]
        cabeca.nascimento = data_nascimento
        cabeca.observacoes = data["observacoes"]
        if s == "3":
            cabeca.sexo = data["sexo"]
        cabeca.author = get_user(request)
        cabeca.save()
        ficha = ficha_medica.objects.get(cabecagado_id=pk)
        ficha.cabecagado = cabeca
        ficha.pesos_timeseries = data["timeseries"]
        ficha.save()
        vac = vacinas.objects.get(ficha_medica_id=int(ficha_medica.objects.get(cabecagado_id=pk).id))
        vac.febre_aftosa = bool(data["febre_aftosa"])
        vac.brucelose = bool(data["brucelose"])
        vac.botulismo = bool(data["botulismo"])
        vac.clostridioses = bool(data["clostridioses"])
        vac.raiva = bool(data["raiva"])
        vac.leptospirose = bool(data["leptospirose"])
        vac.ibr_bvd = bool(data["ibr_bvd"])
        vac.save()

        if s =="3":
            obj = cria.objects.get(cabecagado_id=pk)
            obj.matriz = matriz.objects.get(id=data["matriz"])
            obj.save()
        return redirect(f"/cabeca/{cabeca.id}/view")

def get_brincosView(request):
    if request.method == "GET":
        return HttpResponse(serializers.serialize('json',brinco.objects.all()) , content_type="application/json")

def get_cabecasAtivasView(request):
    if request.method == "GET":
        qs = cabecagado.objects.filter(esta_vivo=True)&cabecagado.objects.filter(vendido=False)
        cabecas = []
        for i in qs:
            cabecas.append({"id": i.id,"tag":str(i),"tipo":i.tipo,"cor_nome":i.brinco.cor_nome})
            
        return HttpResponse(json.dumps({"cabecas": cabecas}) , content_type="application/json")

def Create_brincos(request):
    if request.method=="POST":
        data = json.loads(request.body.decode("utf-8"))
        new_brinco = brinco()
        new_brinco.cor = data["cor_hex"]
        new_brinco.cor_nome = data["cor_nome"]

def Dar_baixa(request,pk):
    if request.method=="POST":
        cabeca = cabecagado.objects.get(id=pk)
        data = json.loads(request.body.decode("utf-8"))
        cabeca.esta_vivo = 0
        cabeca.morte = data["data_morte"]
        cabeca.causa_mortis = data["causa_mortis"]
        cabeca.save()
        return HttpResponse("")

