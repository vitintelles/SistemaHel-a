import json

print("--- SISTEMA HELÉA ARTESANAL ---")

Estoque = {}
Receita = {
    "Brownie": {
        "Chocolate": 160,
        "Ovos": 200,
        "Açucar Cristal": 380,
        "Manteiga": 200,
        "Farinha de Trigo": 200
    },
    "Cookie Baunilha": {
        "Manteiga": 200,
        "Açúcar Mascavo": 175,
        "Açúcar Refinado": 115,
        "Amido de Milho": 35,
        "Ovos": 100,
        "Bicarbonato de Sódio": 4,
        "Fermento": 5,
        "Chocolate em Gotas": 100
    },
    "Cookie Chocolate": {
        "Manteiga": 200,
        "Açúcar Mascavo": 175,
        "Açúcar Refinado": 115,
        "Farinha de Trigo": 340,
        "Amido de Milho": 35,
        "Cacau 50%": 50,
        "Ovos": 100,
        "Bicarbonato de Sódio": 4,
        "Fermento": 5,
        "Chocolate em Gotas": 100
    },
    "Cookie RedVelvet": {
        "Manteiga": 200,
        "Açúcar Mascavo": 175,
        "Açúcar Refinado": 115,
        "Farinha de Trigo": 390,
        "Amido de Milho": 35,
        "Cacau 50%": 25,
        "Ovos": 100,
        "Bicarbonato de Sódio": 4,
        "Fermento": 5,
        "Chocolate em Gotas": 100,
        "Corante em Gel Vermelho": 2
    }
}

Ficha_Tecnica = {
    "Brownie": {"Rendimento": 16, "Embalagem": 1.50},
    "Cookie Baunilha": {"Rendimento": 8, "Embalagem": 1.20},
    "Cookie Chocolate": {"Rendimento": 8, "Embalagem": 1.20},
    "Cookie RedVelvet": {"Rendimento": 8, "Embalagem": 1.20}
}

Tabela_Recheios = {
    "Brownie":{
        "Brigadeiro (Artesanal)": {"Brigadeiro Pronto": 20},
        "Bueno (Pronto)": {"Bueno": 20},
        "Doce de Leite (Pronto)": {"Doce de Leite": 20},
        "Ninho (Artesanal)": {"Ninho Pronto": 20},
        "Ninho com Nutella": {"Ninho Pronto": 10, "Nutella": 10},
        "Nutella (Pronto)": {"Nutella": 20},
        "Ovomaltine (Pronto)": {"Ovomaltine": 20}
    },
    "Cookie": {
        "Bueno (Pronto)": {"Bueno": 20},
        "Doce de Leite (Pronto)": {"Doce de Leite": 20},
        "Nutella (Pronto)": {"Nutella": 20},
    }
}
lista_recheios = list(Tabela_Recheios.keys())
doces_disponiveis = list(Receita.keys())



# Cria uma lsita global e sem repetições de todos os ingredientes usados pela Heléa
ingredientes_unicos = set()
for ingredientes in Receita.values():
    ingredientes_unicos.update(ingredientes.keys())

for familia in Tabela_Recheios.values():
    for recheio_ingredientes in familia.values():
        ingredientes_unicos.update(recheio_ingredientes.keys())
lista_ingredientes_global = sorted(list(ingredientes_unicos))

try:
    with open("estoque.json", "r") as Estoque_Helea:
        Estoque = json.load(Estoque_Helea)
except FileNotFoundError:
    Estoque = {}

while True:
    print("\n1. Cadastrar novo ingrediente")
    print("2. Calcular custo de uma fornada")
    print("3. Visualizar Estoque")
    print("4. Montar Doce Recheado (Venda)")
    print("5. Sair")
    
    OpEscolha = int(input("Escolha uma opção: "))

    if OpEscolha == 1:
        print("\n--- Cadastrar Insumo ---")
        for i, ingred in enumerate(lista_ingredientes_global, 1):
            print(f"{i}. {ingred}")
        opcao_ingred = int(input("Digite o número do ingrediente: "))
        ingred_selecionado = lista_ingredientes_global[opcao_ingred - 1]

        preço = float(input("Digite o valor pago pelo ingrediente: ").replace(",", "."))
        tamanho = float(input("Digite o tamanho em gramas(ou inidades, se for Ovos): ").replace(",", "."))
        if ingred_selecionado =="Ovos":
            qtd_unidade = tamanho
            tamanho = tamanho * 50
            print(f"\n[Sistema]: Convertendo {qtd_unidade:.0f} ovos para {tamanho:.0f}g no estoque")

        # Agora salva diretamente na raiz do dicionário
        Estoque[ingred_selecionado] = {
            "Tamanho": tamanho,
            "Valor": preço,
            "Saldo": tamanho
        }
        print(f"\n✅ {ingred_selecionado} salvo com sucesso no estoque global! ")


        with open("estoque.json", "w") as Estoque_Helea:
            json.dump(Estoque, Estoque_Helea, indent=4)
    elif OpEscolha == 2:
        print("Selecione o doce:")
        for i, doce in enumerate(doces_disponiveis, 1):
            print(f"{i}. {doce}")
        opcao_doce = int(input("Digite o número do doce: "))
        doces_selecionado = doces_disponiveis[opcao_doce - 1]

        if doces_selecionado in Receita:
            print(f"\n--- Verificando estoque para {doces_selecionado} ---")
            estoque_suficiente = True

            # PRÉ-VERIFICAÇÃO GLOBAL
            for nome_ingred, qtd_usada in Receita[doces_selecionado].items():
                #print(f"Debug: Receita pede '{nome_ingred}'. O banco de dados tem: {list(Estoque[doces_selecionado].keys())}")
                if nome_ingred in Estoque:
                    saldo_atual = Estoque[nome_ingred].get("Saldo", Estoque[nome_ingred]["Tamanho"])
                    if saldo_atual < qtd_usada:
                        print(f"❌ Faltam {nome_ingred}! Necessário: {qtd_usada}g | Disponível: {saldo_atual:.02f}g")
                        estoque_suficiente = False
                else:
                    print(f"❌ {nome_ingred} não está cadastrado no estoque!")
                    estoque_suficiente = False

            # Cálculo e Baixa Global        
            if estoque_suficiente:
                custo_total = 0
                print("\n--- Receita Autorizada! Calculando custo... ---")

                for nome_ingred, qtd_usada in Receita[doces_selecionado].items():
                    valor_pago = Estoque[nome_ingred]["Valor"]
                    tamanho_pacote = Estoque[nome_ingred]["Tamanho"]
                    saldo_atual = Estoque[nome_ingred].get("Saldo", tamanho_pacote)
                    
                    custo_ingrediente = (valor_pago * qtd_usada) / tamanho_pacote
                    custo_total += custo_ingrediente

                    novo_saldo = saldo_atual - qtd_usada
                    Estoque[nome_ingred]["Saldo"] = novo_saldo

                    print(f"- {nome_ingred}: R$ {custo_ingrediente:.2f} (Restam: {novo_saldo:.0f}g)")
                print(f"\n✅ O valor dessa fornada foi de R${custo_total:.2f}.")
                rendimento = Ficha_Tecnica[doces_selecionado]["Rendimento"]
                nome_massa = f"Massa de {doces_selecionado}"
                
                #Descobrindo o custo de apenas 1 brownie/cookie sem recheio
                custo_unit_massa = custo_total/ rendimento

                #Verifica se já existe essa massa no estoque para somar, senão começa do zero
                with open("estoque.json", "r") as arq:
                    estoque_atualizado = json.load(arq)
                saldo_atual_massa = estoque_atualizado.get(nome_massa, {}).get("Saldo", 0)

                novo_saldo_massa = saldo_atual_massa + rendimento

                #Salva o produto intermediário no estoque global
                Estoque[nome_massa]={
                    "Tamanho": novo_saldo_massa,
                    "Valor": custo_unit_massa,
                    "Saldo": novo_saldo_massa
                }
                print(f"Fábrica: {rendimento} unidades de '{nome_massa}' enviadas para o estoque!")
                with open("estoque.json", "w") as Estoque_Helea:
                    json.dump(Estoque, Estoque_Helea, indent=4)
            else:
                print(f"\n⚠️ Operação cancelada! Abasteça o estoque na opção 1 para fazer esta fornada")
            
    elif OpEscolha == 3:
        print("\n--- ESTOQUE ATUAL ---")
        if not Estoque:
            print("O estoque está vazio. Cadastre insumos na Opção 1.")
        else:
            for ingredientes, dados in Estoque.items():
                gramas = dados.get("Saldo", dados["Tamanho"])

                # 1. Descobre o maior gasto deste ingrediente em uma única receita
                maior_uso = 0
                for doce, ing_receita in Receita.items():
                    if ingredientes in ing_receita and ing_receita[ingredientes] > maior_uso:
                        maior_uso = ing_receita[ingredientes]

                # 2. O semáforo inteligente de estoque
                if gramas < maior_uso:
                    # Não dá pra fazer nem 1 fornada do doce que mais gasta
                    status = "🔴 Crítico"
                elif gramas < (maior_uso * 2):
                # Dá para fazer 1 fornada, mas não 2 (aviso de ultima fornada
                    status = "🟡 ATENÇÃO"
                else:
                    #Dá para fazer 2 ou mais fornadas
                    status = "🟢 OK"

                if ingredientes.startswith("Massa de"):
                    print(f"🔸 {ingredientes}: {gramas:.0f}un [{status}]")
                else:
                    print(f"🔸 {ingredientes}: {gramas:.0f}g [{status}]")
        print("------------------------")
    elif OpEscolha == 4:
        print("\n--- FRENTE DE CAIXA: MONTAR DOCE ---")

        #1. Puxa só as massas prontas do estoque (tudo que começa com "Massa de")
        massas_disponiveis = [item for item in Estoque.keys() if item.startswith("Massa de")]

        if not massas_disponiveis:
            print("❌ Nenhuma massa pronta! Asse uma fornada na opção 2 primeiro.")
            continue
        print("\nQual base você vai usar?")
        for i, massa in enumerate(massas_disponiveis, 1):
            print(f"{i}. {massa} (Saldo: {Estoque[massa]['Saldo']:.0f} un)")

        opcao_massa = int(input("Digite o número da massa: "))
        massa_selecionada = massas_disponiveis[opcao_massa-1]

        #Remove a palavra "Massa de " para cruzar com a Ficha técnica depois
        nome_original = massa_selecionada.replace("Massa de ","")

        if "Brownie" in nome_original:
            familia = "Brownie"
        else:
            familia = "Cookie"

        recheios_desta_familia = Tabela_Recheios[familia]
        lista_recheios_tela = list(recheios_desta_familia.keys())

        # 2. Escolher o Recheio
        print("\nQual será o recheio?")
        for i, recheio in enumerate (lista_recheios_tela, 1):
            print(f"{i}. {recheio}")
        opcao_recheio = int(input("Digite o número do recheio: "))
        recheio_selecionado = lista_recheios_tela[opcao_recheio - 1]

        # 3. Quantidade desejada
        qtd_venda = int(input(f"\nQuantos '{nome_original} de {recheio_selecionado}' você vai rechear? "))

        # 4. Verificação de Estoque para Montagem
        if Estoque[massa_selecionada]["Saldo"] < qtd_venda:
            print(f"❌ Erro: Você só tem {Estoque[massa_selecionada]['Saldo']:.0f}unidades de {massa_selecionada}.")
            continue
        falta_insumo = False
        for ingred_recheio, qtd_por_unidade in recheios_desta_familia[recheio_selecionado].items():
            qtd_total_necessaria = qtd_por_unidade * qtd_venda
            saldo_ingred = Estoque.get(ingred_recheio, {}).get("Saldo", 0)

            if saldo_ingred < qtd_total_necessaria:
                print(f"❌ Faltam {ingred_recheio}! Necessário: {qtd_total_necessaria}g | Disponível: {saldo_ingred:.0f}g")
                falta_insumo = True
        if falta_insumo:
            print("⚠ Montagem cancelada. Cadastre/Atualize o recheio na Opção 1.")
            continue

        # 5. Baixa no Estoque e Precificação Final
        custo_massa_total = Estoque[massa_selecionada]["Valor"] * qtd_venda
        Estoque[massa_selecionada]["Saldo"] -= qtd_venda

        custo_recheio_total = 0
        for ingred_recheio, qtd_por_unidade in recheios_desta_familia[recheio_selecionado].items():
            qtd_total_necessaria = qtd_por_unidade * qtd_venda
            valor_pago = Estoque[ingred_recheio]["Valor"]
            tamanho_pacote = Estoque[ingred_recheio]["Tamanho"]

            custo_ingred = (valor_pago * qtd_total_necessaria) / tamanho_pacote
            custo_recheio_total += custo_ingred

            Estoque[ingred_recheio]["Saldo"] -= qtd_total_necessaria

        # Adiciona o custo do saquinho/adesivo
        custo_embalagem_total = Ficha_Tecnica[nome_original]["Embalagem"] * qtd_venda

        #Matemática final (preço base + markup de 150%)
        custo_final_unidade = (custo_massa_total + custo_recheio_total + custo_embalagem_total) / qtd_venda
        preco_venda = custo_final_unidade + (custo_final_unidade * 2) #Podendo alterar para 1.50 (150%)
        
        print("\n--- ✅ DOCES MONTADOS COM SUCESSO! ---")
        print(f"Prontos para entrega: {qtd_venda}x {nome_original} de {recheio_selecionado}")
        print(f"Custos de Produção da Unidade (Massa + Recheio + Embalagem): R$ {custo_final_unidade:.2f}")
        print(f"🎯 PREÇO SUGERIDO DE VENDA (Markup 200%): R$ {preco_venda:.2f}")

        with open("estoque.json", "w") as Estoque_Helea:
            json.dump(Estoque, Estoque_Helea, indent=4)

    elif OpEscolha == 5:
        print("Saindo do sistema")
        break    
    else:
        print("\nOpção inválida! Digite 1, 2, 3, 4 ou 5.")