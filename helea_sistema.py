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
    "Cookie Baunilha": {"Rendimento": 8, "Embalgaem": 1.20},
    "Cookie Chocolate": {"Rendimento": 8, "Embalagem": 1.20},
    "Cookie Red Velvet": {"Rendimento": 8, "Embalagem": 1.20}
}
doces_disponiveis = list(Receita.keys())

# Cria uma lsita global e sem repetições de todos os ingredientes usados pela Heléa
ingredientes_unicos = set()
for ingredientes in Receita.values():
    ingredientes_unicos.update(ingredientes.keys())
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
    print("4. Sair")
    
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

                print(f"🔸 {ingredientes}: {gramas:.0f}g [{status}]")
        print("------------------------")
    elif OpEscolha == 4:
        print("Saindo do sistema")
        break    
    else:
        print("\nOpção inválida! Digite 1, 2, 3 ou 4.")