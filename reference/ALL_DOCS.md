## [changelog] Campo transferência removido do contrato de entrada de lançamentos
<https://developer.bling.com.br/changelogs#2026-v354>

O campo transferencia foi removido do contrato de entrada dos endpoints de criação e edição de lançamentos de caixas e bancos. A partir de agora, qualquer valor enviado nesse campo será desconsiderado e o lançamento será registrado como um lançamento de caixa comum. Integrações que enviavam esse campo não precisam de nenhuma alteração, pois o comportamento dos demais campos permanece inalterado.\n Campo transferência removido do contrato de entrada de lançamentos

## [changelog] Nova API de ordens de serviço
<https://developer.bling.com.br/changelogs#2026-v354>

Nova API de ordens de serviço disponibilizada.\n Nova API de ordens de serviço

## [changelog] Correção no tipo e na validação do campo naturezaOperacao ao configurar nota de serviço
<https://developer.bling.com.br/changelogs#2026-v353>

Correção no endpoint PUT /configuracoes/notaservico: o campo naturezaOperacao (em basicas) passa a ser tratado como string, evitando que valores com ponto decimal ou letras (ex: 2.1, T), usados por alguns provedores de NFS-e, sejam truncados ou zerados por um cast indevido para inteiro. Também foi adicionada validação que verifica se o valor informado pertence à lista de naturezas de operação disponíveis para o provedor de NFS-e configurado na empresa, retornando erro quando o valor é inválido. Quando o provedor não define naturezas de operação (campo aberto), a validação é ignorada.\n Correção no tipo e na validação do campo naturezaOperacao ao configurar nota de serviço

## [changelog] Adicionado campo duns na API de produtos
<https://developer.bling.com.br/changelogs#2026-v351>

Adicionado o campo duns aos endpoints de produtos (GET, POST, PUT e PATCH em /produtos), permitindo consultar e gerenciar os códigos DUN (embalagem de distribuição) de um produto. O campo está disponível apenas para empresas com o módulo Checkin de Recebimentos habilitado; sem acesso, o campo é ignorado na escrita e retorna vazio na leitura. Em PUT e PATCH, omitir o campo (ou enviá-lo como null) mantém os DUNs já cadastrados; enviá-lo como array (mesmo vazio) substitui integralmente a lista.\n Adicionado campo duns na API de produtos

## [changelog] Correção no retorno de erro ao criar NF-e com ausência de naturezas de operação cadastradas
<https://developer.bling.com.br/changelogs#2026-v351>

Correção para retornar um erro de validação adequado para o cenário de cadastro de uma NF-e onde a empresa não possui naturezas de operação cadastradas.\n Correção no retorno de erro ao criar NF-e com ausência de naturezas de operação cadastradas

## [changelog] Padronização do formato de data nas consultas de caixa e bancos
<https://developer.bling.com.br/changelogs#2026-v349>

No endpoint GET /caixas, os filtros de período dataInicial e dataFinal passam a aceitar o padrão de data AAAA-MM-DD (ex.: 2024-12-01), utilizado pelas demais APIs do Bling. O formato anterior DD/MM/AAAA continua sendo aceito temporariamente para garantir compatibilidade com integrações existentes, mas será descontinuado em uma versão futura. Recomenda-se migrar as integrações para o novo formato.\n Padronização do formato de data nas consultas de caixa e bancos

## [changelog] Nova API de documentos compartilhados
<https://developer.bling.com.br/changelogs#2026-v349>

Adicionado o endpoint GET /documentos-compartilhados/{token} para acesso a documentos compartilhados via link dinâmico. O token é um token HMAC assinado, gerado automaticamente pelo Bling, com validade de 90 dias. Ao acessar o endpoint, o sistema valida a assinatura e a expiração do token e redireciona (http code 302) para a visualização do documento. Em caso de token inválido ou expirado, o redirecionamento ocorre para a página de erro.\n Nova API de documentos compartilhados

## [changelog] Suporte ao indicador de uso e consumo na NFS-e
<https://developer.bling.com.br/changelogs#2026-v347>

No endpoint POST /nfse, passa a ser suportado o campo tributacaoIbsCbs.indicadorUsoConsumoPessoal, que indica se a operação é destinada a consumidor final (indFinal) (art. 57 da Reforma Tributária — IBS/CBS). Os valores aceitos são 0 (Não), 1 (Sim) e 2 (Não informar). Quando não informado, o campo é preenchido automaticamente com base na configuração do contato vinculado à nota ou, na ausência desta, com o valor padrão 1 (Sim).\n Suporte ao indicador de uso e consumo na NFS-e

## [changelog] Correção no preenchimento do CEST dos itens ao criar NF-e pela API
<https://developer.bling.com.br/changelogs#2026-v345>

No endpoint POST /nfe, quando o CEST do item não for informado explicitamente no payload, passará a ser utilizado o valor cadastrado no sistema para o respectivo produto.\n Correção no preenchimento do CEST dos itens ao criar NF-e pela API

## [changelog] Suporte a criação de notas fiscais de exportação
<https://developer.bling.com.br/changelogs#2026-v345>

No endpoint POST /nfe, passa a ser suportada a criação de notas fiscais de exportação (NF-e de saída com operação com o exterior).\n Suporte a criação de notas fiscais de exportação

## [changelog] Adicionado objeto intermediador na obtenção individual de nota fiscal
<https://developer.bling.com.br/changelogs#2026-v344>

Adicionado objeto intermediador no retorno do endpoint GET /nfe/{idNotaFiscal}, contendo os campos cnpj e nomeUsuario. O objeto é retornado somente quando o indicador de intermediador estiver ativo na nota fiscal.\n Adicionado objeto intermediador na obtenção individual de nota fiscal

## [changelog] Adicionados campos finalidade e tipoNota na API de notas fiscais
<https://developer.bling.com.br/changelogs#2026-v343>

Adicionadas as finalidades 5 (Crédito) e 6 (Débito) para o campo finalidade dos endpoints POST /nfe e GET /nfe/{idNotaFiscal}. Adicionado o campo tipoNota para especificar o tipo da nota quando a finalidade for Crédito ou Débito.\n Adicionados campos finalidade e tipoNota na API de notas fiscais

## [changelog] Corrigido erro interno ao obter anúncios por categoria
<https://developer.bling.com.br/changelogs#2026-v343>

Corrigido o erro HTTP 500 retornado pelo endpoint GET /anuncios/categorias/{idCategoria} ao utilizar IDs de categoria no formato string do Mercado Livre (ex: MLB1430). O parâmetro idCategoria agora aceita corretamente valores string conforme esperado pela integração.\n Corrigido erro interno ao obter anúncios por categoria

## [changelog] Adicionada rota para download do documento da NF-e
<https://developer.bling.com.br/changelogs#2026-v341>

Adicionada rota GET /nfe/documento/{chaveAcesso} para download do documento da NF-e pela chave de acesso. O parâmetro formato (query) é obrigatório e aceita os valores pdf ou xml.\n Adicionada rota para download do documento da NF-e

## [changelog] Alterado endpoint de alteração de situação de pedido de compra
<https://developer.bling.com.br/changelogs#2026-v341>

O endpoint de alteração de situação de pedido de compra agora espera o ID da situação no path, ao invés de informar no body.\nEx: PATCH /pedidos/compras/{idPedidoCompra}/situacoes/{idSituacao}\n Alterado endpoint de alteração de situação de pedido de compra

## [changelog] Ajuste no retorno do campo de documento referenciado em itens de notas fiscais
<https://developer.bling.com.br/changelogs#2026-v339>

O campo documentoReferenciado foi removido do retorno de itens de notas fiscais nos endpoints GET /nfe e GET /nfe/{idNotaFiscal}.\n Ajuste no retorno do campo de documento referenciado em itens de notas fiscais

## [changelog] Adicionada validação de campos IBS/CBS na criação de uma NFS-e
<https://developer.bling.com.br/changelogs#2026-v339>

Adicionada validação dos campos de tributação IBS/CBS (Reforma Tributária) no endpoint POST /nfse, garantindo compatibilidade entre código NBS, indicador de operação, CST e classificação tributária.\n Adicionada validação de campos IBS/CBS na criação de uma NFS-e

## [changelog] Adicionado filtro por ID da unidade de negócio na obtenção múltipla de pedidos de venda
<https://developer.bling.com.br/changelogs#2026-v339>

Adicionado filtro por idUnidadeNegocio referente à filial na obtenção múltipla de pedidos de venda por meio do endpoint GET /pedidos/vendas.\n Adicionado filtro por ID da unidade de negócio na obtenção múltipla de pedidos de venda

## [changelog] Removida a formatação do CEP nos endpoints de notas fiscais
<https://developer.bling.com.br/changelogs#2026-v338>

Removida a formatação dos campos CEP no retorno dos endpoints GET /nfe, GET /nfce, GET /nfe/{idNotaFiscal} e GET /nfce/{idNotaFiscalConsumidor}.\n Removida a formatação do CEP nos endpoints de notas fiscais

## [changelog] Adicionado parâmetro accessKey nos campos linkDanfe e linkPDF na obtenção de NF-e
<https://developer.bling.com.br/changelogs#2026-v338>

Os campos linkDanfe e linkPDF retornados no endpoint GET /nfe/{idNotaFiscal} passam a incluir o parâmetro de query accessKey na URL. Com isso, o tamanho dos links pode aumentar em até 200 caracteres. O parâmetro permite acesso seguro à visualização do documento.\n Adicionado parâmetro accessKey nos campos linkDanfe e linkPDF na obtenção de NF-e

## [changelog] Adicionado campo indicador de operação na API de configurações de NFS-e
<https://developer.bling.com.br/changelogs#2026-v337>

Os endpoints GET /nfse/configuracoes e PUT /nfse/configuracoes agora possuem o campo indicadorOperacao (Indicador de Operação da Reforma Tributária) para cada tributo configurado no objeto ISS.tributos.\n Adicionado campo indicador de operação na API de configurações de NFS-e

## [changelog] Adicionados campos de tributação IBS/CBS para notas fiscais de serviço
<https://developer.bling.com.br/changelogs#2026-v337>

Adicionado suporte ao objeto tributacaoIbsCbs no endpoint POST /nfse, permitindo informar os dados de Tributação IBS/CBS (Imposto sobre Bens e Serviços e Contribuição sobre Bens e Serviços) conforme a nova legislação tributária.\nNovo objeto disponível\nO objeto tributacaoIbsCbs é opcional e deve ser informado apenas quando o município do prestador exigir conformidade com IBS/CBS.\nExemplo de uso:\nPrincipais campos\n\n\n\nCampo\nDescrição\n\n\n\n\nindicadorOperacao\nCódigo que indica onde a operação será realizada (ex: &quot;20201&quot; para operações nacionais)\n\n\ntipoOperacao\nTipo de operação (1 = Tributado, 2 = Não Tributado, 3 = Imune)\n\n\ntipoEnteGovernamental\nTipo de ente governamental quando aplicável (1 = Federal, 2 = Estadual, 3 = Distrito Federal, 4 = Municipal)\n\n\ncodigoSituacaoTributaria\nCST - Código de Situação Tributária (ex: &quot;000&quot; = Tributação integral, &quot;200&quot; = Alíquota reduzida)\n\n\nclassificacaoTributaria\nClassificação específica dentro do CST (ex: &quot;000001&quot;, &quot;200029&quot;)\n\n\n\nCampos adicionais para situações específicas\n\n\nDiferimento (CST 515): percentualDiferimentoEstadual, percentualDiferimentoMunicipal, percentualDiferimentoCBS\n\n\nSuspensão com regime regular (CST 550): cstRegimeRegular, classificacaoTributariaRegular\n\n\nConsulte a Referência da API para a lista completa de campos e suas descrições.\n Adicionados campos de tributação IBS/CBS para notas fiscais de serviço

## [changelog] Permite enviar o ID da unidade de negócio ao salvar ou editar um pedido de venda
<https://developer.bling.com.br/changelogs#2026-v337>

O campo unidadeNegocio.id foi adicionado nos endpoints GET /pedidos/vendas/:idPedidoVenda, POST /pedidos/vendas e PUT /pedidos/vendas/:idPedidoVenda.\n Permite enviar o ID da unidade de negócio ao salvar ou editar um pedido de venda

## [changelog] Permite enviar o ID da unidade de negócio ao salvar uma proposta comercial
<https://developer.bling.com.br/changelogs#2026-v337>

O campo unidadeNegocio.id foi adicionado nos endpoints GET /propostas-comerciais/:idOrcamento e POST /propostas-comerciais.\n Permite enviar o ID da unidade de negócio ao salvar uma proposta comercial

## [changelog] Alterado filtro de situação da conciliação na obtenção múltipla de caixas
<https://developer.bling.com.br/changelogs#2026-v337>

O parâmetro conciliados foi alterado para situacaoConciliacao e agora permite o filtro por todas situações de conciliação.\n Alterado filtro de situação da conciliação na obtenção múltipla de caixas

## [changelog] Adicionado o ID da unidade de negócio na obtenção de um canal de venda
<https://developer.bling.com.br/changelogs#2026-v337>

O campo idUnidadeNegocio referente à filial foi adicionado na obtenção dos detalhes de um canal de venda pelo endpoint GET /canais-venda/{idCanalVenda}.\n Adicionado o ID da unidade de negócio na obtenção de um canal de venda

## [changelog] Correção no retorno de obtenção individual de NF-e e NFC-e
<https://developer.bling.com.br/changelogs#2025-v336>

Para os endpoints GET /nfe/{idNotaFiscal} e GET /nfce/{idNotaFiscal}, ao consultar notas criadas em um ambiente diferente do configurado na conta, resultará em um erro de RESOURCE_NOT_FOUND.\n Correção no retorno de obtenção individual de NF-e e NFC-e

## [changelog] Correção no retorno de obtenção individual de pedido de compra
<https://developer.bling.com.br/changelogs#2025-v336>

Corrigido retorno do campo valor do item no endpoint GET /pedidos/compras/{idPedidoCompra}.\n Correção no retorno de obtenção individual de pedido de compra

## [changelog] Nova API de caixas e bancos
<https://developer.bling.com.br/changelogs#2025-v336>

Nova API de caixas e bancos para administração de laçamentos e registros de caixa.\n\n\nGET /caixas\n\n\nGET /caixas/{idCaixa}\n\n\nPOST /caixas\n\n\nPUT /caixas/{idCaixa}\n\n\nDELETE /caixas/{idCaixa}\n\n\n Nova API de caixas e bancos

## [changelog] Suporte a múltiplos documentos referenciados em notas fiscais
<https://developer.bling.com.br/changelogs#2025-v336>

Documentos referenciados na nota\nO campo documentoReferenciado (objeto singular) foi depreciado e substituído por documentosReferenciados (array), permitindo informar múltiplos documentos referenciados na nota fiscal.\n\n\n\nAnterior\nAtual\n\n\n\n\n&quot;documentoReferenciado&quot;: { ... }\n&quot;documentosReferenciados&quot;: [{ ... }, { ... }]\n\n\n\nRetrocompatibilidade: O campo documentoReferenciado (singular) continua funcionando. O sistema converte automaticamente para o novo formato array.\nDocumento referenciado no item\nFoi adicionado suporte a documento referenciado a nível de item da nota, com os campos chaveAcesso e nItem.\nNovo campo no objeto itens:\n\n\n\nCampo\nTipo\nDescrição\n\n\n\n\ndocumentoReferenciado\nobjeto\nDocumento referenciado do item\n\n\ndocumentoReferenciado.chaveAcesso\nstring\nChave de acesso do documento (44 dígitos)\n\n\ndocumentoReferenciado.nItem\nstring\nNúmero do item no documento referenciado\n\n\n\nExemplo:\nValidação de conflito\nConforme requisitos da Nota Técnica da Reforma Tributária, não é permitido informar documentos referenciados na nota quando há documentos referenciados nos itens.\nNovo código de erro:\n\n\n\nCódigo\nMensagem\n\n\n\n\n31\nNão é permitido informar documentos referenciados na nota quando há documentos referenciados nos itens\n\n\n\nEste erro é retornado quando a requisição contém simultaneamente:\n\n\ndocumentosReferenciados (ou documentoReferenciado) preenchido na raiz da nota, E\n\n\ndocumentoReferenciado preenchido em qualquer item\n\nCenários válidos:\n\nApenas documentosReferenciados na nota (sem docs nos itens)\nApenas documentoReferenciado nos itens (sem docs na nota)\nAmbos preenchidos simultaneamente (retorna erro 31)\n\n Suporte a múltiplos documentos referenciados em notas fiscais

## [changelog] Adiciona dados de IBS e CBS na API de cálculo de impostos
<https://developer.bling.com.br/changelogs#2025-v336>

O endpoint POST /naturezas-operacoes/{idNatureza}/obter-tributacao agora retorna os dados tributários de IBS (Imposto sobre Bens e Serviços) e CBS (Contribuição sobre Bens e Serviços) da Reforma Tributária nos objetos ibsCbs, ibs, cbs e ibsCbsReg (quando aplicável).\n Adiciona dados de IBS e CBS na API de cálculo de impostos

## [changelog] Adicionado parâmetro para controlar envio de e-mail no envio de NF-e
<https://developer.bling.com.br/changelogs#2026-v336>

O endpoint POST /nfe/{idNotaFiscal}/enviar agora aceita o parâmetro enviarEmail (query), permitindo controlar se o e-mail deve ser enviado ao destinatário após a emissão da nota fiscal.\nParâmetro\n\n\n\nCampo\nTipo\nDescrição\n\n\n\n\nenviarEmail\nboolean\nDefine se deve enviar e-mail após a emissão da nota fiscal\n\n\n\nValores:\n\n\ntrue: Envia e-mail ao destinatário\n\nfalse: Não envia e-mail\nNão informado: Utiliza a configuração padrão do sistema\n\nExemplo de uso\nEnviar nota fiscal COM envio de e-mail:\nEnviar nota fiscal SEM envio de e-mail:\nEnviar nota fiscal usando configuração padrão:\n Adicionado parâmetro para controlar envio de e-mail no envio de NF-e

## [changelog] Adicionado parâmetro de ordenação para contas financeiras
<https://developer.bling.com.br/changelogs#2025-v335>

Adicionado parâmetro ordenacao no endpoint GET /contas-contabeis permitindo definir critérios de ordenação das contas financeiras.\nOpção de ordenação:\n\n\ndescricao: Ordenação alfabética com base na descrição da conta\n\nOrdenação padrão (quando não informado): Contas principais primeiro (padrão e padrão de movimentação), depois organizadas por tipo (conta corrente, poupança, recebimento, caixa e outros) e em ordem alfabética dentro de cada grupo.\nO parâmetro é opcional. Se não informado ou com valor inválido, será aplicada a ordenação padrão.\n Adicionado parâmetro de ordenação para contas financeiras

## [changelog] Adicionado filtro por GTIN/EAN na API de produtos
<https://developer.bling.com.br/changelogs#2025-v335>

Adicionado parâmetro gtins[] no endpoint GET /produtos permitindo filtrar produtos por GTIN/EAN.\n Adicionado filtro por GTIN/EAN na API de produtos

## [changelog] Validação de UF nos endpoints de contatos
<https://developer.bling.com.br/changelogs#2025-v334>

Adicionada validação para o campo endereco.geral.uf e endereco.cobranca.uf nos endpoints POST /contatos e PUT /contatos/{idContato}.\n Validação de UF nos endpoints de contatos

## [changelog] Novo campo de natureza de operação na API de pedidos de venda
<https://developer.bling.com.br/changelogs#2025-v334>

Permite informar naturezas de operações específicas por item para que, ao gerar a nota fiscal, o item atenda a regras específicas de tributação.\nO campo itens[].naturezaOperacao.id foi adicionado nos seguintes endpoints:\n\n\nGET /vendas/{idVenda}\n\n\nPUT /vendas/{idVenda}\n\n\nPATCH /vendas/{idVenda}\n\n\n Novo campo de natureza de operação na API de pedidos de venda

## [changelog] Atualização de NF-e não altera o tipo da integração
<https://developer.bling.com.br/changelogs#2025-v330>

O atributo da NF-e que trata o tipo da integração que originou a nota será preservado ao atualizar via endpoint PUT /nfe/{idNotaFiscal}.\n Atualização de NF-e não altera o tipo da integração

## [changelog] Permite informar o código de autorização da transação nas parcelas de notas fiscais
<https://developer.bling.com.br/changelogs#2025-v330>

Adicionado campo caut nos detalhes da parcela da nota fiscal, disponível nos endpoints POST /nfe, PUT /nfe/{idNotaFiscal} e GET /nfe/{idNotaFiscal}.\n Permite informar o código de autorização da transação nas parcelas de notas fiscais

## [changelog] Adiciona campo caut no payload de notas fiscais
<https://developer.bling.com.br/changelogs#2025-v330>

Adiciona campo caut no payload de inserção de notas fiscais POST /nfe, diponível dentro de parcelas.\n Adiciona campo caut no payload de notas fiscais

## [changelog] Corrigido valor do percentual do ISS ao enviar NFS-e
<https://developer.bling.com.br/changelogs#2025-v329>

Agora, o arredondamento do ISS considera quatro casas decimais de precisão, evitando inconsistências no cálculo do valor do imposto no endpoint POST /nfse/{idNotaServico}/enviar.\n Corrigido valor do percentual do ISS ao enviar NFS-e

## [changelog] Permite informar email para envio da nota fiscal no cadastro do contato
<https://developer.bling.com.br/changelogs#2025-v329>

Adicionado campo emailNotaFiscal para o contato nos endpoints POST /contatos, PUT /contatos/{idContato} e GET /contatos/{idContato}.\n Permite informar email para envio da nota fiscal no cadastro do contato

## [changelog] Permite informar o código de autorização de uma parcela ao criar pedidos de vendas
<https://developer.bling.com.br/changelogs#2025-v329>

Adicionado campo caut nos detalhes da parcela do pedido de venda, disponível nos endpoints POST /pedidos/vendas, PUT /pedidos/vendas/{idPedidoVenda} e GET /pedidos/vendas/{idPedidoVenda}.\n Permite informar o código de autorização de uma parcela ao criar pedidos de vendas

## [changelog] Nova API de controle de lotes de produto
<https://developer.bling.com.br/changelogs#2025-v329>

Nova API de controle de lotes de produto disponibilizada.\n Nova API de controle de lotes de produto

## [changelog] Novos campos na obtenção individual de pedidos de compra
<https://developer.bling.com.br/changelogs#2025-v328>

Novos campos no retorno do endpoint GET /pedidos/compras/{idPedidoCompra}:\n\n\nnotaFiscal.id - ID da nota fiscal de entrada\n\nitens[].notaFiscal.id - ID da nota fiscal vinculada ao item\n\nitens[].notaFiscal.quantidade - Quantidade do item vinculado a uma nota fiscal\n\n Novos campos na obtenção individual de pedidos de compra

## [changelog] Ajuste no código de resposta do erro de escopo insuficiente
<https://developer.bling.com.br/changelogs#2025-v328>

Quando autenticado, ao requisitar um recurso ao qual o usuário não possui o escopo necessário, o código HTTP da resposta será 403 Forbidden, ao invés de 401 Unauthorized.\n Ajuste no código de resposta do erro de escopo insuficiente

## [changelog] Liberação de novas rotas de exclusão para categorias de receitas e despesas
<https://developer.bling.com.br/changelogs#2025-v327>

Adicionadas novas rotas DELETE /categorias/receitas-despesas e DELETE /categorias/receitas-despesas/{idCategoria} para exclusões em massa, e por ID, respectivamente.\n Liberação de novas rotas de exclusão para categorias de receitas e despesas

## [changelog] Permite informar se a forma de pagamento utiliza dias úteis na sua criação e atualização
<https://developer.bling.com.br/changelogs#2025-v326>

Permite informar o campo utilizaDiasUteis na criação e atualização de uma forma de pagamento por meio dos endpoints POST /formas-pagamentos e PUT /formas-pagamentos/{idFormaPagamento}.\n Permite informar se a forma de pagamento utiliza dias úteis na sua criação e atualização

## [changelog] Permite alterar o padrão e a situação da forma de pagamento
<https://developer.bling.com.br/changelogs#2025-v326>

Possibilidade de alterar o padrão e a situação de uma forma de pagamento por meio dos endpoints PATCH /formas-pagamentos/padrao/{idFormaPagamento} e PATCH /formas-pagamentos/situacao/{idFormaPagamento}.\n Permite alterar o padrão e a situação da forma de pagamento

## [changelog] Nova API de gerenciamento e categorias de anúncios
<https://developer.bling.com.br/changelogs#2025-v326>

Nova API anuncios disponível para gerenciamento completo de anúncios de integração com marketplaces.\n Nova API de gerenciamento e categorias de anúncios

## [changelog] Ajuste para taxa de marketplace ser subtraída automaticamente na criação de uma conta a receber
<https://developer.bling.com.br/changelogs#2025-v326>

Para contas a receber que possuem taxas de marketplace, no endpoint POST /contas/receber/{idContaReceber}/baixar, o valor da taxa de marketplace não estava sendo subtraido do valorRecebido, sendo necessário subtrair esse valor manualmente para que a baixa funcionasse. Agora, a subtração é feita de forma automática.\n Ajuste para taxa de marketplace ser subtraída automaticamente na criação de uma conta a receber

## [changelog] Validação de lançamentos e situação da nota no PUT de Notas Fiscais Eletrônicas
<https://developer.bling.com.br/changelogs#2025-v325>

A rota PUT /nfe/{idNotaFiscal} verifica a situação da nota fiscal e a existência de lançamentos de estoque e contas. Para notas já autorizadas ou que possuam lançamentos existentes, serão permitidas apenas edições parciais (tipo de frete, dados de transporte, etc). Não será possível atualizar dados fiscais de notas que já foram enviadas à SEFAZ.\nAlém disso, a rota PUT /nfe/{idNotaFiscal} retornará o campo alertas para indicar possíveis ocorrências durante o processo de edição da nota.\n Validação de lançamentos e situação da nota no PUT de Notas Fiscais Eletrônicas

## [changelog] Consulta automática do recibo na emissão de nota de serviço
<https://developer.bling.com.br/changelogs#2025-v325>

Adicionada consulta automática do recibo da nota de serviço por meio do endpoint POST /nfse/{idNotaServico}/enviar.\n Consulta automática do recibo na emissão de nota de serviço

## [changelog] Permite informar a base de cálculo na criação de uma NFS-e
<https://developer.bling.com.br/changelogs#2025-v324>

Adicionado campo de base de cálculo na criação de uma nota fiscal de serviço por meio do endpoint POST /nfse.\n Permite informar a base de cálculo na criação de uma NFS-e

## [changelog] Adicionado filtro para listar serviços inativos na obtenção individual de logística
<https://developer.bling.com.br/changelogs#2025-v324>

Adicionado filtro para listar serviços inativos na obtenção individual de logística por meio do endpoint GET /logisticas/{idLogistica}.\n Adicionado filtro para listar serviços inativos na obtenção individual de logística

## [changelog] Adicionado filtro por tipo de saldo e depósito na obtenção múltipla de produtos
<https://developer.bling.com.br/changelogs#2025-v323>

Adicionado filtro por tipo de saldo (positivo, zerado ou negativo) e depósito na obtenção múltipla de produtos por meio do endpoint GET /produtos.\n Adicionado filtro por tipo de saldo e depósito na obtenção múltipla de produtos

## [changelog] Adicionado filtro por tipo de saldo na obtenção de saldos de estoques
<https://developer.bling.com.br/changelogs#2025-v323>

Adicionado filtro por tipo de saldo na obtenção de saldos de estoque por meio dos endpoints GET /estoques/saldos e GET /estoques/saldos/{idDeposito}.\n Adicionado filtro por tipo de saldo na obtenção de saldos de estoques

## [changelog] Permite informar a situacao na criação de pedido de venda
<https://developer.bling.com.br/changelogs#2025-v323>

Permite informar o campo situacao.id na criação de um pedido de venda por meio do endpoint POST /pedidos/vendas.\n Permite informar a situacao na criação de pedido de venda

## [changelog] Ajuste na obtenção da configuração da alíquota de IR de notas de serviços
<https://developer.bling.com.br/changelogs#2025-v323>

Ajuste na obtenção da alíquota de IR zerada por meio do endpoint GET /nfse/configuracoes.\n Ajuste na obtenção da configuração da alíquota de IR de notas de serviços

## [changelog] Adicionado filtro por IDs de notas fiscais na obtenção de múltiplos pedidos de compras
<https://developer.bling.com.br/changelogs#2025-v321>

Adicionado filtro por IDs de notas fiscais na obtenção de múltiplos pedidos de compras por meio do endpoint GET /pedidos/compras.\n Adicionado filtro por IDs de notas fiscais na obtenção de múltiplos pedidos de compras

## [changelog] Adicionado filtro por tipo de pessoa na obtenção de contatos
<https://developer.bling.com.br/changelogs#2025-v320>

Adicionado filtro por tipo de pessoa na obtenção de contatos no endpoint GET /contatos.\n Adicionado filtro por tipo de pessoa na obtenção de contatos

## [changelog] Ajuste na validação `RESOURCE_NOT_FOUND` nas rotas de nfe
<https://developer.bling.com.br/changelogs#2025-v320>

Ajuste na validação RESOURCE_NOT_FOUND nas rotas de NF-e que utilizam o parâmetro /idNotaFiscal. A correção previne o retorno de erro 500 ao utilizar um ID inválido nas requisições.\n Ajuste na validação `RESOURCE_NOT_FOUND` nas rotas de nfe

## [changelog] Alteração de volumes na atualização de pedido de venda
<https://developer.bling.com.br/changelogs#2025-v319>

Ajustado para gerar um novo volume caso o serviço logístico seja diferente do anterior no endpoint PUT /pedidos/vendas/{idPedidoVenda}.\n Alteração de volumes na atualização de pedido de venda

## [changelog] Adicionados filtros por série, número e chave de acesso na obtenção de múltiplas NF-es e NFC-es
<https://developer.bling.com.br/changelogs#2025-v319>

Adicionado filtros por serie, numero e chaveAcesso nos endpoints GET /nfe e GET /nfce.\n Adicionados filtros por série, número e chave de acesso na obtenção de múltiplas NF-es e NFC-es

## [changelog] Adicionado detalhamento na mensagem do erro 429
<https://developer.bling.com.br/changelogs#2025-v318>

Adicionadas informações de period e limit na response de uma requisição com status code 429.\n\nPeriod:\n\n\nsecond: Indica que o limite por segundo foi atingido.\n\nday: Indica que o limite por dia foi atingido.\n\n\nLimit: Indica o limite da conta referente ao período.\n\n Adicionado detalhamento na mensagem do erro 429

## [changelog] Corrigido valor do percentual do IR nas configurações de NFS-e
<https://developer.bling.com.br/changelogs#2025-v318>

Consideradas as casas decimais do valor do percentual do IR na obtenção das configurações de NFS-e no endpoint GET /nfse/configuracoes.\n Corrigido valor do percentual do IR nas configurações de NFS-e

## [changelog] Adicionada validação de número de caracteres para a descrição da NFS-e
<https://developer.bling.com.br/changelogs#2025-v314>

Adicionada validação para limitar o número de caracteres em 1600 do campo de descrição da nota fiscal de serviço no endpoint POST /nfse.\n Adicionada validação de número de caracteres para a descrição da NFS-e

## [changelog] Adicionados novos campos na obtenção individual de notas por ID
<https://developer.bling.com.br/changelogs#2025-v314>

Novos campos adicionados no retorno dos endpoints GET /nfe/{idNotaFiscal} e GET /nfce/{idNotaFiscalConsumidor}:\n\nitens\noptanteSimplesNacional\nparcelas\nvalorFrete\n\n Adicionados novos campos na obtenção individual de notas por ID

## [changelog] Permite informar o campo série na criação de uma NFS-e
<https://developer.bling.com.br/changelogs#2025-v314>

Ajuste para que o campo serie seja considerado na criação de NFS-e por meio do endpoint POST /nfse.\n Permite informar o campo série na criação de uma NFS-e

## [changelog] Corrigido retorno de categorias de produtos na obtenção de produtos lojas
<https://developer.bling.com.br/changelogs#2025-v314>

Ajuste para que o campo categoriasProdutos retorne os IDs corretamente nos endpoints GET /produtos/lojas e GET /produtos/lojas/{idProdutoLoja}.\n Corrigido retorno de categorias de produtos na obtenção de produtos lojas

## [changelog] Adicionados endpoints para criação e atualização de categorias de receitas e despesas
<https://developer.bling.com.br/changelogs#2025-v314>

Adicionadas rotas POST /categorias/receitas-despesas para a criação e PUT /categorias/receitas-despesas/{idCategoria} para a atualização de uma categoria de receita e despesa.\n Adicionados endpoints para criação e atualização de categorias de receitas e despesas

## [changelog] Paginação na rota de busca de NFC-es
<https://developer.bling.com.br/changelogs#2024-v313>

Ajuste para que os filtros &quot;limite&quot; e &quot;pagina&quot; sejam respeitados ao obter todas as NFes por meio do endpoint GET /nfce.\n Paginação na rota de busca de NFC-es

## [changelog] Adicionada chave de acesso na obtenção de múltiplas notas fiscais
<https://developer.bling.com.br/changelogs#2024-v313>

Adicionada chave de acesso da nota fiscal no retorno dos endpoints GET /nfe e GET /nfce.\n Adicionada chave de acesso na obtenção de múltiplas notas fiscais

## [changelog] Adicionado filtro por transportador na obtenção de NF-e e NFC-e
<https://developer.bling.com.br/changelogs#2024-v313>

Adicionado filtro por transportador (idTransportador) nos endpoints GET /nfe e GET /nfce.\n Adicionado filtro por transportador na obtenção de NF-e e NFC-e

## [changelog] Distribuição dos impostos ICMS ST e IPI nas parcelas de NF-e
<https://developer.bling.com.br/changelogs#2024-v313>

Adicionada distribuição dos impostos ICMS ST e IPI entre as parcelas ao criar nota fiscal por meio do endpoint POST /nfe, respeitando os parâmetros configurados.\n Distribuição dos impostos ICMS ST e IPI nas parcelas de NF-e

## [changelog] Alteração na persistência de produtos para considerar parâmetro de armazenamento de imagens
<https://developer.bling.com.br/changelogs#2024-v313>

Adicionado campo imagensUrl para salvar imagens internas e externas de produto considerando o parâmetro de armazenamento de imagens utilizado na importação e exportação de produtos para lojas virtuais e marketplaces.\nO campo de imagem externas deixou de ser considerado.\n Alteração na persistência de produtos para considerar parâmetro de armazenamento de imagens

## [changelog] Permite filtrar produtos loja por data de alteração
<https://developer.bling.com.br/changelogs#2024-v313>

Adicionado filtros por dataAlteracaoInicial e dataAlteracaoFinal no endpoint GET /produtos/loja.\n Permite filtrar produtos loja por data de alteração

## [changelog] Adicionado código do produto na obtenção de saldos de estoque
<https://developer.bling.com.br/changelogs#2024-v312>

Adicionado código do produto no retorno das rotas GET /estoques/saldos e GET /estoques/saldos/{idDeposito}.\n Adicionado código do produto na obtenção de saldos de estoque

## [changelog] Adicionada rota para atualização parcial de produtos
<https://developer.bling.com.br/changelogs#2024-v312>

Nova rota PATCH /produtos/{idProduto} que permite a atualização parcial de produtos.\n Adicionada rota para atualização parcial de produtos

## [changelog] Ajuste para considerar o campo reterISS na criação de NFS-e
<https://developer.bling.com.br/changelogs#2024-v312>

O valor do campo reterISS não era levado com consideração no momento da criaçao de NFS-e na rota POST /nfse, sendo preenchido sempre com o valor do parâmetro &quot;Preferências &gt; Serviços &gt; Configurações de NFS-e &gt; Configurações básicas e ISS &gt; Reter ISS&quot;. Agora, o valor do parâmetro será considerado apenas se o campo reterISS não for informado no body.\n Ajuste para considerar o campo reterISS na criação de NFS-e

## [changelog] Adicionados campos no cancelamento de NFS-e para o ambiente nacional
<https://developer.bling.com.br/changelogs#2024-v310>

Adicionados campos, no ambiente nacional, codigoMotivo e justificativa no body da requisição de cancelamento de NFS-e.\n Adicionados campos no cancelamento de NFS-e para o ambiente nacional

## [changelog] Permite filtrar pedidos de vendas por data e hora de alteração
<https://developer.bling.com.br/changelogs#2024-v310>

Adicionada a possibilidade de informar a hora nos filtros de data de alteração (dataAlteracaoInicial e dataAlteracaoFinal) na obtenção de múltiplos pedidos de vendas.\n Permite filtrar pedidos de vendas por data e hora de alteração

## [changelog] Permite filtrar contatos por data e hora de inclusão e alteração
<https://developer.bling.com.br/changelogs#2024-v310>

Adicionada a possibilidade de informar a hora nos filtros de data de inclusão e alteração (dataInclusaoInicial, dataInclusaoFinal, dataAlteracaoInicial e dataAlteracaoFinal) na obtenção de múltiplos contatos.\n Permite filtrar contatos por data e hora de inclusão e alteração

## [changelog] Adicionado retorno de erro por falta de informações obrigatórias na emissão de notas fiscais
<https://developer.bling.com.br/changelogs#2024-v309>

Retorno de erro na emissão de NF-e ou NFC-e quando as informações obrigatórias não foram preenchidas. Anteriormente era retornado o HTTP code 200 com os dados do XML em branco, agora será retornado o code 400.\n Adicionado retorno de erro por falta de informações obrigatórias na emissão de notas fiscais

## [changelog] Correção na validação de documentos referenciados na NF-e
<https://developer.bling.com.br/changelogs#2024-v309>

Permite que NF-e com a finalidade normal e CFOP que exige referenciamento de notas preencha as informações relacionadas ao documento referenciado.\n Correção na validação de documentos referenciados na NF-e

## [changelog] Adicionado preço de custo do fornecedor padrão na obtenção de produtos
<https://developer.bling.com.br/changelogs#2024-v308>

Adicionado preço de custo do fornecedor padrão no retorno das rotas GET /produtos e GET /produtos/{idProduto}.\n Adicionado preço de custo do fornecedor padrão na obtenção de produtos

## [changelog] Adicionado saldo atual do estoque na obtenção de produtos
<https://developer.bling.com.br/changelogs#2024-v308>

Adicionado saldo atual do estoque no retorno das rotas GET /produtos e GET /produtos/{idProduto}. A informação será retornada no atributo saldoVirtualTotal pertencente ao objeto de estoque.\n Adicionado saldo atual do estoque na obtenção de produtos

## [changelog] Alterado retorno de obtenções de NF-e e NFC-e quando o recurso não é encontrado
<https://developer.bling.com.br/changelogs#2024-v307>

Alterado retorno nas rotas de obtenção de NF-e e NFC-e por ID quando um recurso não é encontrado. O código retornado é o 404.\n Alterado retorno de obtenções de NF-e e NFC-e quando o recurso não é encontrado

## [changelog] Alteração no endpoint de obtenção das regras de tributação do item
<https://developer.bling.com.br/changelogs#2024-v307>

A rota POST /naturezas-operacoes/{idNaturezaOperacao}/calcular-imposto-item foi alterada para POST /naturezas-operacoes/{idNaturezaOperacao}/obter-tributacao.\n Alteração no endpoint de obtenção das regras de tributação do item

## [changelog] Alteração nos endpoints de boletos vinculados a contas a receber
<https://developer.bling.com.br/changelogs#2024-v307>

Obtenção de boletos\nA rota GET /contas/receber/visualizar/boletos foi alterada para GET /contas/receber/boletos.\nForam renomeados para o português os atributos da resposta, assim como alguns atributos passaram a ser objetos.\n\n\n\nAnterior\nAtual\n\n\n\n\n&quot;numberSale&quot;\n&quot;venda&quot;: {&quot;numero&quot;: 123}\n\n\n&quot;numberNF&quot;\n&quot;notaFiscal&quot;: {&quot;numero&quot;: &quot;000001&quot;}\n\n\n&quot;amountAccounts&quot;\nAtributo removido\n\n\n&quot;amountValuesAccounts&quot;\n&quot;valorTotal&quot;\n\n\n&quot;haveAccountWithIntegration&quot;\nAtributo removido\n\n\n&quot;accounts&quot;\n&quot;contas&quot;\n\n\n\nAtributos dentro do objeto anteriormente denominado accounts:\n\n\n\nAnterior\nAtual\n\n\n\n\n&quot;idExternal&quot;\n&quot;numeroExterno&quot;\n\n\n&quot;dueDate&quot;\n&quot;vencimento&quot;\n\n\n&quot;value&quot;\n&quot;valor&quot;\n\n\n&quot;situation&quot;\n&quot;situacao&quot;\n\n\n&quot;iconSituation&quot;\nAtributo removido\n\n\n&quot;descriptionSituation&quot;\nAtributo removido\n\n\n\nO filtro situations foi alterado para situacoes, assim como suas opções foram alteradas para números inteiros, conforme documentado na Referência da API.\nCancelamento de boletos\nA rota POST /contas/receber/cancelar/boletos foi alterada para POST /contas/receber/boletos/cancelar.\nForam renomeados para o português os atributos no corpo da requisição, assim como alguns atributos passaram a ser objetos. Também foi criado o objeto autenticacao para agrupar os seus atributos.\n\n\n\nAnterior\nAtual\n\n\n\n\n&quot;type2FA&quot;\n&quot;autenticacao&quot;: {&quot;tipo&quot;: 1}\n\n\n&quot;code2FA&quot;\n&quot;autenticacao&quot;: {&quot;codigo&quot;: &quot;000000&quot;}\n\n\n&quot;idOrigem&quot;\n&quot;origem&quot;: {&quot;id&quot;: 321}\n\n\n&quot;idDuplicata&quot;\n&quot;duplicata&quot;: {&quot;id&quot;: 123}\n\n\n&quot;reason&quot;\n&quot;motivo&quot;\n\n\n\n Alteração nos endpoints de boletos vinculados a contas a receber

## [changelog] Alteração para permitir o filtro por múltiplos códigos de produtos na obtenção de produtos
<https://developer.bling.com.br/changelogs#2024-v307>

Alterado o filtro por código de produto para permitir múltiplos na obtenção de produtos.\n Alteração para permitir o filtro por múltiplos códigos de produtos na obtenção de produtos

## [changelog] Bloqueio de requisições com filtro por período com intervalo superior a um ano
<https://developer.bling.com.br/changelogs#2024-v306>

Requests GET com filtros por período com intervalo superior a um ano retornarão o status code 400.\nFiltro por período: Possui sufixo &quot;Inicial&quot; ou &quot;Final&quot;.\nExemplos:\n\n\nRequest válida\n\nGET /pedidos/vendas?dataAlteracaoInicial=2024-01-01&amp;dataAlteracaoFinal=2024-06-16\n\n\nRequest inválida\n\nGET /pedidos/vendas?dataAlteracaoInicial=2023-01-01&amp;dataAlteracaoFinal=2024-02-12\n Bloqueio de requisições com filtro por período com intervalo superior a um ano

## [changelog] Adicionados campos numeroPedidoLoja e vendedor na obtenção individual de NF-e e NFC-e
<https://developer.bling.com.br/changelogs#2024-v306>

Endpoints GET /nfe/{idNotaFiscal} e  GET /nfce/{idNotaFiscalConsumidor} passam a retornar as informações numeroPedidoLoja e vendedor.\n Adicionados campos numeroPedidoLoja e vendedor na obtenção individual de NF-e e NFC-e

## [changelog] Alteração do tipo do campo especie para inteiro nas rotas de notas fiscais
<https://developer.bling.com.br/changelogs#2024-v306>

Alterado o tipo do campo especie para inteiro com opções predefinidas. As seguintes rotas sofreram alterações:\n\n\nPOST /nfe\n\n\nPOST /nfce\n\n\nPUT /nfe/{idNotaFiscal}\n\n\nPUT /nfce/{idNotaFiscalConsumidor}\n\n\n Alteração do tipo do campo especie para inteiro nas rotas de notas fiscais

## [changelog] Permite atualização de produto fornecedor sem informar o ID do fornecedor
<https://developer.bling.com.br/changelogs#2024-v306>

Campo ID do fornecedor passa a ser opcional ao atualizar produto fornecedor pelo endpoint PUT /produtos/fornecedores/{idProdutoFornecedor}.\n Permite atualização de produto fornecedor sem informar o ID do fornecedor

## [changelog] Alterações em atributos retornados nos endpoints de obtenção e criação de notas fiscais
<https://developer.bling.com.br/changelogs#2024-v306>

As seguintes rotas sofreram alterações:\n\n\nGET /nfe/{idNotaFiscal}\n\n\nGET /nfce/{idNotaFiscalConsumidor}\n\n\nPOST /nfce\n\n\nPOST /nfe\n\n\nO campo etiqueta foi removido do payload.\nO campo enderecos foi adicionado no payload, esse atributo terá as informações dos endereços de entrega e retirada.\n Alterações em atributos retornados nos endpoints de obtenção e criação de notas fiscais

## [changelog] Revertidas alterações em atributos retornados nos endpoints de obtenção e criação de notas fiscais
<https://developer.bling.com.br/changelogs#2024-v306>

As seguintes rotas sofreram alterações:\n\n\nGET /nfe/{idNotaFiscal}\n\n\nGET /nfce/{idNotaFiscalConsumidor}\n\n\nPOST /nfce\n\n\nPOST /nfe\n\n\nO campo enderecos foi removido do payload, devido algumas inconsistências encontradas com a funcionalidade destes campos.\nO campo etiqueta foi adicionado novamente no payload, esse atributo terá as informações do endereço de entrega do cliente, o mesmo não levará as informações para o XML da nota.\n Revertidas alterações em atributos retornados nos endpoints de obtenção e criação de notas fiscais

## [changelog] Nova API de grupos de produtos
<https://developer.bling.com.br/changelogs#2024-v305>

Nova API de grupos de produtos disponiblizada.\n Nova API de grupos de produtos

## [changelog] Adicionado filtro por contato e tipo de data na obtenção de múltiplas contas a receber
<https://developer.bling.com.br/changelogs#2024-v305>

Adicionado filtro pelo ID do contato e filtro por tipo de data no endpoint GET /contas/receber.\n Adicionado filtro por contato e tipo de data na obtenção de múltiplas contas a receber

## [changelog] Correção na criação de NF-e para determinadas finalidades
<https://developer.bling.com.br/changelogs#2024-v305>

Corrigida a criação de nota com a finalidade, 2 (complementar), 3 (ajuste) e 4 (devolução).\n Correção na criação de NF-e para determinadas finalidades

## [changelog] Adicionada data de início do contrato ao obter dados básicos da empresa
<https://developer.bling.com.br/changelogs#2024-v305>

Adicionada data de início do contrato no retorno do endpoint GET /empresas/me/dados-basicos.\n Adicionada data de início do contrato ao obter dados básicos da empresa

## [changelog] Adiciona novos tipos de pagamento conforme o Informe Técnico SEFAZ 2024.002
<https://developer.bling.com.br/changelogs#2024-v305>

Adicionado novos tipos de pagamento nos seguintes endpoints:\nGET /formas-pagamentos/{idFormaPagamento}\nPOST /formas-pagamentos\nPUT /formas-pagamentos/{idFormaPagamento}\n Adiciona novos tipos de pagamento conforme o Informe Técnico SEFAZ 2024.002

## [changelog] Alteração para permitir o filtro por múltiplos códigos de produtos na obtenção de saldos de estoque
<https://developer.bling.com.br/changelogs#2024-v304>

Alterado o filtro por código de produto para permitir múltiplos na obtenção de saldos de estoque.\n Alteração para permitir o filtro por múltiplos códigos de produtos na obtenção de saldos de estoque

## [changelog] Nova API de propostas comerciais
<https://developer.bling.com.br/changelogs#2024-v304>

Nova API de propostas comerciais disponiblizada.\n Nova API de propostas comerciais

## [changelog] Adicionado identificador do produto pai na obtenção de um produto do tipo variação
<https://developer.bling.com.br/changelogs#2024-v303>

A propriedade id será retornada dentro da propriedade produtoPai na obtenção de um produto.\n Adicionado identificador do produto pai na obtenção de um produto do tipo variação

## [changelog] Nova API de ordens de produção
<https://developer.bling.com.br/changelogs#2024-v303>

Nova API de ordens de produção disponiblizada.\n Nova API de ordens de produção

## [changelog] Adicionado atributo de ID da empresa ao obter dados básicos da empresa
<https://developer.bling.com.br/changelogs#2024-v303>

Adicionado atributo de ID da empresa no retorno do endpoint GET /empresas/me/dados-basicos.\n Adicionado atributo de ID da empresa ao obter dados básicos da empresa

## [changelog] Adicionados campos na obtenção de contas a receber, contas a pagar e formas de pagamento
<https://developer.bling.com.br/changelogs#2024-v301>

Contas a Receber GET /contas/receber/{idContaReceber}:\n\ntarifa\n\nContas a Pagar GET /contas/pagar/{idContaPagar}:\n\nocorrencia\ntarifa\n\nFormas de Pagamentos GET /formas-pagamentos:\n\nfinalidade\n\n Adicionados campos na obtenção de contas a receber, contas a pagar e formas de pagamento

## [changelog] Correção nos filtros de datas de inclusão e alteração na obtenção de múltiplos produtos
<https://developer.bling.com.br/changelogs#2024-v301>

Adicionada a possibilidade de informar a hora nos filtros de data de inclusão (dataInclusaoInicial e dataInclusaoFinal) e data de alteração (dataAlteracaoInicial e dataAlteracaoFinal) na obtenção de múltiplos produtos.\n Correção nos filtros de datas de inclusão e alteração na obtenção de múltiplos produtos

## [changelog] Nova API de canais de venda
<https://developer.bling.com.br/changelogs#2024-v300>

Nova API de canais de venda disponibilizada.\n Nova API de canais de venda

## [changelog] Adicionada validação do número da nota fiscal
<https://developer.bling.com.br/changelogs#2024-v300>

Ajuste para não permitir a atualização de NFC-e sem informar a numeração.\n Adicionada validação do número da nota fiscal

## [changelog] Adicionado identificador do produto pai no retorno de produtos do tipo variação
<https://developer.bling.com.br/changelogs#2024-v300>

A propriedade idProdutoPai será retornada na obtenção de múltiplos produtos, caso o produto seja uma variação.\n Adicionado identificador do produto pai no retorno de produtos do tipo variação

## [changelog] Correção ao salvar a NFS-e com multiplas parcelas
<https://developer.bling.com.br/changelogs#2024-v299>

Ajuste na validação de equivalência do valor total das parcelas com o total dos serviços.\n Correção ao salvar a NFS-e com multiplas parcelas

## [changelog] Adicionado filtro por código do produto na obtenção de saldos de estoque
<https://developer.bling.com.br/changelogs#2024-v299>

Adicionado filtro nas rotas GET /estoques/saldos/{idDeposito} e GET /estoques/saldos para obter os saldos de um produto a partir do código.\n Adicionado filtro por código do produto na obtenção de saldos de estoque

## [changelog] Obtenção dos links do boleto e do QR Code em contas a receber
<https://developer.bling.com.br/changelogs#2024-v298>

Adicionado retorno de links do boleto e do QR Code no GET /contas/receber e GET /contas/receber/{idContaReceber}.\n Obtenção dos links do boleto e do QR Code em contas a receber

## [changelog] Adicionado filtro para obter vendedores em todas as situações
<https://developer.bling.com.br/changelogs#2024-v296>

Adicionado filtro no GET /vendedores para filtrar por todas as situações, inclusive para os excluídos.\n Adicionado filtro para obter vendedores em todas as situações

## [changelog] Alteração no filtro de critério na obtenção de produtos
<https://developer.bling.com.br/changelogs#2024-v296>

O filtro por critério (5 Todos) no GET /produtos retornará inclusive os produtos excluídos.\n Alteração no filtro de critério na obtenção de produtos

## [changelog] Adicionada rota para obtenção do contato consumidor final
<https://developer.bling.com.br/changelogs#2024-v296>

Nova rota GET /contatos/consumidor-final que obtém os dados do contato consumidor final. O consumidor final é um contato padrão do sistema que é criado automaticamente e não pode ser alterado.\n Adicionada rota para obtenção do contato consumidor final

## [changelog] Retorno de imagens na obtenção de produtos
<https://developer.bling.com.br/changelogs#2024-v295>

Disponibilização do link de imagens internas por meio do endpoint GET /produtos/{idProduto}.\nInclusão da thumbnail na obtenção de múltiplos produtos por meio do endpoint GET /produtos.\n Retorno de imagens na obtenção de produtos

## [changelog] Adicionados filtros na obtenção de contas contábeis
<https://developer.bling.com.br/changelogs#2024-v294>

Adicionados filtros ocultarInvisiveis, ocultarContasIntegracaoPagamento, removerTipoContaBancaria e situacoes na obtenção de contas contábeis por meio do endpoint GET /contas-contabeis.\n Adicionados filtros na obtenção de contas contábeis

## [changelog] Novas rotas para lançamento e estorno de estoques por NF-e e NFC-e
<https://developer.bling.com.br/changelogs#2024-v292>

Adição das funcionalidades de lançar e estornar estoques por meio de uma NF-e ou NFC-e.\n Novas rotas para lançamento e estorno de estoques por NF-e e NFC-e

## [changelog] Alteração no campo intermediador das rotas de NFe
<https://developer.bling.com.br/changelogs#2024-v292>

Ajuste no campo intermediador para que seja considerado ao criar NFes por meio do endpoint POST /nfe.\n Alteração no campo intermediador das rotas de NFe

## [changelog] Correção de permissionamento para ações em NF-e
<https://developer.bling.com.br/changelogs#2024-v292>

Ajuste na validação de permissões para ações de lançar/estornar contas e estoques, além de excluir notas fiscais de entrada, utilizando os mesmos endpoints da nota fiscal de saída.\n Correção de permissionamento para ações em NF-e

## [changelog] Alteração da ordenação na obtenção de NFe e NFCe
<https://developer.bling.com.br/changelogs#2023-v292>

Alterada a ordenação das obtenções de NFe (GET /nfe) e NFCes (GET /nfce). A obtenção será ordenada pelas notas com emissão mais recente.\n Alteração da ordenação na obtenção de NFe e NFCe

## [changelog] Retorno vazio para rota GET de naturezas de operações
<https://developer.bling.com.br/changelogs#2023-v291>

Caso não haja naturezas de operações ativas cadastradas, será retornado um array vazio, na rota GET /naturezas-operacoes.\n Retorno vazio para rota GET de naturezas de operações

## [changelog] Liberação das rotas GET, PUT, POST e DELETE de remessas de logísticas
<https://developer.bling.com.br/changelogs#2023-v291>

Liberadas as rotas de GET /logisticas/remessas/{idRemessa}, GET /logisticas/{idLogistica}/remessas,\nPUT /logisticas/remessas/{idRemessa}, POST /logisticas/remessas e DELETE /logisticas/remessas/{idRemessa}.\n Liberação das rotas GET, PUT, POST e DELETE de remessas de logísticas

## [changelog] Adicionadas rotas para geração de nota fiscal eletrônica a partir de pedidos de vendas
<https://developer.bling.com.br/changelogs#2023-v291>

Adicionadas rotas de POST /pedidos/vendas/{idPedidoVenda}/gerar-nfe e POST /pedidos/vendas/{idPedidoVenda}/gerar-nfce.\n Adicionadas rotas para geração de nota fiscal eletrônica a partir de pedidos de vendas

## [changelog] Adicionados filtros por datas de inclusão e alteração na API de contatos
<https://developer.bling.com.br/changelogs#2023-v291>

Adicionados filtros de data inicial e final de inclusão e alteração na obtenção de contatos.\n Adicionados filtros por datas de inclusão e alteração na API de contatos

## [changelog] Adicionados campos referentes a taxas de marketplace em pedidos de vendas
<https://developer.bling.com.br/changelogs#2023-v291>

Adicionados campos de taxas de marketplace (taxaComissao, custoFrete e valorBase) no GET, POST e PUT de pedidos de vendas.\n Adicionados campos referentes a taxas de marketplace em pedidos de vendas

## [changelog] Adicionados escopos para a API de campos customizados
<https://developer.bling.com.br/changelogs#2023-v291>

Adicionados escopos de &quot;Gerenciar Campos Customizados&quot; e &quot;Exclusão de Campos Customizados&quot; para a API de campos customizados.\n Adicionados escopos para a API de campos customizados

## [changelog] Alteração no filtro por IDs de vendas na rota de obtenção de etiquetas
<https://developer.bling.com.br/changelogs#2023-v291>

A partir da versão 293, não será aceito o envio do filtro\nidsVendas pelo body. Somente será aceito via query parameters como indica a documentação.\n Alteração no filtro por IDs de vendas na rota de obtenção de etiquetas

## [changelog] Correcão no filtro da página do endpoint GET/contas/pagar da V3
<https://developer.bling.com.br/changelogs#2023-v291>

Correcão no filtro da página do endpoint GET/contas/pagar para trazer novos registros em uma nova página, ao invés de mudar apenas o primeiro item.\n Correcão no filtro da página do endpoint GET/contas/pagar da V3

## [changelog] Liberação das rotas GET, PUT, POST e PATCH de serviços de logísticas
<https://developer.bling.com.br/changelogs#2023-v289>

Liberadas as rotas de GET /logisticas/servicos, GET /logisticas/servicos/{idServicoLogistica}, PUT /logisticas/servicos/{idServicoLogistica}, POST /logisticas/servicos e PATCH /logisticas/servicos/{idServicoLogistica}/situacoes.\n Liberação das rotas GET, PUT, POST e PATCH de serviços de logísticas

## [changelog] Paginação na rota de busca de NFes
<https://developer.bling.com.br/changelogs#2023-v289>

Ajuste para que os filtros &quot;limite&quot; e &quot;pagina&quot; sejam respeitados ao obter todas as NFes por meio do endpoint GET /nfe.\n Paginação na rota de busca de NFes

## [changelog] Liberação das rotas de objetos de postagem de logística
<https://developer.bling.com.br/changelogs#2023-v289>

Liberadas as rotas de PUT /logisticas/objetos/{idObjeto}, POST /logisticas/objetos e\nDELETE /logisticas/objetos/{idObjeto}.\n Liberação das rotas de objetos de postagem de logística

## [changelog] Liberação da rota GET de etiquetas de logística
<https://developer.bling.com.br/changelogs#2023-v289>

Liberada para uso a rota de GET /logisticas/etiquetas.\n Liberação da rota GET de etiquetas de logística

## [changelog] Novas rotas para lançamento e estorno de contas por NF-e e NFC-e
<https://developer.bling.com.br/changelogs#2023-v289>

Adição das funcionalidades de lançar e estornar contas por meio de uma NF-e ou NFC-e.\n Novas rotas para lançamento e estorno de contas por NF-e e NFC-e

## [changelog] Liberação da rota GET e escopo de dados básicos da empresa
<https://developer.bling.com.br/changelogs#2023-v289>

Liberada para uso a rota de GET /empresas/me/dados-basicos e escopo, &quot;Visualizar os dados básicos da empresa&quot;, para cadastro de aplicativos.\n Liberação da rota GET e escopo de dados básicos da empresa

## [changelog] Correção de erro interno da API de etiquetas utilizando OAuth2
<https://developer.bling.com.br/changelogs#2023-v289>

Foi ajustado o erro que acontecia ao solicitar uma etiqueta pela rota /logisticas/etiquetas estando autenticado via\nOAuth2.\n Correção de erro interno da API de etiquetas utilizando OAuth2

## [changelog] Aumento do limite de caracteres da URL de redirecionamento do aplicativo
<https://developer.bling.com.br/changelogs#2023-v288>

Permite configurar a URL de redirecionamento do aplicativo com até 350 caracteres.\n Aumento do limite de caracteres da URL de redirecionamento do aplicativo

## [changelog] Alteração da estrutura de campos customizados no POST/PUT de Produto
<https://developer.bling.com.br/changelogs#2023-v288>

Simplifica a estrutura de campos customizados removendo o aninhamento do campo vínculo, corrigindo, também, a associação de novos campos customizados a produtos.\n Alteração da estrutura de campos customizados no POST/PUT de Produto

## [changelog] Rota para exclusão de múltiplas notas fiscais
<https://developer.bling.com.br/changelogs#2023-v287>

Nova rota DELETE para exclusão de múltiplas notas fiscais.\n Rota para exclusão de múltiplas notas fiscais

## [changelog] Liberação das rotas POST, PUT e DELETE de logísticas
<https://developer.bling.com.br/changelogs#2023-v287>

Liberadas as rotas de POST /logisticas, PUT /logisticas e DELETE /logisticas.\n Liberação das rotas POST, PUT e DELETE de logísticas

## [changelog] Adição da propriedade actionEstoque no PUT de Produto
<https://developer.bling.com.br/changelogs#2023-v286>

A propriedade actionEstoque é útil ao transformar um produto Simples para Variação, nesse caso é necessário informar a ação.\n Adição da propriedade actionEstoque no PUT de Produto

## [changelog] Remoção da propriedade atributos no PUT/POST de Produto
<https://developer.bling.com.br/changelogs#2023-v286>

A propriedade não possuí utilidade para as ações de gravar e atualizar e não precisa ser exibida ou enviada no payload.\n Remoção da propriedade atributos no PUT/POST de Produto

## [changelog] Nova API de contas a pagar
<https://developer.bling.com.br/changelogs#2023-v285>

Nova API de contas a pagar disponibilizada.\n Nova API de contas a pagar

## [changelog] Nova API de contas a receber
<https://developer.bling.com.br/changelogs#2023-v285>

Nova API de contas a receber disponibilizada.\n Nova API de contas a receber

## [changelog] Nova API de borderôs
<https://developer.bling.com.br/changelogs#2023-v285>

Nova API de borderôs disponibilizada.\n Nova API de borderôs

## [changelog] Liberação das rotas GET de logísticas
<https://developer.bling.com.br/changelogs#2023-v284>

Liberadas as rotas de GET /logisticas e GET /logisticas/{idLogistica}.\n Liberação das rotas GET de logísticas

## [changelog] Filtro de limite em pedidos de compras
<https://developer.bling.com.br/changelogs#2023-v284>

Ajuste para que o filtro &quot;limite&quot; seja respeitado ao obter todos pedidos de compras por meio do endpoint GET /pedidos/compras.\n Filtro de limite em pedidos de compras

## [changelog] Liberação da API v3
<https://developer.bling.com.br/changelogs#2023-v278>

Liberado o uso da API v3, para mais informações acesse a documentação do cadastro de aplicativos.\n Liberação da API v3

## [reference] /anuncios/categorias
<https://developer.bling.com.br/referencia#/An%C3%BAncios%20-%20Categorias/get_anuncios_categorias>

Obtém categorias de anúncios.

## [reference] /anuncios/categorias/{idCategoria}
<https://developer.bling.com.br/referencia#/An%C3%BAncios%20-%20Categorias/get_anuncios_categorias__idCategoria_>

Obtém uma categoria de anúncio pelo ID.

## [reference] /anuncios
<https://developer.bling.com.br/referencia#/An%C3%BAncios/get_anuncios>

Obtém anúncios paginados.

## [reference] /anuncios
<https://developer.bling.com.br/referencia#/An%C3%BAncios/post_anuncios>

Cria um anúncio.

## [reference] /anuncios/{idAnuncio}
<https://developer.bling.com.br/referencia#/An%C3%BAncios/get_anuncios__idAnuncio_>

Obtém os detalhes de um anúncio específico pelo seu ID.

## [reference] /anuncios/{idAnuncio}
<https://developer.bling.com.br/referencia#/An%C3%BAncios/put_anuncios__idAnuncio_>

Altera um anúncio pelo ID.

## [reference] /anuncios/{idAnuncio}
<https://developer.bling.com.br/referencia#/An%C3%BAncios/delete_anuncios__idAnuncio_>

Remove um anúncio pelo ID.

## [reference] /anuncios/{idAnuncio}/publicar
<https://developer.bling.com.br/referencia#/An%C3%BAncios/post_anuncios__idAnuncio__publicar>

Altera o status do anúncio para publicado.

## [reference] /anuncios/{idAnuncio}/pausar
<https://developer.bling.com.br/referencia#/An%C3%BAncios/post_anuncios__idAnuncio__pausar>

Altera o status do anúncio para pausado.

## [reference] /borderos/{idBordero}
<https://developer.bling.com.br/referencia#/Border%C3%B4s/get_borderos__idBordero_>

Obtém um borderô pelo ID.

## [reference] /borderos/{idBordero}
<https://developer.bling.com.br/referencia#/Border%C3%B4s/delete_borderos__idBordero_>

Remove um borderô pelo ID.

## [reference] /campos-customizados/modulos
<https://developer.bling.com.br/referencia#/Campos%20Customizados/get_campos_customizados_modulos>

Obtém módulos que possuem campos customizados.

## [reference] /campos-customizados/tipos
<https://developer.bling.com.br/referencia#/Campos%20Customizados/get_campos_customizados_tipos>

Obtém tipos de campos customizados.

## [reference] /campos-customizados/modulos/{idModulo}
<https://developer.bling.com.br/referencia#/Campos%20Customizados/get_campos_customizados_modulos__idModulo_>

Obtém campos customizados por módulo paginados.

## [reference] /campos-customizados/{idCampoCustomizado}
<https://developer.bling.com.br/referencia#/Campos%20Customizados/get_campos_customizados__idCampoCustomizado_>

Obtém um campo customizado pelo ID.

## [reference] /campos-customizados/{idCampoCustomizado}
<https://developer.bling.com.br/referencia#/Campos%20Customizados/put_campos_customizados__idCampoCustomizado_>

Altera um campo customizado pelo ID.

## [reference] /campos-customizados/{idCampoCustomizado}
<https://developer.bling.com.br/referencia#/Campos%20Customizados/delete_campos_customizados__idCampoCustomizado_>

Remove um campo customizado pelo ID.

## [reference] /campos-customizados
<https://developer.bling.com.br/referencia#/Campos%20Customizados/post_campos_customizados>

Cria um campo customizado.

## [reference] /campos-customizados/{idCampoCustomizado}/situacoes
<https://developer.bling.com.br/referencia#/Campos%20Customizados/patch_campos_customizados__idCampoCustomizado__situacoes>

Altera a situação de um campo customizado pelo ID.

## [reference] /categorias/lojas
<https://developer.bling.com.br/referencia#/Categorias%20-%20Lojas/get_categorias_lojas>

Obtém categorias de lojas virtuais vinculadas a de produtos paginadas.

## [reference] /categorias/lojas
<https://developer.bling.com.br/referencia#/Categorias%20-%20Lojas/post_categorias_lojas>

Cria o vínculo de uma categoria da loja com a de produto.

## [reference] /categorias/lojas/{idCategoriaLoja}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Lojas/get_categorias_lojas__idCategoriaLoja_>

Obtém uma categoria da loja vinculada a de produto pelo ID.

## [reference] /categorias/lojas/{idCategoriaLoja}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Lojas/put_categorias_lojas__idCategoriaLoja_>

Altera o vínculo de uma categoria da loja com a de produto pelo ID.

## [reference] /categorias/lojas/{idCategoriaLoja}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Lojas/delete_categorias_lojas__idCategoriaLoja_>

Remove o vínculo de uma categoria da loja com a de produto pelo ID.

## [reference] /categorias/produtos
<https://developer.bling.com.br/referencia#/Categorias%20-%20Produtos/get_categorias_produtos>

Obtém categorias de produtos paginadas.

## [reference] /categorias/produtos
<https://developer.bling.com.br/referencia#/Categorias%20-%20Produtos/post_categorias_produtos>

Cria uma categoria de produto.

## [reference] /categorias/produtos/{idCategoriaProduto}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Produtos/get_categorias_produtos__idCategoriaProduto_>

Obtém uma categoria de produto pelo ID.

## [reference] /categorias/produtos/{idCategoriaProduto}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Produtos/put_categorias_produtos__idCategoriaProduto_>

Altera uma categoria de produto pelo ID.

## [reference] /categorias/produtos/{idCategoriaProduto}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Produtos/delete_categorias_produtos__idCategoriaProduto_>

Remove uma categoria de produto pelo ID.

## [reference] /categorias/receitas-despesas
<https://developer.bling.com.br/referencia#/Categorias%20-%20Receitas%20e%20Despesas/get_categorias_receitas_despesas>

Obtém categorias de receitas e despesas paginadas.

## [reference] /categorias/receitas-despesas
<https://developer.bling.com.br/referencia#/Categorias%20-%20Receitas%20e%20Despesas/post_categorias_receitas_despesas>

Cria uma categoria de receita e despesa.

## [reference] /categorias/receitas-despesas
<https://developer.bling.com.br/referencia#/Categorias%20-%20Receitas%20e%20Despesas/delete_categorias_receitas_despesas>

Remove múltiplas categorias de receita e despesa a partir de uma lista de IDs.

## [reference] /categorias/receitas-despesas/{idCategoria}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Receitas%20e%20Despesas/get_categorias_receitas_despesas__idCategoria_>

Obtém uma categoria de receita e despesa pelo ID.

## [reference] /categorias/receitas-despesas/{idCategoria}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Receitas%20e%20Despesas/put_categorias_receitas_despesas__idCategoria_>

Atualiza uma categoria de receita e despesa a partir do ID.

## [reference] /categorias/receitas-despesas/{idCategoria}
<https://developer.bling.com.br/referencia#/Categorias%20-%20Receitas%20e%20Despesas/delete_categorias_receitas_despesas__idCategoria_>

Remove uma categoria de receita e despesa pelo ID.

## [reference] /contas-contabeis
<https://developer.bling.com.br/referencia#/Contas%20Financeiras/get_contas_contabeis>

Obtém contas financeiras paginadas.

## [reference] /contas-contabeis/{idContaContabil}
<https://developer.bling.com.br/referencia#/Contas%20Financeiras/get_contas_contabeis__idContaContabil_>

Obtém uma conta financeira pelo ID.

## [reference] /contas/receber
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/get_contas_receber>

Obtém contas a receber paginadas.

## [reference] /contas/receber
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/post_contas_receber>

Cria uma conta a receber.

## [reference] /contas/receber/{idContaReceber}
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/get_contas_receber__idContaReceber_>

Obtém uma conta a receber pelo ID.

## [reference] /contas/receber/{idContaReceber}
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/put_contas_receber__idContaReceber_>

Altera uma conta a receber pelo ID.

## [reference] /contas/receber/{idContaReceber}
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/delete_contas_receber__idContaReceber_>

Remove uma conta a receber pelo ID.

## [reference] /contas/receber/{idContaReceber}/baixar
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/post_contas_receber__idContaReceber__baixar>

Cria o recebimento de uma conta a receber.

## [reference] /contas/receber/boletos
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/get_contas_receber_boletos>

Obtém os boletos vinculados a um idOrigem, o qual corresponde ao ID de uma venda ou nota fiscal.

## [reference] /contas/receber/boletos/cancelar
<https://developer.bling.com.br/referencia#/Contas%20a%20Receber/post_contas_receber_boletos_cancelar>

Cancela um ou todos os boletos em aberto vinculados a uma venda ou nota fiscal.

## [reference] /contatos
<https://developer.bling.com.br/referencia#/Contatos/get_contatos>

Obtém contatos paginados.

## [reference] /contatos
<https://developer.bling.com.br/referencia#/Contatos/post_contatos>

Cria um contato.

## [reference] /contatos
<https://developer.bling.com.br/referencia#/Contatos/delete_contatos>

Remove múltiplos contatos pelos IDs.

## [reference] /contatos/{idContato}
<https://developer.bling.com.br/referencia#/Contatos/get_contatos__idContato_>

Obtém um contato pelo ID.

## [reference] /contatos/{idContato}
<https://developer.bling.com.br/referencia#/Contatos/put_contatos__idContato_>

Altera um contato pelo ID.

## [reference] /contatos/{idContato}
<https://developer.bling.com.br/referencia#/Contatos/delete_contatos__idContato_>

Remove um contato pelo ID.

## [reference] /contatos/{idContato}/tipos
<https://developer.bling.com.br/referencia#/Contatos/get_contatos__idContato__tipos>

Obtém os tipos de contato de um contato pelo ID.

## [reference] /contatos/consumidor-final
<https://developer.bling.com.br/referencia#/Contatos/get_contatos_consumidor_final>

Obtém os dados do contato Consumidor Final. O consumidor final é um contato padrão do sistema que é criado automaticamente e não pode ser alterado.

## [reference] /contatos/{idContato}/situacoes
<https://developer.bling.com.br/referencia#/Contatos/patch_contatos__idContato__situacoes>

Altera a situação de um contato pelo ID.

## [reference] /contatos/situacoes
<https://developer.bling.com.br/referencia#/Contatos/post_contatos_situacoes>

Altera a situação de múltiplos contatos pelos IDs.

## [reference] /contatos/tipos
<https://developer.bling.com.br/referencia#/Contatos%20-%20Tipos/get_contatos_tipos>

Obtém tipos de contato pelo ID.

## [reference] /contratos
<https://developer.bling.com.br/referencia#/Contratos/get_contratos>

Obtém contratos paginados.

## [reference] /contratos
<https://developer.bling.com.br/referencia#/Contratos/post_contratos>

Cria um contrato.

## [reference] /contratos/{idContrato}
<https://developer.bling.com.br/referencia#/Contratos/get_contratos__idContrato_>

Obtém um contrato pelo ID.

## [reference] /contratos/{idContrato}
<https://developer.bling.com.br/referencia#/Contratos/put_contratos__idContrato_>

Altera um contrato pelo ID.

## [reference] /contratos/{idContrato}
<https://developer.bling.com.br/referencia#/Contratos/delete_contratos__idContrato_>

Remove um contrato pelo ID.

## [reference] /depositos
<https://developer.bling.com.br/referencia#/Dep%C3%B3sitos/get_depositos>

Obtém depósitos paginados.

## [reference] /depositos
<https://developer.bling.com.br/referencia#/Dep%C3%B3sitos/post_depositos>

Cria um depósito. Até 100 depósitos podem ser criados.

## [reference] /depositos/{idDeposito}
<https://developer.bling.com.br/referencia#/Dep%C3%B3sitos/get_depositos__idDeposito_>

Obtém um depósito pelo ID.

## [reference] /depositos/{idDeposito}
<https://developer.bling.com.br/referencia#/Dep%C3%B3sitos/put_depositos__idDeposito_>

Altera um depósito pelo ID.

## [reference] /empresas/me/dados-basicos
<https://developer.bling.com.br/referencia#/Empresas/get_empresas_me_dados_basicos>

Obtém CNPJ, razão social e e-mail da empresa.

## [reference] /estoques/saldos/{idDeposito}
<https://developer.bling.com.br/referencia#/Estoques/get_estoques_saldos__idDeposito_>

Obtém o saldo em estoque de produtos pelo ID do depósito.

## [reference] /estoques/saldos
<https://developer.bling.com.br/referencia#/Estoques/get_estoques_saldos>

Obtém o saldo em estoque de produtos, em todos os depósitos.

## [reference] /estoques
<https://developer.bling.com.br/referencia#/Estoques/post_estoques>

Cria um registro de estoque.

## [reference] /estoques/{idEstoque}
<https://developer.bling.com.br/referencia#/Estoques/put_estoques__idEstoque_>

Altera um registro de estoque pelo ID.

## [reference] /produtos/lotes
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/get_produtos_lotes>

Obtém lotes de produtos paginados.

## [reference] /produtos/lotes
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/put_produtos_lotes>

Cria/altera lotes de produtos.

## [reference] /produtos/lotes
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/delete_produtos_lotes>

Remove lotes de produtos pelos IDs.

## [reference] /produtos/lotes/{idLote}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/get_produtos_lotes__idLote_>

Obtém um lote de um produto pelo ID.

## [reference] /produtos/lotes/{idLote}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/put_produtos_lotes__idLote_>

Altera um lote de um produto pelo ID.

## [reference] /produtos/lotes/controla-lote
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/get_produtos_lotes_controla_lote>

Obtém a informação se determinados produtos possuem controle de lote.

## [reference] /produtos/{idProduto}/lotes/controla-lote/desativar
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/post_produtos__idProduto__lotes_controla_lote_desativar>

Desativa controle de lotes para o produto pelo ID do produto.

## [reference] /produtos/lotes/{idLote}/status
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes/patch_produtos_lotes__idLote__status>

Altera o status de um lote do produto pelo ID.

## [reference] /produtos/lotes/{idLote}/lancamentos
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/get_produtos_lotes__idLote__lancamentos>

Obtém os lançamentos de um lote de produto pelo ID.

## [reference] /produtos/lotes/{idLote}/lancamentos
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/post_produtos_lotes__idLote__lancamentos>

Inclui lançamento de um lote.

## [reference] /produtos/lotes/lancamentos/{idLancamento}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/get_produtos_lotes_lancamentos__idLancamento_>

Obtém um lançamento de um lote de produto pelo ID do lançamento.

## [reference] /produtos/lotes/lancamentos/{idLancamento}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/patch_produtos_lotes_lancamentos__idLancamento_>

Altera a observação de um lançamento de um lote de um produto pelo ID do lançamento.

## [reference] /produtos/{idProduto}/lotes/{idLote}/depositos/{idDeposito}/saldo
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/get_produtos__idProduto__lotes__idLote__depositos__idDeposito__saldo>

Obtém o saldo de um lote de produto.

## [reference] /produtos/{idProduto}/lotes/depositos/{idDeposito}/saldo
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/get_produtos__idProduto__lotes_depositos__idDeposito__saldo>

Obtém os saldos dos lotes de um produto por depósito.

## [reference] /produtos/{idProduto}/lotes/depositos/{idDeposito}/saldo/soma
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/get_produtos__idProduto__lotes_depositos__idDeposito__saldo_soma>

Obtém a soma dos saldos dos lotes de um produto em um depósito.

## [reference] /produtos/{idProduto}/lotes/saldo/soma
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lotes%20Lan%C3%A7amentos/get_produtos__idProduto__lotes_saldo_soma>

Obtém o saldo total dos lotes de um produto pelo ID do produto.

## [reference] /formas-pagamentos
<https://developer.bling.com.br/referencia#/Formas%20de%20Pagamentos/get_formas_pagamentos>

Obtém formas de pagamentos paginadas.

## [reference] /formas-pagamentos
<https://developer.bling.com.br/referencia#/Formas%20de%20Pagamentos/post_formas_pagamentos>

Cria uma forma de pagamento.

## [reference] /formas-pagamentos/{idFormaPagamento}
<https://developer.bling.com.br/referencia#/Formas%20de%20Pagamentos/get_formas_pagamentos__idFormaPagamento_>

Obtém uma forma de pagamento pelo ID.

## [reference] /formas-pagamentos/{idFormaPagamento}
<https://developer.bling.com.br/referencia#/Formas%20de%20Pagamentos/put_formas_pagamentos__idFormaPagamento_>

Altera uma forma de pagamento pelo ID.

## [reference] /formas-pagamentos/{idFormaPagamento}
<https://developer.bling.com.br/referencia#/Formas%20de%20Pagamentos/delete_formas_pagamentos__idFormaPagamento_>

Remove uma forma de pagamento pelo ID.

## [reference] /formas-pagamentos/{idFormaPagamento}/padrao
<https://developer.bling.com.br/referencia#/Formas%20de%20Pagamentos/patch_formas_pagamentos__idFormaPagamento__padrao>

Altera o padrão de uma forma de pagamento pelo ID.

## [reference] /formas-pagamentos/{idFormaPagamento}/situacao
<https://developer.bling.com.br/referencia#/Formas%20de%20Pagamentos/patch_formas_pagamentos__idFormaPagamento__situacao>

Altera a situação de uma forma de pagamento pelo ID.

## [reference] /homologacao/produtos
<https://developer.bling.com.br/referencia#/Homologa%C3%A7%C3%A3o/get_homologacao_produtos>

Obtém o produto que será utilizado durante os demais passos da homologação, e, inicia o processo de validação, o qual deve ser acompanhando via interface do cadastro de aplicativos.

## [reference] /homologacao/produtos
<https://developer.bling.com.br/referencia#/Homologa%C3%A7%C3%A3o/post_homologacao_produtos>

Cria o produto da homologação.

## [reference] /homologacao/produtos/{idProdutoHomologacao}
<https://developer.bling.com.br/referencia#/Homologa%C3%A7%C3%A3o/put_homologacao_produtos__idProdutoHomologacao_>

Altera o produto da homologação pelo ID.

## [reference] /homologacao/produtos/{idProdutoHomologacao}
<https://developer.bling.com.br/referencia#/Homologa%C3%A7%C3%A3o/delete_homologacao_produtos__idProdutoHomologacao_>

Remove o produto da homologação pelo ID.

## [reference] /homologacao/produtos/{idProdutoHomologacao}/situacoes
<https://developer.bling.com.br/referencia#/Homologa%C3%A7%C3%A3o/patch_homologacao_produtos__idProdutoHomologacao__situacoes>

Altera a situação do produto da homologação pelo ID.

## [reference] /listas-precos
<https://developer.bling.com.br/referencia#/Listas%20de%20Pre%C3%A7os/get_listas_precos>

Obtém listas de preços paginadas. O fator customizado (preço negociado, listas do tipo Customizada) não é exposto por este endpoint.

## [reference] /listas-precos/{idListaPreco}
<https://developer.bling.com.br/referencia#/Listas%20de%20Pre%C3%A7os/get_listas_precos__idListaPreco_>

Obtém uma lista de preço pelo ID. O fator customizado (preço negociado, listas do tipo Customizada) não é exposto por este endpoint.

## [reference] /logisticas
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas/get_logisticas>

Obtém logísticas paginados.

## [reference] /logisticas
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas/post_logisticas>

Cria uma logística.

## [reference] /logisticas/{idLogistica}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas/get_logisticas__idLogistica_>

Obtém uma logística pelo ID.

## [reference] /logisticas/{idLogistica}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas/put_logisticas__idLogistica_>

Altera uma logística pelo ID.

## [reference] /logisticas/{idLogistica}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas/delete_logisticas__idLogistica_>

Remove uma logística pelo ID.

## [reference] /logisticas/servicos
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Servi%C3%A7os/get_logisticas_servicos>

Obtém serviços de logísticas paginados.

## [reference] /logisticas/servicos
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Servi%C3%A7os/post_logisticas_servicos>

Cria um serviço de logística personalizada.

## [reference] /logisticas/servicos/{idLogisticaServico}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Servi%C3%A7os/get_logisticas_servicos__idLogisticaServico_>

Obtém um servico de logística pelo ID.

## [reference] /logisticas/servicos/{idLogisticaServico}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Servi%C3%A7os/put_logisticas_servicos__idLogisticaServico_>

Altera dados de um serviço de logística personalizada pelo ID.

## [reference] /logisticas/{idLogisticaServico}/situacoes
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Servi%C3%A7os/patch_logisticas__idLogisticaServico__situacoes>

Desativa ou ativa um serviço de uma logística personalizada pelo ID.

## [reference] /logisticas/objetos/{idObjeto}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Objetos/get_logisticas_objetos__idObjeto_>

Obtém um objeto de logística pelo ID.

## [reference] /logisticas/objetos/{idObjeto}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Objetos/put_logisticas_objetos__idObjeto_>

Altera dados de um objeto de logística personalizada pelo ID.

## [reference] /logisticas/objetos/{idObjeto}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Objetos/delete_logisticas_objetos__idObjeto_>

Remove um objeto de logística personalizada que não esteja em uma PLP.

## [reference] /logisticas/objetos
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Objetos/post_logisticas_objetos>

Cria um objeto de logística personalizada.

## [reference] /logisticas/etiquetas
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Etiquetas/get_logisticas_etiquetas>

Obtém as etiquetas dos pedidos de venda a partir dos ID's dos pedidos. No momento, o filtro está limitado para apenas um ID.

## [reference] /logisticas/remessas/{idRemessa}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Remessas/get_logisticas_remessas__idRemessa_>

Obtém uma remessa de postagem pelo ID.

## [reference] /logisticas/remessas/{idRemessa}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Remessas/put_logisticas_remessas__idRemessa_>

Altera uma remessa de postagem pelo ID.

## [reference] /logisticas/remessas/{idRemessa}
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Remessas/delete_logisticas_remessas__idRemessa_>

Remove uma remessa de postagem pelo ID.

## [reference] /logisticas/{idLogistica}/remessas
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Remessas/get_logisticas__idLogistica__remessas>

Obtém as remessas de postagem de uma logística pelo ID.

## [reference] /logisticas/remessas
<https://developer.bling.com.br/referencia#/Log%C3%ADsticas%20-%20Remessas/post_logisticas_remessas>

Cria uma remessa de postagem de uma logística.

## [reference] /naturezas-operacoes
<https://developer.bling.com.br/referencia#/Naturezas%20de%20Opera%C3%A7%C3%B5es/get_naturezas_operacoes>

Obtém naturezas de operação paginadas.

## [reference] /naturezas-operacoes/{idNaturezaOperacao}/obter-tributacao
<https://developer.bling.com.br/referencia#/Naturezas%20de%20Opera%C3%A7%C3%B5es/post_naturezas_operacoes__idNaturezaOperacao__obter_tributacao>

Obtém regras de tributação que incidem sobre o item, dada uma natureza de operação.

## [reference] /nfce
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/get_nfce>

Obtém notas fiscais de consumidor paginadas.

## [reference] /nfce
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/post_nfce>

Cria uma nota fiscal de consumidor.

## [reference] /nfce/{idNotaFiscalConsumidor}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/get_nfce__idNotaFiscalConsumidor_>

Obtém uma nota fiscal de consumidor pelo ID.

## [reference] /nfce/{idNotaFiscalConsumidor}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/put_nfce__idNotaFiscalConsumidor_>

Altera uma nota fiscal de consumidor.

## [reference] /nfce/{idNotaFiscalConsumidor}/enviar
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/post_nfce__idNotaFiscalConsumidor__enviar>

Envia uma nota de consumidor pelo ID para emissão na Sefaz.

## [reference] /nfce/{idNotaFiscalConsumidor}/lancar-contas
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/post_nfce__idNotaFiscalConsumidor__lancar_contas>

Lança as contas de uma nota fiscal pelo ID.

## [reference] /nfce/{idNotaFiscalConsumidor}/estornar-contas
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/post_nfce__idNotaFiscalConsumidor__estornar_contas>

Estorna as contas de uma nota fiscal pelo ID.

## [reference] /nfce/{idNotaFiscalConsumidor}/lancar-estoque
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/post_nfce__idNotaFiscalConsumidor__lancar_estoque>

Lança o estoque de uma nota fiscal pelo ID, no depósito padrão.

## [reference] /nfce/{idNotaFiscalConsumidor}/lancar-estoque/{idDeposito}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/post_nfce__idNotaFiscalConsumidor__lancar_estoque__idDeposito_>

Lança o estoque de uma nota fiscal pelo ID, especificando o ID do depósito.

## [reference] /nfce/{idNotaFiscalConsumidor}/estornar-estoque
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Consumidor%20Eletr%C3%B4nicas/post_nfce__idNotaFiscalConsumidor__estornar_estoque>

Estorna o estoque de uma nota fiscal pelo ID.

## [reference] /nfe
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/get_nfe>

Obtém notas fiscais paginadas.

## [reference] /nfe
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/post_nfe>

Cria uma nota fiscal.

## [reference] /nfe
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/delete_nfe>

Remove múltiplas notas fiscais por IDs.

## [reference] /nfe/{idNotaFiscal}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/get_nfe__idNotaFiscal_>

Obtém uma nota fiscal pelo ID.

## [reference] /nfe/{idNotaFiscal}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/put_nfe__idNotaFiscal_>

Altera uma nota fiscal pelo ID. Notas com vínculos possuem restrições de atualização. Notas autorizadas não podem ter dados fiscais alterados: valores, impostos, informações do destinatário e qualquer outro dado transmitido no XML da nota.

## [reference] /nfe/{idNotaFiscal}/enviar
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/post_nfe__idNotaFiscal__enviar>

Envia uma nota fiscal pelo ID para emissão na Sefaz.

## [reference] /nfe/{idNotaFiscal}/lancar-contas
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/post_nfe__idNotaFiscal__lancar_contas>

Lança as contas de uma nota fiscal pelo ID.

## [reference] /nfe/{idNotaFiscal}/estornar-contas
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/post_nfe__idNotaFiscal__estornar_contas>

Estorna as contas de uma nota fiscal pelo ID.

## [reference] /nfe/{idNotaFiscal}/lancar-estoque
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/post_nfe__idNotaFiscal__lancar_estoque>

Lança o estoque de uma nota fiscal pelo ID, no depósito padrão.

## [reference] /nfe/{idNotaFiscal}/lancar-estoque/{idDeposito}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/post_nfe__idNotaFiscal__lancar_estoque__idDeposito_>

Lança o estoque de uma nota fiscal pelo ID, especificando o ID do depósito.

## [reference] /nfe/{idNotaFiscal}/estornar-estoque
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/post_nfe__idNotaFiscal__estornar_estoque>

Estorna o estoque de uma nota fiscal pelo ID.

## [reference] /nfe/documento/{chaveAcesso}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20Eletr%C3%B4nicas/get_nfe_documento__chaveAcesso_>

Obtém o PDF ou XML de uma nota fiscal pela chave de acesso. O formato desejado deve ser informado via query param.

## [reference] /nfse
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/get_nfse>

Obtém notas de serviços paginadas.

## [reference] /nfse
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/post_nfse>

Cria uma nota de serviço.

## [reference] /nfse/{idNotaServico}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/get_nfse__idNotaServico_>

Obtém uma nota de serviço pelo ID.

## [reference] /nfse/{idNotaServico}
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/delete_nfse__idNotaServico_>

Exclui uma nota de serviço pelo ID.

## [reference] /nfse/{idNotaServico}/enviar
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/post_nfse__idNotaServico__enviar>

Envia uma nota de serviço pelo ID.

## [reference] /nfse/{idNotaServico}/cancelar
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/post_nfse__idNotaServico__cancelar>

Cancela uma nota de serviço pelo ID.

## [reference] /nfse/configuracoes
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/get_nfse_configuracoes>

Obtém todas as configurações de nota de serviço.

## [reference] /nfse/configuracoes
<https://developer.bling.com.br/referencia#/Notas%20Fiscais%20de%20Servi%C3%A7o%20Eletr%C3%B4nicas/put_nfse_configuracoes>

Cria e altera configurações para emissão de notas de serviço.

## [reference] /notificacoes
<https://developer.bling.com.br/referencia#/Notifica%C3%A7%C3%B5es/get_notificacoes>

Obtém todas as notificações de uma empresa no período informado. Caso período não seja informado, será considerado o ano atual.

## [reference] /notificacoes/{idNotificacao}/confirmar-leitura
<https://developer.bling.com.br/referencia#/Notifica%C3%A7%C3%B5es/post_notificacoes__idNotificacao__confirmar_leitura>

Marca a notificação relacionada à empresa como lida.

## [reference] /notificacoes/quantidade
<https://developer.bling.com.br/referencia#/Notifica%C3%A7%C3%B5es/get_notificacoes_quantidade>

Obtém a quantidade de notificações de uma empresa no período informado. Caso período não seja informado, será considerado o ano atual.

## [reference] /propostas-comerciais
<https://developer.bling.com.br/referencia#/Propostas%20Comerciais/get_propostas_comerciais>

Obtém propostas comerciais paginadas.

## [reference] /propostas-comerciais
<https://developer.bling.com.br/referencia#/Propostas%20Comerciais/post_propostas_comerciais>

Cria uma proposta comercial.

## [reference] /propostas-comerciais
<https://developer.bling.com.br/referencia#/Propostas%20Comerciais/delete_propostas_comerciais>

Remove múltiplas propostas comerciais pelos IDs.

## [reference] /propostas-comerciais/{idPropostaComercial}
<https://developer.bling.com.br/referencia#/Propostas%20Comerciais/get_propostas_comerciais__idPropostaComercial_>

Obtém uma proposta comercial pelo ID.

## [reference] /propostas-comerciais/{idPropostaComercial}
<https://developer.bling.com.br/referencia#/Propostas%20Comerciais/put_propostas_comerciais__idPropostaComercial_>

Altera uma proposta comercial pelo ID.

## [reference] /propostas-comerciais/{idPropostaComercial}
<https://developer.bling.com.br/referencia#/Propostas%20Comerciais/delete_propostas_comerciais__idPropostaComercial_>

Remove uma proposta comercial pelo ID.

## [reference] /propostas-comerciais/{idPropostaComercial}/situacoes
<https://developer.bling.com.br/referencia#/Propostas%20Comerciais/patch_propostas_comerciais__idPropostaComercial__situacoes>

Altera a situação de uma proposta comercial pelo ID.

## [reference] /pedidos/compras
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/get_pedidos_compras>

Obtém pedidos de compras paginados.

## [reference] /pedidos/compras
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/post_pedidos_compras>

Cria um pedido de compra.

## [reference] /pedidos/compras/{idPedidoCompra}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/get_pedidos_compras__idPedidoCompra_>

Obtém um pedido de compra pelo ID.

## [reference] /pedidos/compras/{idPedidoCompra}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/put_pedidos_compras__idPedidoCompra_>

Altera um pedido de compra pelo ID.

## [reference] /pedidos/compras/{idPedidoCompra}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/delete_pedidos_compras__idPedidoCompra_>

Remove um pedido de compra pelo ID.

## [reference] /pedidos/compras/{idPedidoCompra}/situacoes/{idSituacao}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/patch_pedidos_compras__idPedidoCompra__situacoes__idSituacao_>

Altera a situação de um pedido de compra pelo ID.

## [reference] /pedidos/compras/{idPedidoCompra}/lancar-contas
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/post_pedidos_compras__idPedidoCompra__lancar_contas>

Lança as contas de um pedido de compra pelo ID.

## [reference] /pedidos/compras/{idPedidoCompra}/estornar-contas
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/post_pedidos_compras__idPedidoCompra__estornar_contas>

Estorna as contas de um pedido de compra pelo ID.

## [reference] /pedidos/compras/{idPedidoCompra}/lancar-estoque
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/post_pedidos_compras__idPedidoCompra__lancar_estoque>

Lança o estoque de um pedido de compra pelo ID.

## [reference] /pedidos/compras/{idPedidoCompra}/estornar-estoque
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Compras/post_pedidos_compras__idPedidoCompra__estornar_estoque>

Estorna o estoque de um pedido de compra pelo ID.

## [reference] /produtos/estruturas/{idProdutoEstrutura}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Estruturas/get_produtos_estruturas__idProdutoEstrutura_>

Obtém a estrutura de um produto com composição pelo ID.

## [reference] /produtos/estruturas/{idProdutoEstrutura}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Estruturas/put_produtos_estruturas__idProdutoEstrutura_>

Altera a estrutura de um produto com composição pelo ID.

## [reference] /produtos/estruturas/{idProdutoEstrutura}/componentes
<https://developer.bling.com.br/referencia#/Produtos%20-%20Estruturas/post_produtos_estruturas__idProdutoEstrutura__componentes>

Adiciona múltiplos componentes a uma estrutura pelo ID.

## [reference] /produtos/estruturas/{idProdutoEstrutura}/componentes
<https://developer.bling.com.br/referencia#/Produtos%20-%20Estruturas/delete_produtos_estruturas__idProdutoEstrutura__componentes>

Remove os componentes de um produto com composição pelos IDs dos componentes.

## [reference] /produtos/estruturas/{idProdutoEstrutura}/componentes/{idComponente}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Estruturas/patch_produtos_estruturas__idProdutoEstrutura__componentes__idComponente_>

Altera um componente de uma estrutura pelo ID.

## [reference] /produtos/estruturas
<https://developer.bling.com.br/referencia#/Produtos%20-%20Estruturas/delete_produtos_estruturas>

Remove a estrutura de múltiplos produtos com composição pelos IDs.

## [reference] /produtos/fornecedores
<https://developer.bling.com.br/referencia#/Produtos%20-%20Fornecedores/get_produtos_fornecedores>

Obtém produtos fornecedores paginados.

## [reference] /produtos/fornecedores
<https://developer.bling.com.br/referencia#/Produtos%20-%20Fornecedores/post_produtos_fornecedores>

Cria um produto fornecedor.

## [reference] /produtos/fornecedores/{idProdutoFornecedor}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Fornecedores/get_produtos_fornecedores__idProdutoFornecedor_>

Obtém um produto fornecedor pelo ID.

## [reference] /produtos/fornecedores/{idProdutoFornecedor}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Fornecedores/put_produtos_fornecedores__idProdutoFornecedor_>

Altera um produto fornecedor pelo ID.

## [reference] /produtos/fornecedores/{idProdutoFornecedor}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Fornecedores/delete_produtos_fornecedores__idProdutoFornecedor_>

Remove um produto fornecedor pelo ID.

## [reference] /produtos/lojas
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lojas/get_produtos_lojas>

Obtém vínculos de produtos com lojas paginados.

## [reference] /produtos/lojas
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lojas/post_produtos_lojas>

Cria o vínculo de um produto com uma loja.

## [reference] /produtos/lojas/{idProdutoLoja}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lojas/get_produtos_lojas__idProdutoLoja_>

Obtém um vínculo de produto com loja pelo ID.

## [reference] /produtos/lojas/{idProdutoLoja}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lojas/put_produtos_lojas__idProdutoLoja_>

Altera o vínculo de um produto com uma loja pelo ID.

## [reference] /produtos/lojas/{idProdutoLoja}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Lojas/delete_produtos_lojas__idProdutoLoja_>

Remove o vínculo de um produto com uma loja pelo ID.

## [reference] /produtos
<https://developer.bling.com.br/referencia#/Produtos/get_produtos>

Obtém produtos paginados.

## [reference] /produtos
<https://developer.bling.com.br/referencia#/Produtos/post_produtos>

Cria um produto.

## [reference] /produtos
<https://developer.bling.com.br/referencia#/Produtos/delete_produtos>

Remove múltiplos produtos pelos IDs.

## [reference] /produtos/{idProduto}
<https://developer.bling.com.br/referencia#/Produtos/get_produtos__idProduto_>

Obtém um produto pelo ID.

## [reference] /produtos/{idProduto}
<https://developer.bling.com.br/referencia#/Produtos/put_produtos__idProduto_>

Altera um produto pelo ID.

## [reference] /produtos/{idProduto}
<https://developer.bling.com.br/referencia#/Produtos/delete_produtos__idProduto_>

Remove um produto pelo ID.

## [reference] /produtos/{idProduto}
<https://developer.bling.com.br/referencia#/Produtos/patch_produtos__idProduto_>

Altera parcialmente um produto pelo ID. Somente os campos informados terão o valor alterado.

## [reference] /produtos/{idProduto}/situacoes
<https://developer.bling.com.br/referencia#/Produtos/patch_produtos__idProduto__situacoes>

Altera a situação de um produto pelo ID.

## [reference] /produtos/situacoes
<https://developer.bling.com.br/referencia#/Produtos/post_produtos_situacoes>

Altera a situação de múltiplos produtos pelos IDs.

## [reference] /produtos/variacoes/{idProdutoPai}
<https://developer.bling.com.br/referencia#/Produtos%20-%20Varia%C3%A7%C3%B5es/get_produtos_variacoes__idProdutoPai_>

Obtém o produto e variações pelo ID do produto pai.

## [reference] /produtos/variacoes/atributos/gerar-combinacoes
<https://developer.bling.com.br/referencia#/Produtos%20-%20Varia%C3%A7%C3%B5es/post_produtos_variacoes_atributos_gerar_combinacoes>

Ação responsável por retornar o produto pai com combinação de novas variações a partir dos atributos. Esta ação não persistirá os dados.

## [reference] /produtos/variacoes/{idProdutoPai}/atributos
<https://developer.bling.com.br/referencia#/Produtos%20-%20Varia%C3%A7%C3%B5es/patch_produtos_variacoes__idProdutoPai__atributos>

Altera o nome do atributo nas variações de um produto pai.

## [reference] /situacoes/modulos
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20M%C3%B3dulos/get_situacoes_modulos>

Obtém módulos.

## [reference] /situacoes/modulos/{idModuloSistema}
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20M%C3%B3dulos/get_situacoes_modulos__idModuloSistema_>

Obtém situações de um módulo pelo ID.

## [reference] /situacoes/modulos/{idModuloSistema}/acoes
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20M%C3%B3dulos/get_situacoes_modulos__idModuloSistema__acoes>

Obtém as ações de um módulo pelo ID.

## [reference] /situacoes/modulos/{idModuloSistema}/transicoes
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20M%C3%B3dulos/get_situacoes_modulos__idModuloSistema__transicoes>

Obtém as transições de um módulo pelo ID.

## [reference] /situacoes/{idSituacao}
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es/get_situacoes__idSituacao_>

Obtém uma situação pelo ID.

## [reference] /situacoes/{idSituacao}
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es/put_situacoes__idSituacao_>

Altera uma situação pelo ID.

## [reference] /situacoes/{idSituacao}
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es/delete_situacoes__idSituacao_>

Remove uma situação pelo ID.

## [reference] /situacoes
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es/post_situacoes>

Cria uma situação.

## [reference] /situacoes/transicoes/{idTransicao}
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20Transi%C3%A7%C3%B5es/get_situacoes_transicoes__idTransicao_>

Obtém uma transição pelo ID.

## [reference] /situacoes/transicoes/{idTransicao}
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20Transi%C3%A7%C3%B5es/put_situacoes_transicoes__idTransicao_>

Altera uma transição pelo ID.

## [reference] /situacoes/transicoes/{idTransicao}
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20Transi%C3%A7%C3%B5es/delete_situacoes_transicoes__idTransicao_>

Remove uma transição pelo ID.

## [reference] /situacoes/transicoes
<https://developer.bling.com.br/referencia#/Situa%C3%A7%C3%B5es%20-%20Transi%C3%A7%C3%B5es/post_situacoes_transicoes>

Cria uma transição.

## [reference] /usuarios/recuperar-senha
<https://developer.bling.com.br/referencia#/Usu%C3%A1rios/post_usuarios_recuperar_senha>

Envia solicitação de recuperação de senha por e-mail.

## [reference] /usuarios/redefinir-senha
<https://developer.bling.com.br/referencia#/Usu%C3%A1rios/patch_usuarios_redefinir_senha>

Redefine senha do usuário utilizando token enviado por e-mail.

## [reference] /usuarios/verificar-hash
<https://developer.bling.com.br/referencia#/Usu%C3%A1rios/get_usuarios_verificar_hash>

Valida o hash recebido por e-mail.

## [reference] /pedidos/vendas
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/get_pedidos_vendas>

Obtém pedidos de vendas paginados.

## [reference] /pedidos/vendas
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas>

Cria um pedido de venda.

## [reference] /pedidos/vendas
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/delete_pedidos_vendas>

Remove pedidos de vendas pelos IDs.

## [reference] /pedidos/vendas/{idPedidoVenda}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/get_pedidos_vendas__idPedidoVenda_>

Obtém um pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/put_pedidos_vendas__idPedidoVenda_>

Altera um pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/delete_pedidos_vendas__idPedidoVenda_>

Remove um pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}/situacoes/{idSituacao}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/patch_pedidos_vendas__idPedidoVenda__situacoes__idSituacao_>

Altera a situação de um pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}/lancar-estoque/{idDeposito}
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas__idPedidoVenda__lancar_estoque__idDeposito_>

Lança o estoque de um pedido de venda pelo ID, especificando o ID do depósito.

## [reference] /pedidos/vendas/{idPedidoVenda}/lancar-estoque
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas__idPedidoVenda__lancar_estoque>

Lança o estoque de um pedido de venda pelo ID, no depósito padrão.

## [reference] /pedidos/vendas/{idPedidoVenda}/estornar-estoque
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas__idPedidoVenda__estornar_estoque>

Estorna o estoque de um pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}/lancar-contas
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas__idPedidoVenda__lancar_contas>

Lança as contas de um pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}/estornar-contas
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas__idPedidoVenda__estornar_contas>

Estorna as contas de um pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}/gerar-nfe
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas__idPedidoVenda__gerar_nfe>

Gera nota fiscal eletrônica a partir do pedido de venda pelo ID.

## [reference] /pedidos/vendas/{idPedidoVenda}/gerar-nfce
<https://developer.bling.com.br/referencia#/Pedidos%20-%20Vendas/post_pedidos_vendas__idPedidoVenda__gerar_nfce>

Gera nota fiscal de consumidor eletrônica a partir do pedido de venda pelo ID.

## [reference] /vendedores
<https://developer.bling.com.br/referencia#/Vendedores/get_vendedores>

Obtém vendedores paginados.

## [reference] /vendedores/{idVendedor}
<https://developer.bling.com.br/referencia#/Vendedores/get_vendedores__idVendedor_>

Obtém um vendedor pelo ID.

## [reference] /contas/pagar
<https://developer.bling.com.br/referencia#/Contas%20a%20Pagar/get_contas_pagar>

Obtém contas a pagar paginadas.

## [reference] /contas/pagar
<https://developer.bling.com.br/referencia#/Contas%20a%20Pagar/post_contas_pagar>

Cria uma conta a pagar.

## [reference] /contas/pagar/{idContaPagar}
<https://developer.bling.com.br/referencia#/Contas%20a%20Pagar/get_contas_pagar__idContaPagar_>

Obtém uma conta a pagar pelo ID.

## [reference] /contas/pagar/{idContaPagar}
<https://developer.bling.com.br/referencia#/Contas%20a%20Pagar/put_contas_pagar__idContaPagar_>

Atualiza uma conta a pagar pelo ID.

## [reference] /contas/pagar/{idContaPagar}
<https://developer.bling.com.br/referencia#/Contas%20a%20Pagar/delete_contas_pagar__idContaPagar_>

Remove uma conta a pagar pelo ID.

## [reference] /contas/pagar/{idContaPagar}/baixar
<https://developer.bling.com.br/referencia#/Contas%20a%20Pagar/post_contas_pagar__idContaPagar__baixar>

Cria o recebimento de uma conta a pagar.

## [reference] /canais-venda
<https://developer.bling.com.br/referencia#/Canais%20de%20Venda/get_canais_venda>

Obtém canais de venda paginados.

## [reference] /canais-venda/{idCanalVenda}
<https://developer.bling.com.br/referencia#/Canais%20de%20Venda/get_canais_venda__idCanalVenda_>

Obtém uma canal de venda pelo ID.

## [reference] /canais-venda/tipos
<https://developer.bling.com.br/referencia#/Canais%20de%20Venda/get_canais_venda_tipos>

Obtém os tipos de canais de venda paginados.

## [reference] /ordens-producao
<https://developer.bling.com.br/referencia#/Ordens%20de%20Produ%C3%A7%C3%A3o/get_ordens_producao>

Obtém ordens de produção paginadas.

## [reference] /ordens-producao
<https://developer.bling.com.br/referencia#/Ordens%20de%20Produ%C3%A7%C3%A3o/post_ordens_producao>

Cria uma ordem de produção.

## [reference] /ordens-producao/{idOrdemProducao}
<https://developer.bling.com.br/referencia#/Ordens%20de%20Produ%C3%A7%C3%A3o/get_ordens_producao__idOrdemProducao_>

Obtém uma ordem de produção pelo ID.

## [reference] /ordens-producao/{idOrdemProducao}
<https://developer.bling.com.br/referencia#/Ordens%20de%20Produ%C3%A7%C3%A3o/put_ordens_producao__idOrdemProducao_>

Altera uma ordem de produção pelo ID.

## [reference] /ordens-producao/{idOrdemProducao}
<https://developer.bling.com.br/referencia#/Ordens%20de%20Produ%C3%A7%C3%A3o/delete_ordens_producao__idOrdemProducao_>

Remove uma ordem de produção pelo ID.

## [reference] /ordens-producao/{idOrdemProducao}/situacoes
<https://developer.bling.com.br/referencia#/Ordens%20de%20Produ%C3%A7%C3%A3o/put_ordens_producao__idOrdemProducao__situacoes>

Altera a situação de uma ordem de produção pelo ID.

## [reference] /ordens-producao/gerar-sob-demanda
<https://developer.bling.com.br/referencia#/Ordens%20de%20Produ%C3%A7%C3%A3o/post_ordens_producao_gerar_sob_demanda>

Gera ordens de produção sob demanda (abaixo do estoque mínimo).

## [reference] /ordens/servico
<https://developer.bling.com.br/referencia#/Ordens%20de%20Servi%C3%A7o/get_ordens_servico>

Obtém ordens de serviço paginadas.

## [reference] /ordens/servico
<https://developer.bling.com.br/referencia#/Ordens%20de%20Servi%C3%A7o/post_ordens_servico>

Cria uma ordem de serviço.

## [reference] /ordens/servico/{idOrdemServico}
<https://developer.bling.com.br/referencia#/Ordens%20de%20Servi%C3%A7o/get_ordens_servico__idOrdemServico_>

Obtém uma ordem de serviço pelo ID.

## [reference] /ordens/servico/{idOrdemServico}
<https://developer.bling.com.br/referencia#/Ordens%20de%20Servi%C3%A7o/put_ordens_servico__idOrdemServico_>

Altera uma ordem de serviço pelo ID. Os campos não informados são gravados com o valor padrão, portanto envie o recurso completo.

## [reference] /ordens/servico/{idOrdemServico}
<https://developer.bling.com.br/referencia#/Ordens%20de%20Servi%C3%A7o/delete_ordens_servico__idOrdemServico_>

Remove uma ordem de serviço pelo ID.

## [reference] /ordens/servico/{idOrdemServico}/situacoes/{idSituacao}
<https://developer.bling.com.br/referencia#/Ordens%20de%20Servi%C3%A7o/patch_ordens_servico__idOrdemServico__situacoes__idSituacao_>

Altera a situação de uma ordem de serviço pelo ID.

## [reference] /grupos-produtos
<https://developer.bling.com.br/referencia#/Grupos%20de%20Produtos/get_grupos_produtos>

Obtém grupos de produtos paginados.

## [reference] /grupos-produtos
<https://developer.bling.com.br/referencia#/Grupos%20de%20Produtos/post_grupos_produtos>

Cria um grupo de produtos.

## [reference] /grupos-produtos
<https://developer.bling.com.br/referencia#/Grupos%20de%20Produtos/delete_grupos_produtos>

Remove múltiplos grupos de produtos pelos IDs.

## [reference] /grupos-produtos/{idGrupoProduto}
<https://developer.bling.com.br/referencia#/Grupos%20de%20Produtos/get_grupos_produtos__idGrupoProduto_>

Obtém um grupo de produtos pelo ID.

## [reference] /grupos-produtos/{idGrupoProduto}
<https://developer.bling.com.br/referencia#/Grupos%20de%20Produtos/put_grupos_produtos__idGrupoProduto_>

Altera um grupo de produtos pelo ID.

## [reference] /grupos-produtos/{idGrupoProduto}
<https://developer.bling.com.br/referencia#/Grupos%20de%20Produtos/delete_grupos_produtos__idGrupoProduto_>

Remove um grupo de produtos pelo ID.

## [reference] /caixas
<https://developer.bling.com.br/referencia#/Caixas%20e%20Bancos/get_caixas>

Obtém lista de lançamentos de caixas e bancos.

## [reference] /caixas
<https://developer.bling.com.br/referencia#/Caixas%20e%20Bancos/post_caixas>

Cria um novo lançamento de caixa e banco com os dados fornecidos.

## [reference] /caixas/{idCaixa}
<https://developer.bling.com.br/referencia#/Caixas%20e%20Bancos/get_caixas__idCaixa_>

Obtém um lançamento de caixa e banco.

## [reference] /caixas/{idCaixa}
<https://developer.bling.com.br/referencia#/Caixas%20e%20Bancos/put_caixas__idCaixa_>

Atualiza um lançamento de caixa e banco existente com os dados fornecidos.

## [reference] /caixas/{idCaixa}
<https://developer.bling.com.br/referencia#/Caixas%20e%20Bancos/delete_caixas__idCaixa_>

Remove um lançamento de caixa e banco pelo ID. O registro não é excluído permanentemente, apenas marcado como excluído (exclusão lógica).

## [reference] /documentos-compartilhados/{token}
<https://developer.bling.com.br/referencia#/Documentos%20Compartilhados/get_documentos_compartilhados__token_>

Obtém um documento compartilhado pelo token.

## [page] Aplicativos > Introdução
<https://developer.bling.com.br/aplicativos#introducao>

Este manual contempla o passo a passo aos integradores que desejam criar um aplicativo e entender o funcionamento do fluxo de autorização para a obtenção dos tokens de acesso do OAuth 2.0.

## [page] Aplicativos > Inscrição
<https://developer.bling.com.br/aplicativos#inscricao>

Caso você ainda não possua uma conta no Bling clique aqui e faça a sua inscrição.

## [page] Aplicativos > Acesso ao módulo
<https://developer.bling.com.br/aplicativos#acesso-ao-modulo>

É possível cadastrar um aplicativo pela conta do administrador ou criando um usuário para tal finalidade. Recomendamos a criação de um usuário para cada desenvolvedor, dessa forma, cada usuário poderá gerenciar somente os seus aplicativos. 1. Para criar um usuário acesse o menu "Preferências > Sistema > Usuários", clique em "Incluir usuário". 2. Nas permissões de "Cadastros" selecione "Cadastro de aplicativos" e preencha as informações da conta do usuário. Após esse processo, o usuário possuirá acesso ao módulo de Cadastro de aplicativos.

## [page] Aplicativos > Como cadastrar
<https://developer.bling.com.br/aplicativos#como-cadastrar>

1. Acesse a Central de Extensões 2. Clique em "Área do Integrador" Na tela de cadastro de aplicativos clique no botão Criar aplicativo.

## [page] Aplicativos > Como cadastrar > Visibilidade
<https://developer.bling.com.br/aplicativos#visibilidade>

Escolha a visibilidade do aplicativo: Visibilidade Descrição Público O aplicativo será utilizado para realizar operações em outras contas Bling e passará pelo processo de homologação. Enquanto não for homologado, o número de usuários que podem autorizá-lo estará restrito a 10. Privado O aplicativo será utilizado para realizar operações na própria conta Bling. Clique em próximo. Na sequência preencha os seguintes dados do aplicativo: - Logo: Exibido aos usuários do aplicativo. - Nome: Exibido aos seus usuários. - Categoria: Classificação de negócio. - Descrição: Detalhamento das principais características e finalidades deste aplicativo. - Descrição curta: Descrição curta do aplicativo, utilizada na Central de Extensões. - Link de redirecionamento: Utilizado na etapa de autorização. - Link da homepage: Endereço do site do aplicativo. - Link do manual: Link para o manual do aplicativo. - Link do vídeo demonstrativo: Vídeo do Youtube ou Vimeo que apresenta as funcionalidades do aplicativo. - Nome do desenvolvedor: Nome do desenvolvedor do aplicativo. - Email: Email para eventuais contatos do nosso time. - Celular: Celular para eventuais contatos do nosso time. - Lista de escopos: Escopos referentes aos dados dos usuários que serão acessados pelo aplicativo. Após o preenchimento dos dados, clique no botão Salvar para finalizar a criação do aplicativo. O botão será habilitado somente após a inserção de um escopo.

## [page] Aplicativos > Como cadastrar > Visibilidade > Categorias
<https://developer.bling.com.br/aplicativos#categorias>

As categorias são utilizadas para facilitar o cliente na busca por um aplicativo, sendo elas: Nome Descrição Marketplace Plataforma para reunir diversos vendedores em um só lugar. Plataforma de e-commerce Sistema para criação e gerenciamento de lojas virtuais. Hub Plataforma centralizadora de conexões com canais de venda. Delivery Plataforma para entrega rápida de produtos. Social commerce Estratégia para venda de produtos e serviços através de redes sociais. Gestão de entregas Controle, organização e acompanhamento dos envios e entregas. Gestão de estoques Controle, organização e acompanhamento de estoque dos produtos. Controle financeiro Sistema para realizar a gestão de operações financeiras. Precificação Sistema para ajudar a determinar os preços ideais de produtos. Vendas presenciais Gestão de vendas realizadas em lojas físicas, balcões ou pontos de venda. Automação de vendas Sistema para automatizar tarefas comerciais referentes ao processo de vendas. CRM Sistema para gerenciar interações com clientes. Dashboards e BI Painel para apresentar informações importantes, resumidas e permite uma análise rápida. Soluções em IA Resolução de problemas por meio de inteligência artificial. ERP Sistema para controlar operações da empresa, como estoque, vendas, entre outros. Outro Destinada para casos não enquadrados em outras categorias.

## [page] Aplicativos > Como cadastrar > Visibilidade > Imagens do aplicativo
<https://developer.bling.com.br/aplicativos#imagens-do-aplicativo>

Utilizadas somente em aplicativos públicos. As imagens do aplicativo são exibidas na tela de contratação do aplicativo e podem ser usadas como uma forma de divulgar as funcionalidades presentes no sistema. É permitido realizar o upload de até cinco imagens. Exemplo de aplicativo com imagens:

## [page] Aplicativos > Como cadastrar > Visibilidade > Escopos
<https://developer.bling.com.br/aplicativos#escopos>

O Escopo é a representação da permissão para operar sobre os recursos do usuário. Portanto, informe somente os escopos necessários, passando maior clareza e segurança ao usuário no momento da autorização do aplicativo. Para inserir os escopos clique no botão Adicionar, conforme ilustrado na imagem a seguir. Marque os escopos que serão utilizados pelo aplicativo e clique no botão Adicionar. Caso seja necessário, é possível filtrar os escopos por módulo e nome, usando a busca localizada no topo desta janela. Os escopos escolhidos serão listados no formulário. Para excluir um escopo, passe o cursor sobre a linha desejada e clique no ícone da lixeira, uma janela pedindo a confirmação da exclusão será exibida. Se precisar inserir novos escopos, clique na ação de Adicionar escopo logo abaixo da listagem. É importante lembrar que o aplicativo só terá acesso aos dados referentes aos escopos selecionados. Qualquer adição ou exclusão de escopos só será confirmada após o salvamento do aplicativo. Se isso acontecer, uma janela de confirmação será exibida. Ao confirmar a edição, todos os usuários do aplicativo serão automaticamente revogados. Desta forma, é garantida a segurança das informações dos usuários, exibindo a nova listagem de escopos no momento da autorização.

## [page] Aplicativos > Como cadastrar > Visibilidade > Modelo de manual
<https://developer.bling.com.br/aplicativos#modelo-de-manual>

<div id="modelo-de-manual-container"> Passos no Bling: Para integrar com o aplicativo XXXXX, na API v3, acesse a sua conta Bling e clique no menu da Central de Extensões. <br> Neste menu é possível buscar na barra de pesquisa o aplicativo XXXXX. Ao localizar o aplicativo desejado, será possível clicar em Instalar aplicativo. Ao clicar para instalar, é solicitada a autorização: Isso irá autorizar o aplicativo a obter os tokens e se comunicar com sua conta Bling. A partir desse momento, todas as configurações no Bling estão finalizadas. Passos no Integrador (Informações que o desenvolvedor do app deve adicionar no manual) Descreva o fluxo que o cliente precisa seguir em seu site/sistema: REQUISITOS <br> Existe a obrigatoriedade de ter uma conta antes de instalar o aplicativo? <br> Se sim, explique como e onde criar a conta: <br> Ex: Acesse www.aplicativov3.com.br, clique em criar a conta, forneça email e nome… <br> Há preparações necessárias na conta antes de autorizar o aplicativo? Se sim, descrever os processos necessários: <br> Ex: Para integrar com o Bling, antes de permitir a integração, deve ser acessado a tela de “gerir conta” e clicar em “Integrar com o Bling” <br> Após a autorização, quais passos o cliente deve seguir para que a integração ocorra com sucesso? CONTATO <br> Informe o contato do suporte ao seu sistema: <br> Ex: Telefone/Email que o cliente pode entrar em contato. </div>

## [page] Aplicativos > Como cadastrar > Visibilidade > Informações do aplicativo
<https://developer.bling.com.br/aplicativos#informacoes-do-aplicativo>

Após a criação do aplicativo, a aba "Informações do app" ficará disponível. Atente-se ao Client Id e ao Client Secret, que serão utilizados no momento da autorização. É possível revogar os usuários do aplicativo. Essa ação exclui todos os tokens de acesso e faz com que os usuários tenham que realizar novamente a etapa de autorização. Ao executar a ação através do botão Revogar usuários, será solicitada a confirmação da ação. Logo abaixo da quantidade de usuários é possível visualizar as credenciais do aplicativo. Para revelar o Client Secret clique no ícone de olho. Assim como qualquer credencial, é importante manter a chave em segredo. Essa credencial será utilizada nas requisições para obtenção de tokens de acesso. O Client Secret poderá ser alterado a qualquer momento clicando no botão Redefinir client secret. Após pressionar o botão Redefinir client secret será solicitada a confirmação da ação. A ação gera um novo Client Secret, portanto será necessário realizar a alteração nas requisições que fazem uso do Client Secret anterior.

## [page] Aplicativos > Como cadastrar > Visibilidade > Exclusão
<https://developer.bling.com.br/aplicativos#exclusao>

Com a exclusão do aplicativo, todos os tokens de acesso dos usuários serão automaticamente revogados. Para excluir, na aba "Informações do app", ao confirmar a ciência da ação, o botão Excluir aplicativo será exibido.

## [page] Aplicativos > Como cadastrar > Códigos de acesso
<https://developer.bling.com.br/aplicativos#codigos-de-acesso>

Para gerar os códigos de acesso é necessário que os usuários deem autorização sobre o acesso aos dados das contas, ao aplicativo. O OAuth 2 protocola 4 tipos de concessão para que essa autorização seja realizada, no entanto o Bling fará uso de apenas uma delas, que é o Authorization Code. Portanto, será necessário seguir o fluxo de autorização descrito abaixo para obter os códigos de acesso.

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Terminologia
<https://developer.bling.com.br/aplicativos#terminologia>

Termo Detalhamento Client App Aplicativo que fará uso dos dados das contas dos usuários (conta Bling). Authorization Code Código enviado ao Client App quando um usuário autoriza acesso aos dados. Access Token Token utilizado para requisição do recurso dos usuários. Refresh Token Token utilizado para requisitar um novo access_token, quando o mesmo expirar.

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Fluxo de autorização
<https://developer.bling.com.br/aplicativos#fluxo-de-autorizacao>

Segue abaixo um resumo das etapas do fluxo de autorização. 1. O client app, com a intenção de obter o authorization_code, redireciona o usuário (através do seu user agent) para o authorization server. 2. O usuário se autentica no sistema e autoriza, ou não, o aplicativo. 3. O authorization server redireciona o usuário (através do user agent) de volta ao client app, utilizando a “URL de redirecionamento” inserida no cadastro do aplicativo. Se o usuário autorizou o acesso aos seus recursos, o authorization_code será incluído no retorno e segue-se para o passo a seguir. Caso contrário, o fluxo de autorização termina aqui. 4. O client app requisita o access_token, fazendo uma requisição para o authorization server com o authorization_code recebido no passo anterior. 5. Se o authorization_code for válido, o authorization server retornará um JSON contendo o access_token e o refresh_token.

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Authorization code
<https://developer.bling.com.br/aplicativos#authorization-code>

Utilizando redirecionamento de URL o client app direciona o usuário para o endpoint authorize: ``http GET /Api/v3/oauth/authorize?response_type=code&client_id=[seu_client_id]&state=[sequencia_de_caracteres_aleatorios] HTTP/1.1 Host: https://www.bling.com.br ` Parâmetro Descrição response_type O valor deve ser code. Significa que o aplicativo está requisitando um authorization_code. client_id Client id do aplicativo, exibido na edição do aplicativo. state Sequência aleatória de caracteres e de preferência única para cada sessão. O valor informado será mantido pelo authorization server e incluído na resposta ao client. Assim, ao comparar o valor recebido do enviado, é possível amenizar problemas com cross-site request forgery (CSRF). Os parâmetros redirect_uri e scope são considerados de uso opcional pela RFC, portanto, os mesmos não serão exigidos na requisição. Para estes dois parâmetros sempre serão usados os valores inseridos previamente no cadastro de aplicativos, mesmo que os mesmos sejam utilizados na requisição. URL de exemplo da requisição: `http https://bling.com.br/Api/v3/oauth/authorize?response_type=code&client_id=7dbf42c119eea8b65d2c1a1a9ad92b1577594&state=291e61b56ab3d845622cf137b1e1e2 ` Se o usuário autorizar a sua solicitação, o authorization server irá redirecionar o user agent para a URL de redirecionamento do aplicativo. Os parâmetros abaixo são incluídos na URL de redirecionamento: Parâmetro Descrição code Authorization code, que possui tempo de expiração de 1 minuto. Utilizado para obtenção dos tokens de acesso. state Mesmo valor informado na requisição. Caso o state retornado for diferente do utilizado na requisição, ignore-a e interrompa o fluxo de autorização. Exemplo de URL usada como callback com os parâmetros utilizados no retorno do authorization server: `http https://www.clientapp.com.br/callback?code=6521791563472106326454c818bd19f60febdcf3&state=291e61b56ab3d845622cf137b1e1e2 ``

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Tokens de acesso
<https://developer.bling.com.br/aplicativos#tokens-de-acesso>

<hr> Atenção: A autenticação com token opaco foi descontinuada. É necessário migrar para o novo modelo de JWT. Para mais detalhes, consulte migração para autenticação JWT. <hr> Com o authorization_code o client app deve realizar uma requisição POST para o endpoint /token, nisso o code será validado e os tokens de acesso serão retornados. Lembrando que o prazo para realizar esta requisição é de 1 minuto, este é o tempo de expiração do code. Formato da requisição HTTP que deve ser utilizado e uma tabela com o conteúdo que deve ser inserido no body: ``http POST /Api/v3/oauth/token? HTTP/1.1 Host: https://api.bling.com.br Content-Type: application/x-www-form-urlencoded Accept: 1.0 Authorization: Basic [base64_das_credenciais_do_client_app] grant_type=authorization_code&code=[authorization_code] ` Parâmetro no body Descrição grant_type O valor deve ser authorization_code. Informa o tipo de concessão utilizado. code Authorization code obtido na requisição do tópico anterior. O client app precisa ser autenticado para realizar esta operação, portanto, será necessário informar as suas credenciais no cabeçalho da requisição (não é permitida a inserção destes parâmetros no body). Para isso use o esquema “Basic” de autenticação HTTP inserindo um cabeçalho no formato: ` Authorization: Basic [credenciais_do_client_app] ` Lembrando que estas credenciais devem ser o client_id junto do client_secret separados por ":" e codificados em base64. Também é importante utilizar HTTPS / TLS para garantir a segurança dos seus dados. Faça a requisição inteiramente no lado do servidor, busque evitar a exposição de qualquer dado inserido nela, como as credenciais do app ou o authorization_code. Segue um exemplo de requisição dos tokens de acesso utilizando cURL: `bash curl --location --request POST 'https://api.bling.com.br/Api/v3/oauth/token' \\ --header 'Content-Type: application/x-www-form-urlencoded' \\ --header 'Accept: 1.0' \\ --header 'Authorization: Basic ZWRkNTE4NjQzNDYxNzdiMTE5NzFlNmY0YTUyMmM5ZmYxZGZjNjNkZjo2OGViODVkY2FkOTY3Mzk2ZDA1ZmVjZGQwMDgwMjExN2Q3NTE1MjY0YjUyMGMzNjJlN2Y0NjYxOWFhMDk=' \\ --data-urlencode 'grant_type=authorization_code' \\ --data-urlencode 'code=6521791563472106326454c818bd19f60febdcf3' ` Caso a requisição seja válida, será retornado um objeto JSON contendo o access_token, com o seu tipo, tempo de expiração, escopos permitidos e o refresh_token. Veja abaixo um exemplo desse retorno e um quadro com a explicação de cada parâmetro. `json { "access_token": "4a9de71b8aaf91c8ebbf830888354d5479e83a01", "expires_in": 21600, "token_type": "Bearer", "scope": "98309 318257570 5862218180", "refresh_token": "e4d61baafd951bbbdec0a92cf9700a49b4cbc005" } ` Parâmetro da resposta Descrição access_token Token utilizado para requisitar os recursos do usuário. expires_in Tempo de expiração do access_token em segundos. token_type Tipo do esquema de autenticação (Bearer Authentication). scope Lista dos ids dos escopos que o app possui permissão de acesso. refresh_token Token utilizado para requisitar um novo token de acesso, após a expiração do access_token`.

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Refresh Token
<https://developer.bling.com.br/aplicativos#refresh-token>

Quando o tempo do access_token terminar é possível requisitar um novo utilizando o refresh_token, o qual foi enviado junto do access_token e possui um tempo de expiração superior, de 30 dias. Para isso é realizada uma requisição POST para o endpoint token, na mesma estrutura da requisição apresentada anteriormente, a única diferença está nos parâmetros que devem ser apresentados no body. Veja abaixo o formato da requisição HTTP que deve ser utilizado e a tabela com o conteúdo que deve ser inserido no body. ``http POST /Api/v3/oauth/token? HTTP/1.1 Host: https://api.bling.com.br Content-Type: application/x-www-form-urlencoded Accept: 1.0 Authorization: Basic [base64_das_credenciais_do_client_app] grant_type=refresh_token&refresh_token=[refresh_token] ` Parâmetros no body Descrição grant_type O valor deve ser refresh_token. Informa o tipo de concessão utilizado. refresh_token Refresh token obtido na requisição do access_token que expirou. O retorno desta requisição é o mesmo JSON retornado na requisição do access_token com uso do authorization_code`.

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Utilizando o access token
<https://developer.bling.com.br/aplicativos#utilizando-o-access-token>

Com o access_token é possível realizar requisições para a API do Bling e, assim, acessar os recursos do usuário. Lembrando que este tipo de autenticação só está disponível pela API v3 e só será possível requisitar os dados dos escopos que foram permitidos pelo usuário. Como informado no JSON de retorno dos tokens de acesso, o tipo do token fornecido é o Bearer, portanto, utilize o esquema "Bearer" de autenticação HTTP, inserindo a chave de acesso no cabeçalho da requisição, conforme exemplo: ``http GET /Api/v3/[caminho_da_api_desejada] HTTP/1.1 Host: https://api.bling.com.br Authorization: Bearer [access_token] ` Exemplo de uma requisição cURL para a API de contatos: `bash curl --location --request GET 'https://api.bling.com.br/Api/v3/contatos' \\ --header 'Authorization: Bearer 4a9de71b8aaf91c8ebbf830888354d5479e83a01' \\ ``

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Revogando o access token
<https://developer.bling.com.br/aplicativos#revogando-o-access-token>

É possível revogar um access_token ou refresh_token para impedir que um usuário ou uma empresa continuem acessando a API. Essa funcionalidade garante que apenas os tokens desejados sejam invalidados. Para revogar um token, o client app deve realizar uma requisição POST para o endpoint /oauth/revoke, utilizando o esquema "Basic" de autenticação HTTP para fornecer suas credenciais, conforme exemplo: ``http POST /oauth/revoke HTTP/1.1 Host: https://api.bling.com.br Content-Type: application/x-www-form-urlencoded Authorization: Basic [base64_das_credenciais_do_client_app] token=[ACCESS_OR_REFRESH_TOKEN]&token_type_hint=[access_token|refresh_token] ` Parâmetros no body Descrição token O access_token ou refresh_token utilizado para se autenticar na api. token_type_hint` Define o tipo de token informado. Pode ser "access_token" ou "refresh_token". Se essa requisição for bem-sucedida, o token informado será revogado, impedindo seu uso para novas requisições na API.

## [page] Aplicativos > Como cadastrar > Códigos de acesso > Revogação avançada
<https://developer.bling.com.br/aplicativos#revogacao-avancada>

Para atender a necessidade de remoção de todos os tokens associados a um usuário ou empresa, foram adicionados os parâmetros revoke_action e revoke_target, que ampliam o escopo da revogação. ``http POST /oauth/revoke HTTP/1.1 Host: https://api.bling.com.br Content-Type: application/x-www-form-urlencoded Authorization: Basic [base64_das_credenciais_do_client_app] token=[ACCESS_OR_REFRESH_TOKEN]&token_type_hint=[access_token|refresh_token]&revoke_action=[logout|uninstall]&revoke_target=[user|company] ` Parâmetro no body Descrição revoke_action Define o tipo de revogação. Valores possíveis: logout ou uninstall. Se não for informado, apenas o token enviado na requisição será revogado. revoke_target Define o alvo da revogação. Valores possíveis: user (padrão) ou company. Se não for informado, o padrão será user` (revoga os tokens apenas do usuário relacionado ao token informado).

## [page] Minhas Instalações > Gerenciamento
<https://developer.bling.com.br/aplicativos#gerenciamento>

Através da aba Minhas instalações da Central de Extensões é possível gerenciar os aplicativos que foram autorizados a operar a conta. Ao clicar sobre o menu de contexto de uma instalação, será possível reportá-lo, desinstalá-lo ou reautenticá-lo, caso os códigos de acesso tenham expirados e seja preciso autorizar o aplicativo novamente.

## [page] Bling API > Introdução
<https://developer.bling.com.br/bling-api#introducao>

Bem-vindo ao Bling Developers! Neste repositório você irá encontrar toda a documentação necessária para integrar com o Bling. Por meio da nossa API é possível consumir recursos do Bling para atender as necessidades da sua empresa/clientes. Estruturada no padrão REST, onde você poderá utilizar métodos GET, POST, PUT, PATCH e DELETE, por meio de autenticação OAuth 2.0. A organização dessa documentação contempla informações sobre o Bling, o conceito de API e como utilizá-la.

## [page] Bling API > Sobre o Bling
<https://developer.bling.com.br/bling-api#sobre-o-bling>

O Bling é um ERP que facilita a emissão de notas fiscais e boletos, além de realizar integrações nativas com plataformas de e-commerce, marketplaces e logísticas, tais como por API. Com o Bling é possível gerenciar todo o processo de compra e venda dos produtos de maneira facilitada, bem como possuir relatórios que auxiliam na análise e gestão empresarial.

## [page] Bling API > O que é API
<https://developer.bling.com.br/bling-api#o-que-e-api>

API (Application Programming Interface) é um conjunto de protocolos e ferramentas que facilitam a integração entre softwares e permitem que uma solução se comunique com outros produtos e serviços sem precisar acessar a interface gráfica da solução diretamente, tudo isso através do que chamamos de interface. O intuito de uma API é a troca de dados entre sistemas implementados em diferentes tecnologias que utilizam o mesmo protocolo de comunicação. No Bling, usamos a API para integrar as nossas soluções com nossos parceiros, sendo possível criar processos de automatização, atualização ou análise de registros, criação de novos aplicativos e uma vasta gama de soluções podem ser criadas para facilitar a vida dos nossos clientes.

## [page] Bling API > Para quem é destinada a API
<https://developer.bling.com.br/bling-api#para-quem-e-destinada-a-api>

A API é pública e está disponível para quem deseja estender as funcionalidades já existentes no Bling, podendo criar plugins ou componentes em sistemas próprios. A utilização da API permite a realização de operações de forma independente, visto que os recursos do Bling serão controlados pelo cliente da API, podendo utilizar a API para implementar soluções próprias.

## [page] Bling API > Padrão REST
<https://developer.bling.com.br/bling-api#padrao-rest>

No Bling, usamos um padrão de arquitetura para a API chamado de REST (Representational State Transfer). O REST ignora os detalhes da implementação do componente e a sintaxe de protocolo visando focar nos papéis dos componentes, nas restrições sobre sua interação e na sua interpretação de elementos de dados significativos. Ou seja, o usuário deve fazer uma requisição HTTP para algum endpoint disponível para solicitar, enviar ou modificar dados do sistema, então o endpoint de API transfere uma informação do estado do recurso ao solicitante. Essa informação é entregue via HTTP utilizando um formato de mensagem do tipo JSON. Exemplo de requisição, abaixo: GET https://api.bling.com.br/Api/v3/produtos Resposta do servidor: ``JSON { "data": { "id": 1, "nome": "Caderno universitário, 100 Folhas" } } ` Cada requisição consiste em um método HTTP, um Header, uma URI e um Body que são explicados a seguir: O método HTTP diferencia a ação que o usuário deseja realizar pela API, sendo eles: - GET: Ação para obter uma ou mais entidades - POST: Ação para criar uma entidade ou executar uma ação - PUT: Ação para atualizar todos os dados de uma entidade - PATCH: Ação para atualizar parcialmente os dados de uma entidade - DELETE: Ação para remover uma entidade Header: É o cabeçalho da requisição, as informações enviadas no header podem ser utilizadas para o servidor interpretar a requisição. Exemplo: Content-Type: application/json. <br> URI: Define o caminho onde a requisição irá ocorrer, por exemplo, em uma requisição para obtenção dos dados de produtos, a URI seria: /Api/v3/produtos`. <br> Body: É o corpo da requisição, nele são informados os dados que serão enviados para o sistema e também são retornadas as informações da resposta de uma requisição.

## [page] Autenticação > Fundamentos
<https://developer.bling.com.br/bling-api#fundamentos>

Dentro dos fundamentos da segurança entre redes, a API dispõe de regras que assegurem a confidencialidade, a integridade e a acessibilidade das informações disponíveis: - Confidencialidade: É a estrita regra de manter uma autorização através de uma autenticação de acesso ao recurso. - Integridade: Assegura que os dados não poderão ser alterados sem as devidas permissões, ou que os dados não sejam visualizados em conta diferente a qual está solicitando o uso ao recurso. - Acessibilidade: Permite a cada usuário uma disponibilidade de acesso sem prejudicar o serviço que por consequência afeta todos os outros usuários dos nossos recursos. Mantemos as informações dos nossos usuários seguras pela utilização de HTTPS e por tokens gerados por aplicativos OAuth.

## [page] Autenticação > OAuth e tokens de acesso
<https://developer.bling.com.br/bling-api#oauth-e-tokens-de-acesso>

OAuth 2.0 é um protocolo de autorização utilizado para permitir que aplicativos de terceiros tenham acesso limitado aos recursos dos usuários do sistema, no qual o sistema detentor dos dados do usuário fica encarregado de realizar a autenticação e, por fim, após a aprovação deste usuário, conceder a autorização para o aplicativo acessar os seus recursos. Descubra como criar seus aplicativos e gerar os tokens de acesso através do fluxo de autorização. Em resumo, quando um usuário autoriza determinado aplicativo a acessar os seus recursos, este aplicativo conseguirá obter os tokens necessários para realizar as requisições e acessar o recurso. Veja abaixo como utilizar o Bearer token gerado pelos aplicativos OAuth.

## [page] Autenticação > Como utilizar os tokens
<https://developer.bling.com.br/bling-api#como-utilizar-os-tokens>

O tipo de token fornecido pelo protocolo OAuth é o Bearer, portanto, utilize o esquema "Bearer" de autenticação HTTP, inserindo a chave de acesso no cabeçalho da requisição, veja o formato abaixo. GET /Api/v3/[caminho_da_api_desejada] Host: https://api.bling.com.br <br> Header: Authorization: Bearer [access_token] Abaixo contempla um exemplo de uma requisição cURL para a API de contatos. ``bash curl --location --request GET 'https://api.bling.com.br/Api/v3/contatos' --header 'Authorization: Bearer 4a9de71b8aaf91c8ebbf830888354d5479e83a01' `` Possíveis erros e exceções com relação ao uso destes tokens são tratados aqui.

## [page] Boas práticas > Introdução
<https://developer.bling.com.br/boas-praticas#introducao>

Quando se está desenvolvendo uma solução onde precisa consumir uma API de terceiro, é essencial saber lidar com ela para obter o melhor desempenho possível, dentro das condições que ela pode oferecer, para não se deparar com erros que poderiam ser evitados.

## [page] Boas práticas > Recomendações
<https://developer.bling.com.br/boas-praticas#recomendacoes>

Leia com atenção a documentação específica sobre a API que deseja implementar, para compreender todas as funcionalidades disponíveis para utilização. Na documentação, estarão descritos os objetivos de cada endpoint, método HTTP, filtros, schemas de dados detalhado e os códigos de retornos.

## [page] Boas práticas > Paginação
<https://developer.bling.com.br/boas-praticas#paginacao>

A paginação é utilizada na obtenção de dados através do método GET. Para informar a página utilize o parâmetro pagina. Para controlar a quantidade de registros retornados na busca, utilize o parâmetro limite. Por padrão, serão retornados 100 registros por requisição, sendo possível configurar a quantidade de registros conforme exemplo abaixo: ``http GET /pedidos/vendas?pagina=2&limite=10 ``

## [page] Boas práticas > Atualização total (PUT) e parcial (PATCH)
<https://developer.bling.com.br/boas-praticas#atualizacao-total-put-e-parcial-patch>

A API disponibiliza dois métodos para atualizar um recurso existente: PUT e PATCH, e eles têm comportamentos diferentes. O método PUT substitui o recurso por completo. Todos os campos que já possuem valor preenchido precisam ser informados no corpo da requisição, pois caso algum campo seja omitido será removido ou retornará ao valor padrão, sem possibilidade de recuperação. O método PATCH atualiza apenas os campos enviados no corpo da requisição. Os demais campos do recurso permanecem inalterados. ``http PUT /produtos/{idProduto} ` `json { "nome": "Produto 1", "tipo": "P", "situacao": "A", "formato": "S", "codigo": "CODE_123", "preco": 1.00 } ` Nesse exemplo, nome, tipo, situacao e formato são obrigatórios em toda chamada PUT. Qualquer outro campo do produto (como descricaoCurta ou marca) que não esteja no corpo da requisição será removido ou zerado. `http PATCH /produtos/{idProduto} ` `json { "preco": 1.00 } ` Já aqui, somente preco` é alterado, mantendo os demais campos do produto como estavam. Atenção: nem todo endpoint possui o método PATCH. Verifique na documentação específica de cada recurso se a atualização parcial está disponível antes de assumir esse comportamento.

## [page] Boas práticas > Tratamento de erros
<https://developer.bling.com.br/boas-praticas#tratamento-de-erros>

Durante o desenvolvimento é possível encontrar erros não previstos. Em decorrência a isso, é importante se atentar às mensagens de erro. Verifique o código de estado HTTP, caso ele seja diferente de 2xx, construa um tratamento de erros que seja eficiente e condizente ao retorno obtido. Retornos com o HTTP code 4xx, são erros provenientes de validação, leia a mensagem de erro no corpo da resposta e verifique os dados enviados na requisição. Recomenda-se a criação de um ou mais componentes ou clientes REST para consumo da API.

## [page] Boas práticas > Segurança
<https://developer.bling.com.br/boas-praticas#seguranca>

De acordo com as orientações na seção de autenticação, para maior segurança, as práticas abaixo são recomendadas: - Não deixe que mais alguém conheça o seu client_secret, access_token e nem do refresh_token. - Prefira gerar um state único para enviar na requisição e através dele valide a operação. - Garanta que a requisição para obter os tokens de acesso sejam feitas sempre server-to-server. - Sempre utilize o protocolo HTTPS nas requisições.

## [page] Como testar > API v3 no Postman
<https://developer.bling.com.br/como-testar#api-v3-no-postman>

Como pré-requisito para utilização da API v3, é necessário que haja um aplicativo já cadastrado. Caso não o tenha, confira o passo a passo para realizar o cadastro.

## [page] Como testar > API v3 no Postman > Importação da collection
<https://developer.bling.com.br/como-testar#importacao-da-collection>

É possível importar toda a collection da API v3 para o Postman. Esse processo facilita a utilização da API, pois todos os endpoints disponíveis ficam de fácil acesso. <x-CollectionButton text="Bling collection" alias="bling-openapi.json" path="resources/OpenAPI/openapi.json"/> No Postman, clique em Import, selecione o arquivo anteriormente salvo na máquina e importe-o.

## [page] Como testar > API v3 no Postman > Configurando a permissão de acesso
<https://developer.bling.com.br/como-testar#configurando-a-permissao-de-acesso>

Nesse momento, será necessário configurar as permissões de acesso do aplicativo a conta Bling. <br> Para isso, clique no nome da collection criada (Bling API) e escolha a aba Authorization. <br> Certifique-se que o campo Type esteja selecionado como OAuth 2.0. Na seção "Configure New Token", altere os seguintes campos: 1. Callback URL para o mesmo informado no campo Link de redirecionamento, na seção de dados básicos do cadastro do aplicativo. 2. Preencha o campo Client ID conforme o valor exibido na seção de informações do app do cadastro do aplicativo. 3. Preencha o campo Client Secret conforme o valor exibido na seção de informações do app do cadastro do aplicativo. 4. Preencha o campo State com um valor aleatório, pois ele não pode ser vazio. Para mais informações sobre o campo state, acesse a seção Authorization code. Clique em Get New Access Token. <br> Nesse ponto, você precisará realizar o login na conta Bling. Após o login, será exibida a tela de autorização. Clique em "Autorizar". Assim que o login for concluído, a mensagem de sucesso será exibida. Clique em Use Token, para que o token seja preenchido de forma automática nas configurações da autorização de toda a collection. Por fim, pressione Ctrl + S para salvar as configurações realizadas. <br> Agora você terá acesso aos escopos da conta Bling que o aplicativo configurado possui.

## [page] Como testar > API v3 no Postman > Exemplo de requisição
<https://developer.bling.com.br/como-testar#exemplo-de-requisicao>

Exemplo de requisição GET de Contatos.

## [page] Erros comuns > Introdução
<https://developer.bling.com.br/erros-comuns#introducao>

Nós usamos HTTP codes para diferenciar as requisições bem sucedidas de requisições que contenham erros. Sempre serão informados o tipo, mensagem e descrição do erro. Erros 4xx apontam inconsistências nos dados enviados. <br> Erros 5xx apontam falhas no nosso serviço. A listagem abaixo exemplifica códigos de erros e mensagens que podem ser encontrados durante o uso da API.

## [page] Erros comuns > VALIDATION_ERROR
<https://developer.bling.com.br/erros-comuns#validation-error>

Ocorre quando houve erros na validação dos campos enviados pela requisição. HTTP Code: 400 `` { "error": { "type": "VALIDATION_ERROR", "message": "Não foi possível executar a operação", "description": "Ocorreu um erro ao validar os dados recebidos." } } ``

## [page] Erros comuns > MISSING_REQUIRED_FIELD_ERROR
<https://developer.bling.com.br/erros-comuns#missing-required-field-error>

Ocorre quando campos obrigatórios não foram enviados. HTTP Code: 400 `` { "error": { "type": "MISSING_REQUIRED_FIELD_ERROR", "message": "Não foi possível executar a operação", "description": "Nenhum dado foi informado na requisição." } } ``

## [page] Erros comuns > UNKNOWN_ERROR
<https://developer.bling.com.br/erros-comuns#unknown-error>

Ocorre quando uma operação não pode ser concluida. HTTP Code: 400 `` { "error": { "type": "UNKNOWN_ERROR", "message": "Não foi possível executar a operação", "description": "Ocorreu um erro inesperado." } } ``

## [page] Erros comuns > UNAUTHORIZED
<https://developer.bling.com.br/erros-comuns#unauthorized>

Ocorre quando a chave de acesso informada não está válida. HTTP Code: 401 `` { "error": { "type": "invalid_token", "message": "invalid_token", "description": "The access token provided is invalid" } } ``

## [page] Erros comuns > FORBIDDEN
<https://developer.bling.com.br/erros-comuns#forbidden>

Ocorre quando o token enviado não possui permissão para operar nos escopos requisitados. HTTP Code: 403 `` { "error": { "type": "insufficient_scope", "message": "insufficient_scope", "description": "The request requires higher privileges than provided by the access token" } } ``

## [page] Erros comuns > RESOURCE_NOT_FOUND
<https://developer.bling.com.br/erros-comuns#resource-not-found>

Ocorre quando a URN ou URI informada não existe, ou quando o recurso solicitado não foi encontrado no sistema. HTTP Code: 404 `` { "error": { "type": "RESOURCE_NOT_FOUND", "message": "Recurso não encontrado", "description": "O recurso requisitado não foi encontrado. Verifique se o endpoint solicitado está correto ou se o ID informado realmente existe no sistema." } } ``

## [page] Erros comuns > TOO_MANY_REQUESTS
<https://developer.bling.com.br/erros-comuns#too-many-requests>

Ocorre quando o total de requisições feitas atingiu o seu limite. Conforme a página limites. HTTP Code: 429 `` { "error": { "type": "TOO_MANY_REQUESTS", "message": "Limite de requisições atingido.", "description": "O limite de requisições por segundo foi atingido, tente novamente mais tarde.", "limit": 3, "period": "second" } } ` ` { "error": { "type": "TOO_MANY_REQUESTS", "message": "Limite de requisições atingido.", "description": "O limite de requisições por dia foi atingido, tente novamente mais tarde.", "limit": 120000, "period": "day" } } ``

## [page] Erros comuns > SERVER_ERROR
<https://developer.bling.com.br/erros-comuns#server-error>

Ocorre quando algum processo interno no servidor da nossa aplicação possui alguma falha. HTTP Code: 500 `` { "error": { "type": "SERVER_ERROR", "message": "Não foi possível executar a operação", "description": "Um erro interno ocorreu." } } ``

## [page] Exceções > Obtenção do authorization code
<https://developer.bling.com.br/erros-comuns#obtencao-do-authorization-code>

Neste tópico são citados alguns erros que poderão ocorrer na etapa de requisição do authorization_code. De modo geral, os erros serão retornados para a URL de redirecionamento informada no cadastro do aplicativo com a estrutura de parâmetros demonstrada na tabela abaixo. Parâmetro Descrição error O código do erro. Ex.: "invalid_request". error_description Descrição sobre o erro. error_uri Link contendo informações adicionais sobre o erro. state Valor do parâmetro state informado na requisição.

## [page] Exceções > Obtenção do authorization code > Aplicativo não autorizado
<https://developer.bling.com.br/erros-comuns#aplicativo-nao-autorizado>

Caso o usuário não autorize o acesso aos escopos solicitados pelo aplicativo, o erro será retornado através da URL de redirecionamento do aplicativo. ``http https://www.clientapp.com.br/callback?error=access_denied&error_description=The+user+denied+access+to+your+application&state=291e61b56ab3d845622cf137b1e1e2 ``

## [page] Exceções > Obtenção do authorization code > Aplicativo inativado
<https://developer.bling.com.br/erros-comuns#aplicativo-inativado>

Caso o aplicativo esteja inativado (conforme seção situação do aplicativo) você não será capaz de realizar nenhum tipo de requisição. Um erro, como o do exemplo abaixo, será retornado através da URL de redirecionamento do aplicativo. ``http https://www.clientapp.com.br/callback?error=app_inativo&error_description=Este+aplicativo+foi+inativado+temporariamente&state=291e61b56ab3d845622cf137b1e1e2 ``

## [page] Exceções > Obtenção do authorization code > Usuário não autorizado
<https://developer.bling.com.br/erros-comuns#usuario-nao-autorizado>

Exceções causadas por usuários não autorizados poderão ser redirecionadas para o callback do aplicativo, veja o exemplo abaixo. ``http https://www.clientapp.com.br/callback?error=UNAUTHORIZED_ERROR&error_description=O+usu%C3%A1rio+n%C3%A3o+possui+autoriza%C3%A7%C3%A3o+para+acessar+os+recursos+requisitados&state=xyz ` Isso poderá ocorrer especificamente quando for requisitado um novo authorization_code` para um usuário que já concedeu autorização previamente ao aplicativo. Porém, este usuário perdeu alguns privilégios durante este tempo (deixou de ter permissão para algum escopo solicitado na autorização) ou a conta passou para a situação inadimplente.

## [page] Exceções > Obtenção do authorization code > Obtenção da URL de redirecionamento
<https://developer.bling.com.br/erros-comuns#obtencao-da-url-de-redirecionamento>

Ocorre geralmente quando o client_id da requisição for inválido.

## [page] Exceções > Obtenção dos tokens de acesso
<https://developer.bling.com.br/erros-comuns#obtencao-dos-tokens-de-acesso>

O formato dos erros retornados durante esta requisição seguem o modelo adotado pela API v3 do Bling, um objeto JSON contendo as informações sobre o erro no body da resposta HTTP. Este tópico não é uma lista completa de todos os erros que poderão ocorrer durante a requisição dos tokens de acesso, porém, a leitura deste manual poderá ajudar na interpretação da maioria dos erros.

## [page] Exceções > Obtenção dos tokens de acesso > Sintaxe
<https://developer.bling.com.br/erros-comuns#sintaxe>

Independente do grant type (authorization_code ou refresh_token) utilizado, os erros mais comuns durante esta etapa são causados por problemas na sintaxe da requisição. Os exemplos mais comuns são: ausência parâmetros obrigatórios no body ou as credenciais no cabeçalho, grant type inválido, credenciais inválidas, code inexistente ou expirado. Veja abaixo os objetos JSON retornados nas requisições com erro nas credenciais do aplicativo e authorization_code expirado. ``JSON { "error": { "type": "invalid_client", "message": "invalid_client", "description": "The client credentials are invalid" } } ` `JSON { "error": { "type": "invalid_grant", "message": "invalid_grant", "description": "The authorization code has expired" } } ``

## [page] Exceções > Obtenção dos tokens de acesso > Authorization code já utilizado
<https://developer.bling.com.br/erros-comuns#authorization-code-ja-utilizado>

É permitido que cada authorization_code seja utilizado apenas uma vez. Caso um authorization_code válido (não expirado) for utilizado em uma segunda requisição para obtenção dos tokens de acesso, esta requisição não será válida e por medidas de segurança o usuário vinculado ao code terá o seu acesso revogado. Segue abaixo o JSON retornado neste caso. ``JSON { "error": { "type": "VALIDATION_ERROR", "message": "Invalid authorization code", "description": "This authorization code has already been used, for security reasons the user has been revoked." } } ``

## [page] Exceções > Obtenção dos tokens de acesso > Empresa inativa
<https://developer.bling.com.br/erros-comuns#empresa-inativa>

Assim como não é permitida a geração de um novo authorization_code aos usuários vinculados a empresas com situação diferente de ativa, não será permitida a obtenção de novos tokens de acesso com uso do refresh token. Nestes casos, o JSON abaixo será inserido no retorno. ``JSON { "error": { "type": "UNAUTHORIZED_ERROR", "message": "Empresa inativa", "description": "A empresa vinculada ao token esta inativa." } } ``

## [page] Exceções > Obtenção dos tokens de acesso > Obter recurso do usuário
<https://developer.bling.com.br/erros-comuns#obter-recurso-do-usuario>

O formato dos erros retornados durante esta requisição seguem o modelo adotado pela API v3 do Bling, um objeto JSON contendo as informações sobre o erro no body da resposta HTTP. Este tópico detalha os erros causados durante a validação do access_token utilizado na autenticação OAuth, não serão detalhados os demais erros que poderão ocorrer na requisição do recurso, para isso consulte o tópico sobre erros da API v3.

## [page] Exceções > Obtenção dos tokens de acesso > Problemas de sintaxe
<https://developer.bling.com.br/erros-comuns#problemas-de-sintaxe>

Qualquer problema com relação à sintaxe da inserção do access token na requisição. ``JSON { "error": { "type": "invalid_request", "message": "invalid_request", "description": "Malformed auth header" } } ``

## [page] Exceções > Obtenção dos tokens de acesso > Token expirou
<https://developer.bling.com.br/erros-comuns#token-expirou>

Access token expirado. ``JSON { "error": { "type": "invalid_token", "message": "invalid_token", "description": "The access token provided has expired" } } ` Utilize o refresh token` para gerar uma nova chave a este usuário, veja o tópico refresh token para mais informações.

## [page] Exceções > Obtenção dos tokens de acesso > Token não autorizado
<https://developer.bling.com.br/erros-comuns#token-nao-autorizado>

Caso o recurso requisitado não tenha sido autorizado pelo usuário, ou seja, o access_token não possui permissão para acessar o escopo referente a este recurso. ``JSON { "error": { "type": "insufficient_scope", "message": "insufficient_scope", "description": "The request requires higher privileges than provided by the access token" } } ``

## [page] Homologação > Processo
<https://developer.bling.com.br/homologacao#processo>

O processo de homologação é destinado a aplicativos com visibilidade pública, realizando integração com clientes do Bling. A primeira etapa consiste na revisão do uso da API. Após, é possível solicitar a revisão do aplicativo, onde os itens serão validados pela nossa equipe técnica conforme as regras descritas na seção validação de dados.

## [page] Homologação > Validação de dados
<https://developer.bling.com.br/homologacao#validacao-de-dados>

<div class="container-exemplos mb-4"> ❌ Exemplo incorreto: </div> <div class="container-exemplos"> ✅ Exemplo correto: </div> - Logo: Deve ser condizente com a aplicação desenvolvida. - Nome do aplicativo: Nome que será exibido para os clientes do Bling. - Descrição: Descrição da solução proposta pelo seu aplicativo/plataforma. - Descrição curta: Descrição curta do aplicativo, utilizada na Central de Extensões. Deve ser uma descrição breve e objetiva da solução proposta pelo seu aplicativo/plataforma. - Categoria: Deve ser condizente com a solução proposta, assim o cliente poderá encontrar o seu aplicativo facilmente. - Link de redirecionamento: Conforme o fluxo de autorização, espera-se que, ao trocar o authorization_code pelo access_token, haja uma interface amigável para o usuário, tanto nos casos de sucesso quanto de erro. Esse fluxo ininterrupto facilita a experiência do usuário e a integração entre o seu aplicativo e o Bling. - Link da homepage: Recomenda-se que a página disponível pela URI possua uma descrição mais detalhada da solução que o aplicativo oferece, auxiliando, também, a promover e converter novos clientes. Aconselha-se que não necessite de autenticação para acessá-la. - Link do manual: Link para o manual do aplicativo. - Link do vídeo demonstrativo: Vídeo do Youtube ou Vimeo que apresenta as funcionalidades do aplicativo. - Escopos: Os escopos selecionados devem possuir relação com a finalidade do aplicativo. Os itens apresentados acima são essencialmente utilizados na revisão dos dados cadastrados. No entanto, atente-se para a criação de um serviço seguro e bem otimizado. Qualquer indício de problema que possa prejudicar os nossos usuários fará com que o aplicativo seja inativado.

## [page] Homologação > Revisão > Introdução
<https://developer.bling.com.br/homologacao#introducao>

Para iniciar o processo de revisão do aplicativo, acesse a aba "Homologação". Após confirmar o preenchimento dos dados, uma interface para acompanhar o processo será exibida. Caso ocorram inconsistências, elas serão exibidas e será necessário iniciar a revisão novamente. Já, se o teste for bem sucedido, será possível solicitar a revisão do aplicativo para a nossa equipe técnica.

## [page] Homologação > Revisão > Execução
<https://developer.bling.com.br/homologacao#execucao>

O objetivo é validar o correto uso da API, através da execução de requests sequenciais para a API de homologação. <br> Em uma das etapas será invalidado o access token, nesse caso, utilize o refresh token. A cada request realizado, será retornado no header um hash que deve ser informado no header do passo seguinte. <br> Exemplo de retorno do header: x-bling-homologacao: iEL06HbaOdyrjw6F0cTk6z63ZOaI0Ezn0L43++ZjY/c= 1. O primeiro request deve ser feito para obter os dados que serão utilizados para o segundo request, utilizando o método GET. GET https://api.bling.com.br/Api/v3/homologacao/produtos Exemplo de resposta: `` { "data": { "nome": "Copo do Bling", "preco": 32.56, "codigo": "COD-4587" } } ` 2. Realize o request para o endpoint de método POST informando, no body da requisição, os dados contidos na propriedade data, obtidos no primeiro passo. Será retornado o id do produto "criado", lembrando que o id é apenas para representar um novo produto. POST https://api.bling.com.br/Api/v3/homologacao/produtos Exemplo do body: ` { "nome": "Copo do Bling", "preco": 32.56, "codigo": "COD-4587" } ` Exemplo de resposta: ` { "data": { "nome": "Copo do Bling", "preco": 32.56, "codigo": "COD-4587", "id": 16842381880 } } ` 3. Após criar o produto, realize a alteração do atributo descricao para "Copo". Para isso utilize o método PUT, informando no path o id do produto obtido no passo anterior e no body informe os dados atualizados do produto. PUT https://api.bling.com.br/Api/v3/homologacao/produtos/16842381880 Exemplo do body: ` { "nome": "Copo", "preco": 32.56, "codigo": "COD-4587" } ` 4. Altere a situação do produto utilizando o método PATCH. A situação do produto deve ser informada no body. PATCH https://api.bling.com.br/Api/v3/homologacao/produtos/16842381880/situacoes Exemplo do body: ` { "situacao": "I" } ` 5. Por fim, remova o produto por meio do método DELETE. DELETE https://api.bling.com.br/Api/v3/homologacao/produtos/16842381880`

## [page] Homologação > Revisão > Limites
<https://developer.bling.com.br/homologacao#limites>

O tempo total do teste deve ser de no máximo 10 segundos. <br> O limite entre cada requisição é de 2 segundos. <br> Caso o limite seja atingido, revise a implementação e refaça a operação.

## [page] Homologação > Situações
<https://developer.bling.com.br/homologacao#situacoes>

As 5 situações de um aplicativo público são: - Em desenvolvimento: Ao salvar um aplicativo de visibilidade pública, no momento da criação, ele será salvo nessa situação. - Em revisão: Após o aplicativo estar desenvolvido e pronto para operar contas do Bling, na edição do aplicativo clique em "Solicitar revisão". Após, nossa equipe técnica fará a revisão. - Aprovado: Caso não haja incoerência, o aplicativo será aprovado. - Rejeitado: Havendo inconsistência no aplicativo, ele será rejeitado durante a fase de revisão. Se isso acontecer, você será notificado e os motivos da rejeição serão apresentados na edição do aplicativo. Realize os ajustes e salve o aplicativo, nesse momento uma nova revisão será solicitada. Durante a fase de rejeição o aplicativo funcionará como na fase de revisão. - Inativado: Caso sejam identificados ou reportados abusos, o aplicativo poderá ser inativado. Será notificado o problema encontrado e o aplicativo terá todos os tokens de acesso revogados. Para poder reativar o seu aplicativo, será necessário entrar em contato com a nossa equipe. Se a situação do aplicativo for alterada, você será notificado no Bling. Caso a situação tenha sido alterada para rejeitado ou inativado, o motivo será informado na tela de edição do aplicativo.

## [page] Limites > Filtros
<https://developer.bling.com.br/limites#filtros>

Requests GET com filtros por período com intervalo superior a um ano retornarão o status code 400. Filtros por período possuem os sufixos "Inicial" ou "Final", ex: dataInicial, dataFinal, dataAlteracaoInicial e dataAlteracaoFinal.

## [page] Limites > Requisições
<https://developer.bling.com.br/limites#requisicoes>

A API do Bling possui uma política de segurança para evitar prejudicar o usuário e assegurar a disponibilidade dos nossos recursos. Existem limites sobre as requisições de cada conta Bling, não específicas por endpoints, mas sim para todas. Isso significa que em quaisquer módulos que estejam sendo operados, o limite é aplicado para toda a conta. Caso um limite seja atingido, os próximos requests não serão processados. Os limites por requisições são determinados pelas regras abaixo: - 3 requisições por segundo - 120.000 requisições por dia Exemplos de retornos quando um limite é atingido: HTTP Status code: 429 Too Many Requests `` { "error": { "type": "TOO_MANY_REQUESTS", "message": "Limite de requisições atingido.", "description": "O limite de requisições por segundo foi atingido, tente novamente mais tarde.", "limit": 3, "period": "second" } } ` HTTP Status code: 429 Too Many Requests ` { "error": { "type": "TOO_MANY_REQUESTS", "message": "Limite de requisições atingido.", "description": "O limite de requisições por dia foi atingido, tente novamente amanhã.", "limit": 120000, "period": "day" } } ` Também existem cenários aos quais o IP de origem da requisição pode ser bloqueado. As regras de bloqueios por IP são especificadas abaixo: - 300 erros em 10 segundos, com duração de 10 minutos. - 600 requests em 10 segundos, com duração de 10 minutos. - 20 requests (/oauth/token`) em 60 segundos, com duração de 60 minutos. Com o objetivo de manter a integridade do sistema, se uma aplicação continuar ultrapassando os limites definidos, o IP poderá ser bloqueado por tempo indeterminado.

## [page] MCP Server > Bem-vindo
<https://developer.bling.com.br/mcp-server#bem-vindo>

Seja bem-vindo ao MCP Server do Bling. Aqui você aprende a conectar o seu assistente de IA favorito diretamente à sua operação no Bling. O Bling oferece um servidor MCP (Model Context Protocol) hospedado que dá a assistentes de IA acesso direto à sua conta Bling. Em vez de abrir o painel e navegar entre telas, você pergunta em linguagem natural e o assistente consulta e opera o Bling em seu nome, com dados reais e atualizados da sua conta. Com o MCP conectado, você pode: - Consultar pedidos de venda, notas fiscais, contatos, estoque e contas a pagar/receber sem sair da conversa - Criar e atualizar cadastros, pedidos de venda, pedidos de compra e realizar lançamentos de estoque - Montar relatórios e panoramas sob demanda (financeiro, vendas, operação do dia), cruzando várias consultas de uma vez - Diagnosticar situações comuns, como uma NF-e rejeitada ou um produto perto de zerar no estoque O acesso respeita os limites de permissão da sua conta no painel Bling. Esta página é organizada em duas partes: Para todos (assistentes de chat e produtividade, com detalhamento para ChatGPT e Claude) e Para desenvolvedores (IDEs e CLIs). No final, você também encontra exemplos detalhados de uso no formato prompt, comportamento esperado e resultado.

## [page] MCP Server > Visão geral
<https://developer.bling.com.br/mcp-server#visao-geral>

Um fluxo típico de uso é assim: 1. Entender sua conta: o assistente identifica como sua empresa está organizada: módulos liberados, situações de pedidos e notas, entre outros 2. Consultar: liste pedidos, NF-e, contatos, contas a pagar/receber 3. Criar: registre contatos, pedidos de venda, pedidos de compra, lançamentos de estoque 4. Continuar a conversa: faça novas perguntas sobre o que já foi respondido, sem precisar repetir o contexto

## [page] MCP Server > Ferramentas disponíveis
<https://developer.bling.com.br/mcp-server#ferramentas-disponiveis>

Ferramentas são as ações que o assistente pode executar no Bling: consultar um pedido, listar o estoque, criar um contato, entre outras. Elas ficam organizadas por área do negócio. Categoria Operações principais Catálogo listProducts, getProduct, createProduct, patchProduct, listProductCategories, createProductCategory, listProductGroups, createProductGroup, listProductVariations, listProductBatches Vendas listContacts, getContact, createContact, listProposals, getProposal, createProposal, listSalesOrders, getSalesOrder, createSalesOrder, updateSalesOrderStatus, manageSalesOrderAccounts, manageSalesOrderStock, generateSalesOrderNfe Fiscal listNfes, getNfe, authorizeNfe, listNfces Financeiro listAccountPayables, createAccountPayable, listAccountReceivables, createAccountReceivable, getAccountReceivableBoletos, getBordero Suprimentos listWarehouses, getStockBalance, createStock, listPurchaseOrders, getPurchaseOrder, createPurchaseOrder, updatePurchaseOrderStatus, managePurchaseOrderAccounts, managePurchaseOrderStock, listLogistics, listProductSuppliers, createProductSupplier Sistema listStatusModules, listStatusModuleActions, listStatusModuleTransitions, getCompanyBasicData A tabela acima mostra as principais operações por categoria. Depois de conectar, você pode pedir ao próprio assistente a lista completa e atualizada de ferramentas disponíveis (ex.: "quais ferramentas você tem para consultar o Bling?"). Além das ferramentas, o servidor expõe Recursos, que fornecem contexto adicional para a IA entender a estrutura da API.

## [page] MCP Server > URL do servidor MCP
<https://developer.bling.com.br/mcp-server#url-do-servidor-mcp>

`` https://mcp.bling.com.br/mcp `` Verifique o status do servidor em https://mcp.bling.com.br/health.

## [page] MCP Server > Permissões e acesso
<https://developer.bling.com.br/mcp-server#permissoes-e-acesso>

Conectar não exige nenhuma configuração técnica: qualquer pessoa com uma conta Bling ativa pode fazer login e autorizar o acesso diretamente no cliente de IA escolhido, sem lidar com senhas de API, chaves ou configurações à parte. - O acesso não passa das permissões que a sua conta já tem no painel Bling - Você só vê e opera os módulos liberados para sua empresa (Cadastros, Vendas, Compras, Fiscal, Financeiro, Estoque, etc.) - Não há exposição de dados de outras empresas - Você pode revogar o acesso a qualquer momento (veja Gerenciar suas conexões MCP)

## [page] MCP Server > Conectando seu assistente de IA
<https://developer.bling.com.br/mcp-server#conectando-seu-assistente-de-ia>

Escolha o cliente que você já usa. Se o seu não está listado, veja Outros clientes ou a seção para desenvolvedores.

## [page] MCP Server > Conectando seu assistente de IA > Para todos (assistentes de chat e produtividade) > ChatGPT
<https://developer.bling.com.br/mcp-server#chat-gpt>

Configure a conexão via Custom Connector no Developer Mode: 1. Habilite o Developer Mode em Settings → Apps & Connectors → Advanced settings → Developer mode 2. Clique em Create 3. Preencha: - Name: Bling - Description: Conecte o ChatGPT ao Bling para consultar pedidos, NF-e, estoque e financeiro - Connector URL: https://mcp.bling.com.br/mcp - Authentication: OAuth 4. Complete o fluxo OAuth com sua conta Bling Os nomes exatos dos menus podem mudar conforme o ChatGPT é atualizado. Se não encontrar algum desses itens, procure por "Connectors" ou "MCP" nas configurações. Consulte os planos do ChatGPT que suportam Custom Connectors na documentação da OpenAI.

## [page] MCP Server > Conectando seu assistente de IA > Para todos (assistentes de chat e produtividade) > Claude
<https://developer.bling.com.br/mcp-server#claude>

Configure a conexão via Custom Connector: Claude.ai (web e mobile) 1. Acesse Settings → Connectors → Add Custom Connector 2. Cole https://mcp.bling.com.br/mcp 3. Complete o fluxo OAuth Claude Desktop 1. Abra Settings → Connectors e clique em Add Connector 2. Cole https://mcp.bling.com.br/mcp 3. Complete o fluxo OAuth Os nomes exatos dos menus podem mudar conforme o Claude é atualizado. Se não encontrar algum desses itens, procure por "Connectors" ou "MCP" nas configurações. Consulte os planos do Claude que suportam Custom Connectors na documentação da Anthropic.

## [page] MCP Server > Conectando seu assistente de IA > Para todos (assistentes de chat e produtividade) > Outros clientes
<https://developer.bling.com.br/mcp-server#outros-clientes>

Outros assistentes de chat e produtividade compatíveis com MCP (como Gemini Enterprise, OpenClaw e Notion) também podem conectar. Qualquer cliente compatível com MCP via mcpServers em config JSON pode usar: ``json { "mcpServers": { "bling": { "url": "https://mcp.bling.com.br/mcp" } } } `` No primeiro uso, abre o navegador para autorizar com o Bling.

## [page] MCP Server > Conectando seu assistente de IA > Para desenvolvedores (IDEs e CLIs)
<https://developer.bling.com.br/mcp-server#para-desenvolvedores-ides-e-clis>

Se você desenvolve com a Bling API ou quer integrar o MCP ao seu fluxo de código, qualquer IDE ou CLI compatível com MCP (Cursor, VS Code, Claude Code, Codex, Gemini CLI, Windsurf, Zed, entre outros) pode conectar apontando para a URL do servidor na sua configuração: ``json { "mcpServers": { "bling": { "url": "https://mcp.bling.com.br/mcp" } } } ` Para clientes que ainda não suportam Streamable HTTP nativo, use o bridge mcp-remote: `json { "mcpServers": { "bling": { "command": "npx", "args": ["-y", "mcp-remote", "https://mcp.bling.com.br/mcp"] } } } `` No primeiro uso, o navegador abre para autorizar com sua conta Bling. Consulte a documentação do seu cliente para o formato e o caminho exatos do arquivo de configuração de MCP.

## [page] MCP Server > Fluxos comuns
<https://developer.bling.com.br/mcp-server#fluxos-comuns>

Os fluxos abaixo são prontos para usar: basta colar o prompt no seu assistente conectado.

## [page] MCP Server > Fluxos comuns > Diagnosticar uma NF-e rejeitada
<https://developer.bling.com.br/mcp-server#diagnosticar-uma-nf-e-rejeitada>

Cole a URL ou número da NF-e do painel Bling no chat. O assistente carrega motivo da rejeição, dados do destinatário e produtos para te ajudar a corrigir e reenviar. > "Por que a NF-e número 12345 foi rejeitada? Como corrigir?" > > "Verifique todas as NF-e dos últimos 7 dias e me mostre as que rejeitaram, com o motivo"

## [page] MCP Server > Fluxos comuns > Resumo financeiro do mês
<https://developer.bling.com.br/mcp-server#resumo-financeiro-do-mes>

Pergunte de qualquer cliente conectado e o assistente cruza contas a pagar, a receber e calcula o saldo projetado, já agrupando por vencimento. > "Quanto vou receber e quanto preciso pagar este mês? Liste os 5 maiores vencimentos do mês" > > "Quem são os clientes inadimplentes com boleto vencido?"

## [page] MCP Server > Fluxos comuns > Estoque crítico antes de comprar
<https://developer.bling.com.br/mcp-server#estoque-critico-antes-de-comprar>

Antes de finalizar um pedido de compra, pergunte ao assistente quais produtos estão zerados ou em ruptura. Ele cruza saldo de estoque com vendas médias para sugerir quantidades de reposição. > "Quais produtos estão em ruptura ou prestes a zerar? Sugira quantidade de reposição baseada no giro dos últimos 30 dias" > > "Crie um pedido de compra para o fornecedor X com os itens críticos"

## [page] MCP Server > Fluxos comuns > Mais ideias
<https://developer.bling.com.br/mcp-server#mais-ideias>

Entender o negócio - "Qual o panorama operacional do dia?" - "Quais são meus 5 maiores pedidos de venda este mês?" Consultar pedidos e notas - "Pedidos prontos para envio sem NF-e ou etiqueta gerada" - "Visão 360 do pedido 12345: cliente, produtos, NF-e e logística" Operação de catálogo - "Visão completa do produto X: detalhes, estoque por depósito, giro de vendas" - "Crie a categoria 'Linha Premium'" Conferência fiscal - "Cruze pedidos com NF-e e identifique vendas sem nota e divergências" Operações de cadastro - "Crie um contato pessoa jurídica chamado Empresa Teste LTDA" - "Crie um pedido de venda para o cliente 5678 com 2 unidades do produto 9012"

## [page] MCP Server > Fluxos comuns > Exemplos detalhados
<https://developer.bling.com.br/mcp-server#exemplos-detalhados>

Os exemplos abaixo seguem o formato prompt → comportamento esperado → resultado, mostrando quais ferramentas o assistente encadeia e como fica a resposta final. Os valores são ilustrativos.

## [page] MCP Server > Fluxos comuns > Exemplos detalhados > Resumo financeiro
<https://developer.bling.com.br/mcp-server#resumo-financeiro>

> Prompt: "Faça um resumo financeiro da empresa: o que tenho a pagar e a receber, o saldo projetado e quais contas vencem nos próximos 7 dias." Comportamento esperado: listAccountPayables (em aberto) → listAccountReceivables (pendentes) → o assistente calcula totais, saldo projetado (receber − pagar) e filtra vencimentos dos próximos 7 dias. Resultado: tabela de saldo (a pagar / a receber / saldo projetado), lista de contas a pagar dos próximos 7 dias e maiores valores a receber pendentes.

## [page] MCP Server > Fluxos comuns > Exemplos detalhados > Relatório de vendas de um período
<https://developer.bling.com.br/mcp-server#relatorio-de-vendas-de-um-periodo>

> Prompt: "Gere um relatório de vendas do mês passado: faturamento, ticket médio, ranking de produtos e quantos pedidos ainda estão em aberto." Comportamento esperado: descoberta de situações (listStatusModules + listStatusModuleTransitions, pois os IDs de situação são customizáveis por conta) → listSalesOrders filtrando pelas situações concluídas → getSalesOrder por pedido para montar o ranking → segunda consulta com situações em andamento para contabilizar pedidos abertos. Resultado: faturamento total, ticket médio, top 5 produtos e a contagem de pedidos ainda em aberto no período.

## [page] MCP Server > Fluxos comuns > Exemplos detalhados > Panorama operacional do dia
<https://developer.bling.com.br/mcp-server#panorama-operacional-do-dia>

> Prompt: "Monte o panorama operacional de hoje: vendas, notas fiscais, estoque crítico, expedição pendente e financeiro do dia." Comportamento esperado: listSalesOrders (hoje) + listNfes (hoje) + listProducts (filtrando por saldo em estoque zerado/negativo) + listSalesOrders (últimos 7 dias, não finalizados) + listAccountPayables/listAccountReceivables (vencimento hoje), consolidados em um único dashboard. Resultado: dashboard com vendas e NF-e do dia, contagem de estoque crítico e expedição pendente, financeiro do dia e uma lista de ações imediatas.

## [page] MCP Server > Recursos
<https://developer.bling.com.br/mcp-server#recursos>

Recursos fornecem contexto adicional para a IA entender a estrutura da API. Recurso Descrição bling://catalogo Catálogo de todas as operações disponíveis, agrupadas por domínio bling://enums Valores válidos para cada campo (situações, tipos, etc.) bling://schemas/{slug} Schemas JSON de request/response por domínio bling://guia/situacoes Mapa completo de situações por entidade (NF-e fixa 1-11, pedidos de venda dinâmicos por conta)

## [page] MCP Server > Gerenciar suas conexões MCP
<https://developer.bling.com.br/mcp-server#gerenciar-suas-conexoes-mcp>

Você pode ver e revogar a qualquer momento o acesso do MCP à sua conta Bling. 1. Acesse Aplicativos no painel Bling 2. Localize o aplicativo MCP Bling autorizado 3. Clique em Revogar acesso Após revogar, o cliente conectado perde acesso imediatamente. Para reconectar, refaça o fluxo OAuth no próprio cliente.

## [page] MCP Server > Considerações de segurança
<https://developer.bling.com.br/mcp-server#consideracoes-de-seguranca>

Você confia ao seu assistente de IA o acesso aos dados da sua conta Bling. Revise a política de privacidade do provedor antes de conectar. Quando conectado, o assistente pode consultar e operar o seu Bling em seu nome. Os dados retornados são também enviados ao provedor de IA (OpenAI, Anthropic, Google, etc.); revise as políticas deles. Controles de acesso - A conexão usa OAuth 2.1 com PKCE, e as credenciais não saem do fluxo do Bling - Antes de executar uma operação, o cliente de IA pede sua autorização. Dependendo do cliente, você pode aprovar operação por operação ou permitir sempre para as próximas vezes - Para revogar acesso a qualquer momento, veja Gerenciar suas conexões MCP Boas práticas - As ações executadas afetam dados reais da sua conta. Ao testar, acompanhe os pedidos de autorização e confira o que cada operação faz antes de aprovar, principalmente em criações e alterações - Se você não é o responsável pela conta, alinhe com quem decide na empresa antes de habilitar o acesso - Revogue o acesso pelo painel Bling quando parar de usar um cliente - O tratamento de dados segue a Política de Privacidade do Bling e a LGPD Encontrou uma vulnerabilidade? Quando uma vulnerabilidade ou incidente de segurança afeta a distribuição do Bling MCP Server em um diretório de terceiros, notificamos prontamente, sem atraso injustificado, o canal oficial de segurança da respectiva plataforma: - Bling: Reporte para security@bling.com.br - OpenAI(ChatGPT Apps Directory): via o canal oficial de Coordinated Vulnerability Disclosure da OpenAI, conforme os App Developer Terms.

## [page] MCP Server > Perguntas frequentes > FAQ geral
<https://developer.bling.com.br/mcp-server#faq-geral>

Funciona no celular? Sim. Após conectar o Bling em qualquer cliente (web ou desktop), o connector fica disponível automaticamente nos apps mobile do mesmo provedor. Teste primeiro no desktop e depois experimente no celular. Posso ter mais de uma empresa Bling conectada simultaneamente? Cada cliente MCP autoriza uma conta Bling por vez. Se você gerencia várias empresas, troque de empresa no painel Bling antes de iniciar uma sessão no assistente, ou conecte cada empresa em um cliente diferente (ex.: empresa A no ChatGPT, empresa B no Claude). O assistente tem acesso a tudo no meu Bling? Apenas aos módulos liberados para a sua conta (vendas, compras, fiscal, financeiro, estoque, cadastros, conforme o seu plano). Além disso, é o próprio assistente quem realiza cada consulta ou ação, sempre pedindo sua aprovação antes de agir. Onde eu vejo os assistentes que estão conectados? Vá em Gerenciar suas conexões MCP para ver e revogar o acesso. O Bling cobra a mais por isso? Não há cobrança adicional pelo uso do MCP. As requisições feitas pelo assistente em seu nome usam os limites de requisições da API já contratados no seu plano Bling. Veja Limites.

## [page] MCP Server > Perguntas frequentes > FAQ para desenvolvedores
<https://developer.bling.com.br/mcp-server#faq-para-desenvolvedores>

Suporta WSL no Windows? Sim. Para clientes que rodam em WSL com mcp-remote, use: ``json { "mcpServers": { "bling": { "command": "wsl", "args": ["npx", "-y", "mcp-remote", "https://mcp.bling.com.br/mcp"] } } } ` O servidor suporta SSE legado ou apenas Streamable HTTP? Hoje suporta apenas Streamable HTTP (/mcp`), o transporte atual do protocolo MCP, que substituiu o SSE usado em versões antigas da especificação. Isso não tem relação com criptografia: a conexão sempre acontece via HTTPS.

## [page] MCP Server > Limites
<https://developer.bling.com.br/mcp-server#limites>

O MCP usa os mesmos limites de requisições da API já contratados no seu plano Bling, sem um limite adicional específico para o MCP. Quando o limite é atingido, o servidor aplica retry automático com backoff exponencial.

## [page] MCP Server > Verificar o servidor
<https://developer.bling.com.br/mcp-server#verificar-o-servidor>

Healthcheck: `` https://mcp.bling.com.br/health ` Retorna {"status":"ok"}` se o servidor está operacional.

## [page] MCP Server > Precisando de ajuda?
<https://developer.bling.com.br/mcp-server#precisando-de-ajuda>

Dúvidas sobre o MCP ou problemas de conexão: suporte.plataforma@bling.com.br. Para reportar uma vulnerabilidade de segurança, veja Considerações de segurança.

## [page] Migração para autenticação JWT > Introdução
<https://developer.bling.com.br/migracao-jwt#introducao>

Este guia aborda detalhadamente a ativação e o uso de JSON Web Tokens (JWT) na API do Bling além de apresentar as instruções necessárias para a implementação dessa evolução em nossa arquitetura tecnológica e destacar os principais benefícios proporcionados por essa mudança. <hr> Os principais tópicos da alteração que serão explicados detalhadamente nas seções subsequentes: - A data de bloqueio do uso de tokens opacos está em definição. - A autenticação utilizando tokens opacos está descontinuada. - Alteração no tamanho do token gerado. - Para obter JWT: Inclua o header enable-jwt: 1 ao obter um token por meio do endpoint POST /oauth/token. É fundamental manter este header em todas as requisições subsequentes para garantir que os tokens JWT continuem sendo emitidos após renovações. - Para renovar JWT: Inclua o header enable-jwt: 1 também na requisição de renovação do token para continuar recebendo tokens JWT. - Para usar JWT: Envie o header Authorization: Bearer {token} em todas as requisições à API que exigem autenticação. <hr>

## [page] Migração para autenticação JWT > Motivação da alteração
<https://developer.bling.com.br/migracao-jwt#motivacao-da-alteracao>

Antes dessa evolução, a API do Bling somente utilizava tokens opacos para autenticação. Esse tipo de token é apenas uma referência, um identificador aleatório. Quando a API recebe um token opaco, o sistema precisa consultar um banco de dados ou mecanismo de cache centralizado para validar quem é o usuário e quais são suas permissões. Com o JWT essa abordagem mudou. Trata-se de um token estruturado e auto contido, ou seja, as informações sobre o usuário, a empresa e os escopos de permissão ficam codificadas no próprio token.

## [page] Migração para autenticação JWT > Ganhos computacionais e de infraestrutura
<https://developer.bling.com.br/migracao-jwt#ganhos-computacionais-e-de-infraestrutura>

A adoção do JWT traz benefícios imediatos para a latência das requisições e uso de recursos computacionais: - Redução de I/O (Stateless): Ao usar JWT, a API não precisa necessariamente consultar o banco de dados para validar o token a cada requisição. A validação é feita criptograficamente (CPU), sendo computacionalmente mais eficiente do que operações de entrada/saída (I/O) em disco ou rede para buscar sessões em banco de dados. - Escalabilidade: Como o token carrega os dados necessários, a arquitetura torna-se stateless (sem estado). Isso facilita a escala horizontal dos serviços, pois qualquer servidor pode validar o token sem depender de uma central de sessões. - Eficiência de Rede: Embora o JWT seja maior do que um token opaco, a eliminação da necessidade de consultas adicionais ao banco de dados (round-trips) compensa o aumento do payload, especialmente em cenários de alta concorrência.

## [page] Migração para autenticação JWT > Estrutura e tamanho do token
<https://developer.bling.com.br/migracao-jwt#estrutura-e-tamanho-do-token>

Diferente dos tokens opacos curtos, o JWT carrega um payload de dados em Base64. Com base na estrutura atual de informações contidas (claims), o tamanho de um token JWT pode variar aproximadamente de 1.500 a 3.000 caracteres. <span style="color: #F05143;">Atenção: </span>É essencial que sua aplicação esteja preparada para armazenar e trafegar strings desse tamanho nos headers de autorização.

## [page] Migração para autenticação JWT > Utilizando JWT no Bling
<https://developer.bling.com.br/migracao-jwt#utilizando-jwt-no-bling>

Por padrão, a API do Bling retorna tokens opacos, contudo, esse modelo de autenticação está descontinuado. Para receber um token JWT ao invés de um token opaco, você deve incluir o header enable-jwt com o valor 1 na requisição ao endpoint POST /oauth/token. Importante: Sem o header enable-jwt, você receberá um token opaco que continuará funcionando até a migração total para o JWT. Migre o quanto antes, não deixe para o último momento.

## [page] Migração para autenticação JWT > Utilizando JWT no Bling > Exemplo de obtenção de token JWT
<https://developer.bling.com.br/migracao-jwt#exemplo-de-obtencao-de-token-jwt>

``http POST /Api/v3/oauth/token? HTTP/1.1 Host: https://api.bling.com.br Content-Type: application/x-www-form-urlencoded Accept: 1.0 Authorization: Basic [base64_das_credenciais_do_client_app] enable-jwt: 1 grant_type=authorization_code&code=[authorization_code] ` `bash curl -X POST "https://api.bling.com.br/oauth/token" \\ -H "Content-Type: application/x-www-form-urlencoded" \\ -H "Authorization: Basic [base64_das_credenciais_do_client_app]" \\ -H "enable-jwt: 1" \\ -d "grant_type=authorization_code&code=[authorization_code]" ``

## [page] Migração para autenticação JWT > Utilizando JWT no Bling > Exemplo de renovação de token JWT
<https://developer.bling.com.br/migracao-jwt#exemplo-de-renovacao-de-token-jwt>

``http POST /Api/v3/oauth/token? HTTP/1.1 Host: https://api.bling.com.br Content-Type: application/x-www-form-urlencoded Accept: 1.0 Authorization: Basic [base64_das_credenciais_do_client_app] enable-jwt: 1 grant_type=refresh_token&refresh_token=[refresh_token] ` `bash curl -X POST "https://api.bling.com.br/oauth/token" \\ -H "Content-Type: application/x-www-form-urlencoded" \\ -H "Authorization: Basic [base64_das_credenciais_do_client_app]" \\ -H "enable-jwt: 1" \\ -d "grant_type=refresh_token&refresh_token=[refresh_token]" ``

## [page] Migração para autenticação JWT > Utilizando JWT no Bling > Usando o token JWT nas requisições
<https://developer.bling.com.br/migracao-jwt#usando-o-token-jwt-nas-requisicoes>

Após obter o token JWT através do endpoint POST /oauth/token, você deve incluí-lo em todas as requisições subsequentes à API. É fundamental que o header enable-jwt: 1 seja mantido em todas as requisições para garantir a compatibilidade e o processamento correto da autenticação JWT pela API. Este header deve ser incluído em todas as requisições que exigem autenticação, como consultar produtos, criar pedidos, etc. Exemplo de requisição para a API de produtos: ``http GET /Api/v3/produtos HTTP/1.1 Host: https://api.bling.com.br Authorization: Bearer [access_token] enable-jwt: 1 ` `bash curl --location --request GET 'https://api.bling.com.br/Api/v3/produtos' \\ --header 'Authorization: Bearer [access_token]' \\ --header 'Content-Type: application/json' \\ --header 'enable-jwt: 1' ``

## [page] Migração para autenticação JWT > Tratamento de erros comuns
<https://developer.bling.com.br/migracao-jwt#tratamento-de-erros-comuns>

Ao implementar o uso do JWT, atente-se aos seguintes códigos de retorno: <hr> 401 Unauthorized: Indica que o token expirou ou é inválido. Solução: Renove o token usando o refresh_token (lembrando do header enable-jwt: 1) ou refaça o fluxo de autorização OAuth. <hr> 400 Bad Request: Geralmente indica token malformado ou erro na sintaxe do header. Solução: Verifique se o header segue estritamente o formato: Authorization: Bearer {token}. <hr> Dúvidas? Entre em contato com nossa equipe de atendimento.

## [page] Perguntas frequentes > Como gerar o Access Token?
<https://developer.bling.com.br/perguntas-frequentes#como-gerar-o-access-token>

O primeiro passo é a criação de um aplicativo. Após o desenvolvedor irá solicitar por meio do aplicativo, acesso à conta do Bling que deseja operar. Nesse momento o cliente que opera a conta irá fazer login e autorizar o aplicativo a realizar as operações na mesma, retornando de forma automática o authorization code na URL de redirecionamento configurada no aplicativo. Por fim, será necessário o desenvolvedor realizar uma requisição ao authorization server com o authorization code obtido, e então o access token será retornado no formato JSON. Para o passo a passo detalhado, acesse a seção de fluxo de autorização.

## [page] Perguntas frequentes > Como gerar o client_id e o client_secret?
<https://developer.bling.com.br/perguntas-frequentes#como-gerar-o-client-id-e-o-client-secret>

Após a criação do aplicativo, será exibido ao lado do formulário o client_id e client_secret.

## [page] Perguntas frequentes > Qual é o formato de retorno das respostas da API?
<https://developer.bling.com.br/perguntas-frequentes#qual-e-o-formato-de-retorno-das-respostas-da-api>

O formato de retorno é em JSON, conforme o exemplo: `` { "data": { "id": 123, "nome": "Bling", "numero": 1 } } ``

## [page] Perguntas frequentes > Quais são os limites da API?
<https://developer.bling.com.br/perguntas-frequentes#quais-sao-os-limites-da-api>

No Bling existem limites de frequência, no qual a regra permite até 3 requisições por segundo e 120 mil requisições por dia. Entretanto, existe também outras validações por bloqueio de IP. A limitação de API é o processo de limitar o número de requisições que um usuário pode fazer em um determinado período.

## [page] Perguntas frequentes > Quantos registros são retornados por página em cada requisição?
<https://developer.bling.com.br/perguntas-frequentes#quantos-registros-sao-retornados-por-pagina-em-cada-requisicao>

Por padrão são retornados até 100 registros por requisição. APIs que possuem paginação irão retornar os resultados em páginas, ou seja, para obter todos os registros serão necessárias mais de uma requisição, informando o parâmetro pagina. Mais informações podem ser encontradas na seção de boas práticas.

## [page] Perguntas frequentes > Qual é a utilidade do campo state?
<https://developer.bling.com.br/perguntas-frequentes#qual-e-a-utilidade-do-campo-state>

A utilidade principal do campo state é evitar cross-site request forgery (CSRF) para o endpoint configurado na URL de redirecionamento do aplicativo. O client app gera um token aleatório e o informa no campo state ao solicitar o Authorization code, após o usuário conceder acesso ao aplicativo, o token é retornado ao client app junto à URL de redirecionamento, dessa forma, é possível verificar que a origem é de fato o Bling. Além disso, pode ser usado de maneira flexível, já que é possível informar qualquer valor para o campo e reinterpretá-lo no redirecionamento. Por exemplo, criptografando um json contendo um timestamp e um ambiente {"timestamp":1698757251.796,"environment":"dev"}, após o redirecionamento ao client app, é possível descriptografar o state e verificar se o processo foi realizado em tempo hábil e se o ambiente que o usuário está é valido para a utilização do aplicativo.

## [page] Perguntas frequentes > Como emitir uma nota de venda com itens de brinde ou bonificação?
<https://developer.bling.com.br/perguntas-frequentes#como-emitir-uma-nota-de-venda-com-itens-de-brinde-ou-bonificacao>

É possível emitir uma única NF-e com itens de venda e itens de brinde ou bonificação juntos, cada um com seu próprio CFOP, vinculando uma natureza de operação específica a cada item especial do pedido de venda. 1. Cadastre uma natureza de operação com o CFOP e as regras fiscais de brinde/bonificação. Esse cadastro é manual, não existindo endpoint de criação via API. Dessa forma, alinhe os dados com seu contador. 2. Liste as naturezas de operação e localize o id da que foi configurada para esse fim: GET /naturezas-operacoes?situacao=1&descricao=Bonificação. 3. Ao criar ou atualizar o pedido de venda, informe naturezaOperacao.id no item que deve sair como brinde/bonificação. Os demais itens não precisam ter a natureza vinculada pois ao gerar a nota o sistema atribuirá de forma automática, conforme cadastro prévio. ``json { "itens": [ { "descricao": "Produto A", "quantidade": 2, "valor": 49.90 }, { "descricao": "Produto B", "quantidade": 1, "valor": 0, "naturezaOperacao": { "id": 12345678 } } ] } ` 4. Ao gerar a NF-e a partir do pedido, o item que recebeu essa natureza de operação usa o CFOP e as regras fiscais configuradas nela. A natureza de operação precisa existir e estar ativa (situacao=1`), caso contrário a API retorna erro de natureza de operação inválida ou inativa.

## [page] Perguntas frequentes > Preciso criar uma conta no Bling para utilizar a API?
<https://developer.bling.com.br/perguntas-frequentes#preciso-criar-uma-conta-no-bling-para-utilizar-a-api>

Sim. A utilização da API do Bling requer a criação de uma conta, para cadastro de um aplicativo de visibilidade pública. É necessário também passar por um processo de homologação, o qual assegura a conformidade da conta com os padrões exigidos pela API. Concluída a etapa de testes de 30 dias, a conta permanece ativa, dispensando a necessidade de solicitar isenções para prosseguir com o uso do serviço.

## [page] Webhooks > Introdução
<https://developer.bling.com.br/webhooks#introducao>

Webhook é um método de comunicação utilizado para que aplicativos e sistemas se comuniquem em tempo real de forma reativa e acontece sempre que um evento específico ocorre em uma das aplicações. Para exemplificar o uso de webhooks, imagine que, a cada produto cadastrado, atualizado ou excluído no Bling, seja necessário realizar a mesma operação em outro sistema. Em vez de criar uma rotina que periodicamente consulte a API do Bling para verificar alterações, é possível configurar webhooks para que sejam acionados automaticamente a cada uma dessas ações. Dessa forma, o sistema receberá os dados em tempo real, processará as informações necessárias e evitará o uso de rotinas automáticas que demandem consultas constantes ao Bling.

## [page] Webhooks > Como cadastrar
<https://developer.bling.com.br/webhooks#como-cadastrar>

1. Acesse o aplicativo já cadastrado. 2. Certifique-se que o aplicativo possua os escopos referentes aos recursos aos quais queira ser notificado. Caso o aplicativo não possua um escopo específico, o recurso de webhook correspondente não será exibido para configurar. 3. Navegue até a aba "Webhooks". 4. Configure os servidores que receberão os eventos. 5. Configure os recursos que deseja receber as notificações. - Selecione o servidor que deseja receber o evento. - Marque as ações que deseja ser notificado. - Selecione a versão do _payload_ conforme a estrutura de retorno. 6. Salve as alterações.

## [page] Webhooks > Recebimento de eventos
<https://developer.bling.com.br/webhooks#recebimento-de-eventos>

O aplicativo começará a receber os eventos após a obtenção dos tokens de acesso do usuário ao final do fluxo de autorização.

## [page] Webhooks > Webhooks vs Polling > Atualização de informações
<https://developer.bling.com.br/webhooks#atualizacao-de-informacoes>

Webhooks e polling são duas técnicas amplamente utilizadas para integração de sistemas e comunicação entre aplicações. Ambos os métodos têm como objetivo transferir informações entre sistemas, mas funcionam de maneira fundamentalmente diferente. A escolha entre webhooks e polling depende do caso de uso, das demandas de desempenho e das restrições do sistema.

## [page] Webhooks > Webhooks vs Polling > Webhooks
<https://developer.bling.com.br/webhooks#webhooks-1>

Webhooks são uma abordagem baseada em eventos, onde um servidor é configurado para enviar notificações para outro sistema sempre que um determinado evento ocorre. Isso é feito através de requisições HTTP para um endpoint previamente definido. O uso de webhooks reduz a sobrecarga de requisições desnecessárias, enviando apenas quando há dados novos.

## [page] Webhooks > Webhooks vs Polling > Polling
<https://developer.bling.com.br/webhooks#polling>

Polling é uma técnica onde um sistema consulta periodicamente o servidor de origem para verificar se há novos dados ou atualizações. Nesse modelo, o cliente faz requisições repetitivas, independentemente de haver ou não dados novos. Em relação ao webhook, é menos eficiente, visto que podem ser realizadas muitas requisições sem dados novos.

## [page] Webhooks > Autenticação > Técnica
<https://developer.bling.com.br/webhooks#tecnica>

A autenticação das mensagens enviadas pelo Bling deve ser realizada por meio do cabeçalho HTTP X-Bling-Signature-256. Esse cabeçalho contém um hash de autenticação HMAC (Hash-Based Message Authentication Code) composto pelo payload JSON da resposta e o client secret do aplicativo. Esse processo garante a integridade e a autenticidade dos dados enviados pelo Bling.

## [page] Webhooks > Autenticação > Validação do hash
<https://developer.bling.com.br/webhooks#validacao-do-hash>

Para garantir que a mensagem recebida é legítima e não foi manipulada, considere os seguintes passos: 1. Gerar um hash HMAC utilizando o payload e o client secret do aplicativo. 2. Comparar se o hash informado no header X-Bling-Signature-256 é igual ao hash gerado. Exemplo de hashes: - Hash gerado: a012da891d0cebcb375c8e12b881e81df40256dfffc25e08ba9db4ab35515516 - Header informado na requisição: sha256=a012da891d0cebcb375c8e12b881e81df40256dfffc25e08ba9db4ab35515516 Observações: - O Bling usa um código hash hexadecimal HMAC para calcular o hash. - A assinatura do hash sempre começa com sha256=. - O padrão de codificação utilizado é o UTF-8.

## [page] Webhooks > Idempotência
<https://developer.bling.com.br/webhooks#idempotencia>

Idempotência é a capacidade de uma operação retornar o mesmo resultado, independentemente de quantas vezes seja executada, desde que os parâmetros sejam os mesmos. No contexto de webhooks, caso o Bling envie o mesmo webhook duas vezes, sua aplicação deve responder a ambas as requisições com um código HTTP 2xx.

## [page] Webhooks > Entrega não ordenada
<https://developer.bling.com.br/webhooks#entrega-nao-ordenada>

Não há garantia da entrega dos eventos na ordem em que foram gerados. Por exemplo, um webhook de atualização de produto pode ser recebido antes que o webhook de criação deste mesmo produto. Uma prática recomendada para lidar com esse cenário é gerenciar os webhooks recebidos de maneira assíncrona, usando filas, por exemplo.

## [page] Webhooks > Retentativas
<https://developer.bling.com.br/webhooks#retentativas>

O processo de retentativas foi projetado para garantir a entrega confiável de webhooks aos integradores, mesmo diante de falhas temporárias no sistema de destino. Serão feitas tentativas no período máximo de 3 dias onde, a cada retentativa, o tempo da próxima retentativa poderá ser maior. Ao final do processo de retentativas, caso o processamento do evento continue com problemas, a configuração do webhook para o recurso em questão será desabilitada e o Bling não enviará novos eventos até que a configuração seja habilitada manualmente através das configurações de webhooks do aplicativo. Uma requisição é considerada entregue com sucesso quando o integrador responde com um código HTTP 2xx em até 5 segundos. Caso exceda o tempo de resposta ou o código for diferente de 2xx serão feitas as retentativas no envio da mensagem.

## [page] Webhooks > Ações
<https://developer.bling.com.br/webhooks#acoes>

Abaixo estão detalhadas as ações disponíveis: - created: Ocorre quando um recurso é criado. - updated: Ocorre quando um recurso é atualizado. - deleted: Ocorre quando um recurso é deletado definitivamente. - Alterar a situação de um recurso para excluído gera um evento de updated.

## [page] Webhooks > Recursos > Recursos disponíveis
<https://developer.bling.com.br/webhooks#recursos-disponiveis>

Antes de configurar um recurso de webhook, é necessário adicionar o escopo referente ao recurso aos dados básicos do aplicativo. - Pedido de Venda: order - Produto: product - Estoque: stock - Estoque virtual: virtual_stock - Produto fornecedor: product_supplier - Nota fiscal: invoice - Nota fiscal de consumidor: consumer_invoice O webhook de Estoque Virtual é ativado automaticamente quando o de Estoque é habilitado, por esse motivo, herdará suas configurações.

## [page] Webhooks > Recursos > Recursos disponíveis > Diferenças entre eventos de estoque e estoque virtual
<https://developer.bling.com.br/webhooks#diferencas-entre-eventos-de-estoque-e-estoque-virtual>

Os payloads não são as únicas diferenças entre os eventos. Os gatilhos também variam: - Eventos de estoque são disparados apenas por lançamentos físicos, ou seja, lançamentos de estoque por vendas, NF-es, tela de estoque, etc. - Eventos de estoque virtual são disparados por reservas de vendas e atualização de saldo em produtos com composição e tipo de estoque virtual.

## [page] Webhooks > Recursos > Estrutura de retorno
<https://developer.bling.com.br/webhooks#estrutura-de-retorno>

`` { "eventId": "01945027-150e-72b4-e7cf-4943a042cd9c", "date": "2025-01-10T12:18:46Z", "version": "v1", "event": "$resource.$action", "companyId": "d4475854366a36c86a37e792f9634a51", "data": $payload } ` Detalhamento dos campos: - eventId: Identificador único do evento. - date: Data no formato ISO 8601. - version: Versão do webhook. - event: Recurso junto a ação separados por ".". - companyId: ID da empresa. - Para obtê-lo, consulte os dados básicos da empresa por API. - data: Payload do evento. Considere: - $resource: O recurso do webhook. - $action: A ação do webhook. - $payload`: Uma das estruturas abaixo, conforme o recurso e a ação do webhook.

## [page] Webhooks > Recursos > Pedido de venda
<https://developer.bling.com.br/webhooks#pedido-de-venda>

Estrutura dos payloads dos webhooks de pedido de venda:

## [page] Webhooks > Recursos > Pedido de venda > Versão 1
<https://developer.bling.com.br/webhooks#versao-1>

Created Updated Deleted <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "data": "2024-09-25",&#10; "numero": 123,&#10; "numeroLoja": "Loja_123",&#10; "total": 123.45,&#10; "contato": {&#10; "id": 12345678&#10; },&#10; "vendedor": {&#10; "id": 12345678&#10; },&#10; "loja": {&#10; "id": 12345678&#10; },&#10; "situacao": {&#10; "id": 12345678,&#10; "valor": 12345678&#10; }&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "data": "2024-09-25",&#10; "numero": 123,&#10; "numeroLoja": "Loja_123",&#10; "total": 123.45,&#10; "contato": {&#10; "id": 12345678&#10; },&#10; "vendedor": {&#10; "id": 12345678&#10; },&#10; "loja": {&#10; "id": 12345678&#10; },&#10; "situacao": {&#10; "id": 12345678,&#10; "valor": 12345678&#10; }&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678&#10;}&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;</code></pre>

## [page] Webhooks > Recursos > Produto
<https://developer.bling.com.br/webhooks#produto>

Estrutura dos payloads dos webhooks de produto:

## [page] Webhooks > Recursos > Produto > Versão 1
<https://developer.bling.com.br/webhooks#versao-1-1>

Created Updated Deleted <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "nome": "Copo do Bling",&#10; "codigo": "COD-4587",&#10; "tipo": "P",&#10; "situacao": "A",&#10; "preco": 4.99,&#10; "unidade": "UN",&#10; "formato": "S",&#10; "idProdutoPai": 12345678,&#10; "categoria": {&#10; "id": 12345679&#10; },&#10; "descricaoCurta": "Descrição curta",&#10; "descricaoComplementar": "Descrição complementar"&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "nome": "Copo do Bling",&#10; "codigo": "COD-4587",&#10; "tipo": "P",&#10; "situacao": "A",&#10; "preco": 4.99,&#10; "unidade": "UN",&#10; "formato": "S",&#10; "idProdutoPai": 12345678,&#10; "categoria": {&#10; "id": 12345679&#10; },&#10; "descricaoCurta": "Descrição curta",&#10; "descricaoComplementar": "Descrição complementar"&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678&#10;}&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;</code></pre>

## [page] Webhooks > Recursos > Estoque
<https://developer.bling.com.br/webhooks#estoque>

Estrutura dos payloads dos webhooks de estoque:

## [page] Webhooks > Recursos > Estoque > Versão 1
<https://developer.bling.com.br/webhooks#versao-1-2>

Created Updated Deleted <pre><code class="language-javascript">{&#10; "produto": {&#10; "id": 12345678&#10; },&#10; "deposito": {&#10; "id": 12345678,&#10; "saldoFisico": 1250.75,&#10; "saldoVirtual": 1250.75&#10; },&#10; "operacao": "E",&#10; "quantidade": 25,&#10; "saldoFisicoTotal": 1500.75,&#10; "saldoVirtualTotal": 1500.75&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "produto": {&#10; "id": 12345678&#10; },&#10; "deposito": {&#10; "id": 12345678,&#10; "saldoFisico": 1250.75,&#10; "saldoVirtual": 1250.75&#10; },&#10; "operacao": "E",&#10; "quantidade": 26,&#10; "saldoFisicoTotal": 1500.75,&#10; "saldoVirtualTotal": 1500.75&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "produto": {&#10; "id": 12345678&#10; },&#10; "deposito": {&#10; "id": 12345678,&#10; "saldoFisico": 1250.75,&#10; "saldoVirtual": 1250.75&#10; },&#10; "saldoFisicoTotal": 1500.75,&#10; "saldoVirtualTotal": 1500.75&#10;}&#10;&#10;&#10;</code></pre>

## [page] Webhooks > Recursos > Estoque Virtual
<https://developer.bling.com.br/webhooks#estoque-virtual>

Estrutura do payload do webhook de estoque virtual:

## [page] Webhooks > Recursos > Estoque Virtual > Versão 1
<https://developer.bling.com.br/webhooks#versao-1-3>

Updated <pre><code class="language-javascript">{&#10; "produto": {&#10; "id": 12345&#10; },&#10; "saldoFisicoTotal": 150.75,&#10; "saldoVirtualTotal": 148.50,&#10; "vinculoComplexo": true,&#10; "depositos": [&#10; {&#10; "id": 1,&#10; "saldoFisico": 75.25,&#10; "saldoVirtual": 73.00&#10; },&#10; {&#10; "id": 2,&#10; "saldoFisico": 75.50,&#10; "saldoVirtual": 75.50&#10; }&#10; ]&#10;}</code></pre> O campo vinculoComplexo indica que o produto possui mais de 200 produtos vinculados (componentes ou composições) que tiveram seu estoque virtual atualizado e seus saldos devem ser obtidos através da API.

## [page] Webhooks > Recursos > Produto fornecedor
<https://developer.bling.com.br/webhooks#produto-fornecedor>

Estrutura dos payloads dos webhooks de produto fornecedor:

## [page] Webhooks > Recursos > Produto fornecedor > Versão 1
<https://developer.bling.com.br/webhooks#versao-1-4>

Created Updated Deleted <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "descricao": "Copo do Bling",&#10; "codigo": "COD-123",&#10; "precoCusto": 3.9,&#10; "precoCompra": 3.5,&#10; "padrao": false,&#10; "garantia": 3,&#10; "produto": {&#10; "id": 12345678&#10; },&#10; "fornecedor": {&#10; "id": 12345678&#10; }&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "descricao": "Copo do Bling",&#10; "codigo": "COD-123",&#10; "precoCusto": 3.9,&#10; "precoCompra": 3.5,&#10; "padrao": true,&#10; "garantia": 5,&#10; "produto": {&#10; "id": 12345678&#10; },&#10; "fornecedor": {&#10; "id": 12345678&#10; }&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678&#10;}&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;</code></pre>

## [page] Webhooks > Recursos > Nota fiscal eletrônica e de consumidor
<https://developer.bling.com.br/webhooks#nota-fiscal-eletronica-e-de-consumidor>

Estrutura dos payloads dos webhooks de nota fiscal eletrônica e de consumidor:

## [page] Webhooks > Recursos > Nota fiscal eletrônica e de consumidor > Versão 1
<https://developer.bling.com.br/webhooks#versao-1-5>

Created Updated Deleted <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "tipo": 1,&#10; "situacao": 1,&#10; "numero": "1234",&#10; "dataEmissao": "2024-09-27 11:24:56",&#10; "dataOperacao": "2024-09-27 11:00:00",&#10; "contato": {&#10; "id": 12345678&#10; },&#10; "naturezaOperacao": {&#10; "id": 12345678&#10; },&#10; "loja": {&#10; "id": 12345678&#10; }&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678,&#10; "tipo": 1,&#10; "situacao": 1,&#10; "numero": "1234",&#10; "dataEmissao": "2024-09-27 11:24:56",&#10; "dataOperacao": "2024-09-27 11:00:00",&#10; "contato": {&#10; "id": 12345678&#10; },&#10; "naturezaOperacao": {&#10; "id": 12345678&#10; },&#10; "loja": {&#10; "id": 12345678&#10; }&#10;}</code></pre> <pre><code class="language-javascript">{&#10; "id": 12345678&#10;}&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;&#10;</code></pre>

## [page] Webhooks > Recursos > Exemplo de retorno
<https://developer.bling.com.br/webhooks#exemplo-de-retorno>

Para exemplicicar, conforme a estrutura de retorno, em uma ação de atualização no recurso de produtos, teríamos o seguinte payload: `` { "eventId": "01945027-150e-72b4-e7cf-4943a042cd9c", "date": "2025-01-10T12:18:46Z", "version": "v1", "event": "product.updated", "companyId": "d4475854366a36c86a37e792f9634a51", "data": { "id": 12345678, "nome": "Copo do Bling", "codigo": "COD-4587", "tipo": "P", "situacao": "A", "preco": 4.99, "unidade": "UN", "formato": "S", "idProdutoPai": 12345678, "categoria": { "id": 12345679 }, "descricaoCurta": "Descrição curta", "descricaoComplementar": "Descrição complementar" } } ``

