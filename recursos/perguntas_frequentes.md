# Perguntas Frequentes

Este documento responde às perguntas mais comuns sobre os Agentes de IA da SMN.

## ❓ Perguntas Gerais

### O que são Agentes de IA?

Agentes de IA são sistemas de software que combinam modelos de linguagem com ferramentas e memória para realizar tarefas específicas de forma autônoma. Diferente de um chatbot tradicional, um agente pode usar ferramentas, manter estado entre interações e tomar decisões para atingir objetivos.

### É preciso saber programar para usar estes agentes?

Não necessariamente. Os agentes de exemplo foram projetados para serem executados com comandos simples, e muitos podem ser personalizados editando apenas textos em arquivos de configuração. No entanto, para modificações mais avançadas, algum conhecimento básico de Python será útil.

### Estes agentes são seguros para uso com dados sensíveis?

Os agentes usam APIs externas como a da OpenAI, então os dados passam por servidores de terceiros. Para dados altamente sensíveis, considere:
1. Usar versões dos agentes com modelos locais
2. Implementar ofuscação de dados sensíveis
3. Consultar sua equipe de segurança da informação

## 💻 Configuração e Instalação

### Qual versão do Python devo usar?

Recomendamos Python 3.8 ou superior. A maioria das bibliotecas usadas nos agentes suporta estas versões.

### Por que estou recebendo um erro "ModuleNotFoundError"?

Este erro ocorre quando uma biblioteca necessária não está instalada. Execute:
```
pip install -r requirements.txt
```
Se o erro persistir, tente instalar a biblioteca específica:
```
pip install nome_da_biblioteca
```

### Como obtenho uma chave de API da OpenAI?

1. Crie uma conta em [platform.openai.com](https://platform.openai.com/)
2. Acesse "API keys" no menu
3. Clique em "Create new secret key"
4. Copie a chave e salve em seu arquivo `.env`

### Quanto custa usar estes agentes?

Os custos dependem principalmente do uso das APIs de IA:
- OpenAI cobra por token (unidade de texto) processado
- Para uso leve (algumas consultas por dia), o custo geralmente é de poucos dólares por mês
- Você pode definir limites de uso na plataforma da OpenAI
- Os exemplos deste repositório usam modelos mais econômicos (ex: gpt-3.5-turbo)

## 🔧 Personalização e Uso

### Como posso personalizar a base de conhecimento do Agente de FAQ?

Abra o arquivo `exemplos/exemplo_faq.py` e localize a variável `conhecimento`. Substitua o texto entre aspas triplas com suas próprias informações. Siga o mesmo formato de seções com títulos.

### Como usar meus próprios dados com o Agente de Análise?

Você pode:
1. Fornecer o caminho para seu arquivo CSV quando executar o agente: `python exemplos/exemplo_analise_dados.py caminho/para/seus_dados.csv`
2. Modificar o código para carregar seus dados diretamente, alterando a parte que cria o DataFrame de exemplo

### Como posso fazer o agente responder em outro idioma?

Modifique o template do prompt para incluir instruções sobre o idioma:
```python
template_prompt = """
Você é um assistente de atendimento da SMN. Responda sempre em português.

Informações relevantes:
{contexto}

Pergunta: {pergunta}

Sua resposta (em português):
"""
```

### Como faço para o agente processar documentos em PDF?

O Agente Processador de Documentos já suporta PDFs. Para usá-lo:
1. Certifique-se de que a biblioteca `pypdf` está instalada
2. Execute: `python exemplos/exemplo_processador_documentos.py caminho/para/seu_documento.pdf`

### O agente pode processar documentos Word (DOCX)?

Atualmente, o suporte para documentos Word não está implementado nos exemplos. Para adicionar esta funcionalidade:
1. Instale a biblioteca `python-docx`: `pip install python-docx`
2. Modifique o agente processador para incluir suporte a DOCX

## 📊 Desempenho e Limitações

### Por que o agente às vezes dá respostas incorretas?

Os agentes dependem de modelos de linguagem que têm limitações:
1. Podem gerar informações incorretas ("alucinações")
2. Estão limitados pelo conhecimento em sua base de dados
3. Dependem da qualidade dos prompts e das informações fornecidas

Para minimizar erros:
- Use RAG (retrieval-augmented generation) para fundamentar respostas em fontes confiáveis
- Refine os prompts para serem mais específicos
- Implemente verificação de fatos

### Quanto tempo devo esperar para obter uma resposta?

O tempo de resposta depende de vários fatores:
- Complexidade da tarefa
- Tamanho dos documentos processados
- Velocidade da API usada
- Sua conexão com a internet

Em média:
- Perguntas simples no Agente FAQ: 2-5 segundos
- Análise de dados básica: 5-10 segundos
- Processamento de documentos longos: 30 segundos a alguns minutos

### Há um limite para o tamanho dos documentos que posso processar?

Sim, existem limitações:
- Os modelos de linguagem têm limites de contexto (ex: GPT-3.5 tem limite de ~16K tokens)
- Documentos grandes são divididos em pedaços menores
- Processamento de arquivos muito grandes pode ser lento ou falhar

Para documentos extensos:
- O agente divide em segmentos menores automaticamente
- Use técnicas de resumo para condensar informações
- Considere processá-los em lotes

## 🔄 Integração e Desenvolvimento

### Como integro estes agentes com nossos sistemas internos?

Para integração, você pode:
1. Modificar os agentes para ler/escrever em seus bancos de dados
2. Criar APIs em volta dos agentes usando frameworks como Flask ou FastAPI
3. Conectar os agentes a sistemas de mensagens corporativas

Veja o tutorial [Integrando APIs](../tutoriais/integrando_apis.md) para exemplos detalhados.

### Posso usar estes agentes em aplicações de produção?

Estes agentes são principalmente exemplos educacionais. Para uso em produção:
1. Implemente controle de erros mais robusto
2. Adicione monitoramento e logging
3. Configure autenticação e autorização
4. Otimize para desempenho e escala
5. Teste extensivamente antes de usar com dados reais

### Como contribuo com melhorias para este repositório?

Veja o [guia de contribuição](../CONTRIBUINDO.md) para instruções detalhadas sobre como:
1. Reportar bugs
2. Sugerir melhorias
3. Submeter código
4. Melhorar a documentação

## 🛡️ Segurança e Privacidade

### Os agentes mantêm um histórico das minhas perguntas?

Por padrão, os agentes neste repositório:
- Não armazenam histórico entre sessões
- Não enviam dados para servidores além das APIs necessárias (como OpenAI)

A API da OpenAI pode manter logs para fins de melhoria de serviço. Consulte a [política de privacidade da OpenAI](https://openai.com/policies/privacy-policy) para mais detalhes.

### Como garantir que informações sensíveis não vazem?

Para proteger dados sensíveis:
1. Não inclua informações confidenciais na base de conhecimento dos agentes
2. Implemente filtragem para remover informações sensíveis antes do processamento
3. Use modelos locais quando possível para dados altamente sensíveis
4. Estabeleça regras claras sobre quais tipos de perguntas podem ser feitas

---

Se você tiver outras perguntas não abordadas aqui, sinta-se à vontade para abrir uma issue no repositório ou contribuir com esta documentação.