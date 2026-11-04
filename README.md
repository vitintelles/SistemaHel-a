# 🧁 Sistema Heléa Artesanal - Gestão de Custos e Receitas

Sistema em Python desenvolvido para automatizar a gestão de estoque, cadastro de ingredientes e cálculo automático de custos de fornadas para a confeitaria artesanal **Heléa Artesanal**.

---

## 🎯 Objetivo do Projeto
O objetivo deste projeto é eliminar erros manuais de precificação e garantir o cálculo exato dos custos de produção (Brownies, Cookies, etc.), cruzando dados estáticos de receitas com o custo dinâmico de insumos comprados no mercado.

---

## 🚀 Funcionalidades Implementadas

### 📌 Sprint 1 - Core e Regras de Negócio
- **Menu Interativo:** Navegação simplificada por menus numéricos gerados dinamicamente via `enumerate`.
- **Prevenção de Erros de Digitação:** Seleção de doces e ingredientes baseada nas chaves estáticas das receitas.
- **Formatação de Dados:** Tratamento automático de entradas numéricas com conversão de vírgula (`,`) para ponto (`.`).
- **Cálculo Automático de Fornada:** Cruzamento de dados de uso da receita com os valores por grama cadastrados no estoque.

### 📌 Sprint 2 - Persistência de Dados
- **Armazenamento em JSON:** Integração com `json` para leitura (`"r"`) e gravação (`"w"`) automática no arquivo `estoque.json`.
- **Tratamento de Exceções:** Uso de `try...except FileNotFoundError` para inicialização segura do sistema sem quebras.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **JSON** (Persistência de Dados)
- **Git & GitHub** (Versionamento e Portfólio)

---

## 📋 Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU-USUARIO/sistema-helea-artesanal.git](https://github.com/SEU-USUARIO/sistema-helea-artesanal.git)
