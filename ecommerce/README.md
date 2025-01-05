# Ferramentas de Análise de E-commerce

Este projeto contém scripts Python para coletar e analisar dados de produtos da Amazon e do Mercado Livre usando Apify e DuckDB.

## 📺 Tutorial
Assista o tutorial passo a passo no YouTube:
[![Tutorial de Análise de Dados de E-commerce](https://img.youtube.com/vi/I7VAidYHUDM/0.jpg)](https://youtu.be/I7VAidYHUDM)

## 🚀 Funcionalidades

- Coleta de dados de produtos da Amazon e Mercado Livre
- Salvamento de dados em formato JSON
- Análise de dados usando DuckDB
- Interface interativa para consultas
- Suporte para buscas personalizadas
- Recursos de visualização de dados

## 📋 Requisitos

Instale os pacotes necessários usando: 

```
pip install -r requirements.txt
```

Pacotes necessários:
- `phidata==2.7.6`
- `pandas==2.2.3`
- `duckdb==1.1.3`
- `apify-client==1.8.1`
- `openai==1.59.3`

## CONFIGURAÇÃO

1. Crie um arquivo `.env` na raiz do projeto
2. Adicione seu token do Apify:
APIFY_TOKEN=seu_token_aqui


## ESTRUTURA DO PROJETO

- `amazon.py` - Script para coletar e analisar produtos da Amazon
- `mercadolivre.py` - Script para coletar e analisar produtos do Mercado Livre
- `requirements.txt` - Dependências do projeto

## COMO USAR

**Coletor da Amazon:**

python amazon.py


**Coletor do Mercado Livre:**

python mercadolivre.py


Ambos os scripts irão:
1. Perguntar se você quer usar dados já existentes
2. Se não, solicitar termos de busca e quantidade
3. Coletar os dados
4. Salvar em um arquivo JSON
5. Fornecer uma interface interativa para análise

## RECURSOS DE ANÁLISE

Ambos os scripts incluem recursos de análise integrados:
- Visualização dos campos de dados disponíveis
- Cálculo de preços médios
- Encontrar produtos mais bem avaliados
- Consultas personalizadas através do modo interativo

## COMO CONSEGUIR UM TOKEN DO APIFY

1. Acesse Apify ([https://console.apify.com/](https://console.apify.com/))
2. Crie uma conta gratuita
3. Vá para "Integrations"
4. Copie seu "Personal API Token"
5. Cole no arquivo `.env`

## DICAS DE USO

- Para buscas mais precisas, use termos específicos
- Recomenda-se começar com uma quantidade menor de produtos para testes
- Salve suas consultas mais úteis para uso futuro
- Utilize o modo interativo para explorar os dados em profundidade

## OBSERVAÇÕES IMPORTANTES

- O número de requisições pode ser limitado pela sua conta Apify
- Alguns produtos podem não ter todos os dados disponíveis
- Os preços são salvos em formato numérico (sem R$)
- Mantenha seu token do Apify em segurança

## LICENÇA

Este projeto é open source e está disponível sob a Licença MIT.

## CONTRIBUIÇÕES

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## CONTATO

Para dúvidas ou sugestões, abra uma issue no GitHub.