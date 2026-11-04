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
doces_disponiveis = list(Receita.keys())

try:
    with open("estoque.json", "r") as Estoque_Helea:
        Estoque = json.load(Estoque_Helea)
except FileNotFoundError:
    Estoque = {}

while True:
    print("1. Cadastrar novo ingrediente")
    print("2. Calcular custo de uma fornada")
    print("3. Sair")
    
    OpEscolha = int(input("Escolha uma opção: "))

    if OpEscolha == 1:
        print("Selecione o doce:")
        for i, doce in enumerate(doces_disponiveis, 1):
            print(f"{i}. {doce}")
        opcao_doce = int(input("Digite o número do doce: "))
        doces_selecionado = doces_disponiveis[opcao_doce - 1]
        
        lista_ingredientes = list(Receita[doces_selecionado].keys())
        for i, ingred_receita in enumerate(lista_ingredientes, 1):
            print(f"{i}. {ingred_receita}")
        opcao_ingred = int(input("Digite o número do ingrediente: "))
        ingred_selecionado = lista_ingredientes[opcao_ingred - 1]
        preço = float(input("Digite o valor pago pelo ingrediente: ").replace(",","."))
        tamanho = float(input("Digite o tamanho em gramas(ou unidades, se for Ovos): ").replace(",", "."))
        if ingred_selecionado == "Ovos":
            qtd_unidade = tamanho
            tamanho = tamanho*50
            print(f"\n[Sistema]: Convertendo {qtd_unidade:.0f} ovos para {tamanho:.0f}g no estoque")
        if doces_selecionado not in Estoque:
            Estoque[doces_selecionado] = {}
        Estoque[doces_selecionado][ingred_selecionado] = {
            "Tamanho": tamanho,
            "Valor": preço,
        }
        print("\nIngrediente salvo com sucesso!")
        print("Estoque Atual:", Estoque)
        with open("estoque.json", "w") as Estoque_Helea:
            json.dump(Estoque, Estoque_Helea, indent=4)
    elif OpEscolha == 2:
        print("Selecione o doce:")
        for i, doce in enumerate(doces_disponiveis, 1):
            print(f"{i}. {doce}")
        opcao_doce = int(input("Digite o número do doce: "))
        doces_selecionado = doces_disponiveis[opcao_doce - 1]

        custo_total = 0

        if doces_selecionado in Receita:
            print(f"\n--- Calculando custo do {doces_selecionado} ---")
            for nome_ingred, qtd_usada in Receita[doces_selecionado].items():
                if doces_selecionado in Estoque and nome_ingred in Estoque[doces_selecionado]:
                    valor_pago = Estoque[doces_selecionado][nome_ingred]["Valor"]
                    tamanho_pacote = Estoque[doces_selecionado][nome_ingred]["Tamanho"]
                    custo_ingrediente = (valor_pago * qtd_usada) / tamanho_pacote
                    custo_total += custo_ingrediente
                    print(f"- {nome_ingred}: R$ {custo_ingrediente:.2f}")
                else:
                    print(f"Alerta: O preço de '{nome_ingred}' não foi cadastrado! O cálculo final estará ERRADO.")
            print(f"\nO valor dessa fornada foi de R${custo_total:.2f}.")
    elif OpEscolha == 3:
        print("Saindo do sistema... Até Logo!")
        break
    else:
        print("\nOpção inválida! Digite 1, 2 ou 3.")