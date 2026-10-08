# Bling API v3 — inventário completo de endpoints

265 operações. Extraído do índice de busca de developer.bling.com.br.


## Anúncios

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/anuncios` | `get_anuncios` | Obtém anúncios paginados. |
| POST | `/anuncios` | `post_anuncios` | Cria um anúncio. |
| DELETE | `/anuncios/{idAnuncio}` | `delete_anuncios__idAnuncio_` | Remove um anúncio pelo ID. |
| GET | `/anuncios/{idAnuncio}` | `get_anuncios__idAnuncio_` | Obtém os detalhes de um anúncio específico pelo seu ID. |
| PUT | `/anuncios/{idAnuncio}` | `put_anuncios__idAnuncio_` | Altera um anúncio pelo ID. |
| POST | `/anuncios/{idAnuncio}/pausar` | `post_anuncios__idAnuncio__pausar` | Altera o status do anúncio para pausado. |
| POST | `/anuncios/{idAnuncio}/publicar` | `post_anuncios__idAnuncio__publicar` | Altera o status do anúncio para publicado. |

## Anúncios - Categorias

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/anuncios/categorias` | `get_anuncios_categorias` | Obtém categorias de anúncios. |
| GET | `/anuncios/categorias/{idCategoria}` | `get_anuncios_categorias__idCategoria_` | Obtém uma categoria de anúncio pelo ID. |

## Borderôs

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/borderos/{idBordero}` | `delete_borderos__idBordero_` | Remove um borderô pelo ID. |
| GET | `/borderos/{idBordero}` | `get_borderos__idBordero_` | Obtém um borderô pelo ID. |

## Caixas e Bancos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/caixas` | `get_caixas` | Obtém lista de lançamentos de caixas e bancos. |
| POST | `/caixas` | `post_caixas` | Cria um novo lançamento de caixa e banco com os dados fornecidos. |
| DELETE | `/caixas/{idCaixa}` | `delete_caixas__idCaixa_` | Remove um lançamento de caixa e banco pelo ID. O registro não é excluído permanentemente, apenas marcado como excluído ( |
| GET | `/caixas/{idCaixa}` | `get_caixas__idCaixa_` | Obtém um lançamento de caixa e banco. |
| PUT | `/caixas/{idCaixa}` | `put_caixas__idCaixa_` | Atualiza um lançamento de caixa e banco existente com os dados fornecidos. |

## Campos Customizados

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/campos-customizados` | `post_campos_customizados` | Cria um campo customizado. |
| GET | `/campos-customizados/modulos` | `get_campos_customizados_modulos` | Obtém módulos que possuem campos customizados. |
| GET | `/campos-customizados/modulos/{idModulo}` | `get_campos_customizados_modulos__idModulo_` | Obtém campos customizados por módulo paginados. |
| GET | `/campos-customizados/tipos` | `get_campos_customizados_tipos` | Obtém tipos de campos customizados. |
| DELETE | `/campos-customizados/{idCampoCustomizado}` | `delete_campos_customizados__idCampoCustomizado_` | Remove um campo customizado pelo ID. |
| GET | `/campos-customizados/{idCampoCustomizado}` | `get_campos_customizados__idCampoCustomizado_` | Obtém um campo customizado pelo ID. |
| PUT | `/campos-customizados/{idCampoCustomizado}` | `put_campos_customizados__idCampoCustomizado_` | Altera um campo customizado pelo ID. |
| PATCH | `/campos-customizados/{idCampoCustomizado}/situacoes` | `patch_campos_customizados__idCampoCustomizado__situacoes` | Altera a situação de um campo customizado pelo ID. |

## Canais de Venda

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/canais-venda` | `get_canais_venda` | Obtém canais de venda paginados. |
| GET | `/canais-venda/tipos` | `get_canais_venda_tipos` | Obtém os tipos de canais de venda paginados. |
| GET | `/canais-venda/{idCanalVenda}` | `get_canais_venda__idCanalVenda_` | Obtém uma canal de venda pelo ID. |

## Categorias - Lojas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/categorias/lojas` | `get_categorias_lojas` | Obtém categorias de lojas virtuais vinculadas a de produtos paginadas. |
| POST | `/categorias/lojas` | `post_categorias_lojas` | Cria o vínculo de uma categoria da loja com a de produto. |
| DELETE | `/categorias/lojas/{idCategoriaLoja}` | `delete_categorias_lojas__idCategoriaLoja_` | Remove o vínculo de uma categoria da loja com a de produto pelo ID. |
| GET | `/categorias/lojas/{idCategoriaLoja}` | `get_categorias_lojas__idCategoriaLoja_` | Obtém uma categoria da loja vinculada a de produto pelo ID. |
| PUT | `/categorias/lojas/{idCategoriaLoja}` | `put_categorias_lojas__idCategoriaLoja_` | Altera o vínculo de uma categoria da loja com a de produto pelo ID. |

## Categorias - Produtos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/categorias/produtos` | `get_categorias_produtos` | Obtém categorias de produtos paginadas. |
| POST | `/categorias/produtos` | `post_categorias_produtos` | Cria uma categoria de produto. |
| DELETE | `/categorias/produtos/{idCategoriaProduto}` | `delete_categorias_produtos__idCategoriaProduto_` | Remove uma categoria de produto pelo ID. |
| GET | `/categorias/produtos/{idCategoriaProduto}` | `get_categorias_produtos__idCategoriaProduto_` | Obtém uma categoria de produto pelo ID. |
| PUT | `/categorias/produtos/{idCategoriaProduto}` | `put_categorias_produtos__idCategoriaProduto_` | Altera uma categoria de produto pelo ID. |

## Categorias - Receitas e Despesas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/categorias/receitas-despesas` | `delete_categorias_receitas_despesas` | Remove múltiplas categorias de receita e despesa a partir de uma lista de IDs. |
| GET | `/categorias/receitas-despesas` | `get_categorias_receitas_despesas` | Obtém categorias de receitas e despesas paginadas. |
| POST | `/categorias/receitas-despesas` | `post_categorias_receitas_despesas` | Cria uma categoria de receita e despesa. |
| DELETE | `/categorias/receitas-despesas/{idCategoria}` | `delete_categorias_receitas_despesas__idCategoria_` | Remove uma categoria de receita e despesa pelo ID. |
| GET | `/categorias/receitas-despesas/{idCategoria}` | `get_categorias_receitas_despesas__idCategoria_` | Obtém uma categoria de receita e despesa pelo ID. |
| PUT | `/categorias/receitas-despesas/{idCategoria}` | `put_categorias_receitas_despesas__idCategoria_` | Atualiza uma categoria de receita e despesa a partir do ID. |

## Contas Financeiras

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/contas-contabeis` | `get_contas_contabeis` | Obtém contas financeiras paginadas. |
| GET | `/contas-contabeis/{idContaContabil}` | `get_contas_contabeis__idContaContabil_` | Obtém uma conta financeira pelo ID. |

## Contas a Pagar

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/contas/pagar` | `get_contas_pagar` | Obtém contas a pagar paginadas. |
| POST | `/contas/pagar` | `post_contas_pagar` | Cria uma conta a pagar. |
| DELETE | `/contas/pagar/{idContaPagar}` | `delete_contas_pagar__idContaPagar_` | Remove uma conta a pagar pelo ID. |
| GET | `/contas/pagar/{idContaPagar}` | `get_contas_pagar__idContaPagar_` | Obtém uma conta a pagar pelo ID. |
| PUT | `/contas/pagar/{idContaPagar}` | `put_contas_pagar__idContaPagar_` | Atualiza uma conta a pagar pelo ID. |
| POST | `/contas/pagar/{idContaPagar}/baixar` | `post_contas_pagar__idContaPagar__baixar` | Cria o recebimento de uma conta a pagar. |

## Contas a Receber

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/contas/receber` | `get_contas_receber` | Obtém contas a receber paginadas. |
| POST | `/contas/receber` | `post_contas_receber` | Cria uma conta a receber. |
| GET | `/contas/receber/boletos` | `get_contas_receber_boletos` | Obtém os boletos vinculados a um idOrigem, o qual corresponde ao ID de uma venda ou nota fiscal. |
| POST | `/contas/receber/boletos/cancelar` | `post_contas_receber_boletos_cancelar` | Cancela um ou todos os boletos em aberto vinculados a uma venda ou nota fiscal. |
| DELETE | `/contas/receber/{idContaReceber}` | `delete_contas_receber__idContaReceber_` | Remove uma conta a receber pelo ID. |
| GET | `/contas/receber/{idContaReceber}` | `get_contas_receber__idContaReceber_` | Obtém uma conta a receber pelo ID. |
| PUT | `/contas/receber/{idContaReceber}` | `put_contas_receber__idContaReceber_` | Altera uma conta a receber pelo ID. |
| POST | `/contas/receber/{idContaReceber}/baixar` | `post_contas_receber__idContaReceber__baixar` | Cria o recebimento de uma conta a receber. |

## Contatos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/contatos` | `delete_contatos` | Remove múltiplos contatos pelos IDs. |
| GET | `/contatos` | `get_contatos` | Obtém contatos paginados. |
| POST | `/contatos` | `post_contatos` | Cria um contato. |
| GET | `/contatos/consumidor-final` | `get_contatos_consumidor_final` | Obtém os dados do contato Consumidor Final. O consumidor final é um contato padrão do sistema que é criado automaticamen |
| POST | `/contatos/situacoes` | `post_contatos_situacoes` | Altera a situação de múltiplos contatos pelos IDs. |
| DELETE | `/contatos/{idContato}` | `delete_contatos__idContato_` | Remove um contato pelo ID. |
| GET | `/contatos/{idContato}` | `get_contatos__idContato_` | Obtém um contato pelo ID. |
| PUT | `/contatos/{idContato}` | `put_contatos__idContato_` | Altera um contato pelo ID. |
| PATCH | `/contatos/{idContato}/situacoes` | `patch_contatos__idContato__situacoes` | Altera a situação de um contato pelo ID. |
| GET | `/contatos/{idContato}/tipos` | `get_contatos__idContato__tipos` | Obtém os tipos de contato de um contato pelo ID. |

## Contatos - Tipos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/contatos/tipos` | `get_contatos_tipos` | Obtém tipos de contato pelo ID. |

## Contratos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/contratos` | `get_contratos` | Obtém contratos paginados. |
| POST | `/contratos` | `post_contratos` | Cria um contrato. |
| DELETE | `/contratos/{idContrato}` | `delete_contratos__idContrato_` | Remove um contrato pelo ID. |
| GET | `/contratos/{idContrato}` | `get_contratos__idContrato_` | Obtém um contrato pelo ID. |
| PUT | `/contratos/{idContrato}` | `put_contratos__idContrato_` | Altera um contrato pelo ID. |

## Depósitos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/depositos` | `get_depositos` | Obtém depósitos paginados. |
| POST | `/depositos` | `post_depositos` | Cria um depósito. Até 100 depósitos podem ser criados. |
| GET | `/depositos/{idDeposito}` | `get_depositos__idDeposito_` | Obtém um depósito pelo ID. |
| PUT | `/depositos/{idDeposito}` | `put_depositos__idDeposito_` | Altera um depósito pelo ID. |

## Documentos Compartilhados

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/documentos-compartilhados/{token}` | `get_documentos_compartilhados__token_` | Obtém um documento compartilhado pelo token. |

## Empresas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/empresas/me/dados-basicos` | `get_empresas_me_dados_basicos` | Obtém CNPJ, razão social e e-mail da empresa. |

## Estoques

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/estoques` | `post_estoques` | Cria um registro de estoque. |
| GET | `/estoques/saldos` | `get_estoques_saldos` | Obtém o saldo em estoque de produtos, em todos os depósitos. |
| GET | `/estoques/saldos/{idDeposito}` | `get_estoques_saldos__idDeposito_` | Obtém o saldo em estoque de produtos pelo ID do depósito. |
| PUT | `/estoques/{idEstoque}` | `put_estoques__idEstoque_` | Altera um registro de estoque pelo ID. |

## Formas de Pagamentos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/formas-pagamentos` | `get_formas_pagamentos` | Obtém formas de pagamentos paginadas. |
| POST | `/formas-pagamentos` | `post_formas_pagamentos` | Cria uma forma de pagamento. |
| DELETE | `/formas-pagamentos/{idFormaPagamento}` | `delete_formas_pagamentos__idFormaPagamento_` | Remove uma forma de pagamento pelo ID. |
| GET | `/formas-pagamentos/{idFormaPagamento}` | `get_formas_pagamentos__idFormaPagamento_` | Obtém uma forma de pagamento pelo ID. |
| PUT | `/formas-pagamentos/{idFormaPagamento}` | `put_formas_pagamentos__idFormaPagamento_` | Altera uma forma de pagamento pelo ID. |
| PATCH | `/formas-pagamentos/{idFormaPagamento}/padrao` | `patch_formas_pagamentos__idFormaPagamento__padrao` | Altera o padrão de uma forma de pagamento pelo ID. |
| PATCH | `/formas-pagamentos/{idFormaPagamento}/situacao` | `patch_formas_pagamentos__idFormaPagamento__situacao` | Altera a situação de uma forma de pagamento pelo ID. |

## Grupos de Produtos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/grupos-produtos` | `delete_grupos_produtos` | Remove múltiplos grupos de produtos pelos IDs. |
| GET | `/grupos-produtos` | `get_grupos_produtos` | Obtém grupos de produtos paginados. |
| POST | `/grupos-produtos` | `post_grupos_produtos` | Cria um grupo de produtos. |
| DELETE | `/grupos-produtos/{idGrupoProduto}` | `delete_grupos_produtos__idGrupoProduto_` | Remove um grupo de produtos pelo ID. |
| GET | `/grupos-produtos/{idGrupoProduto}` | `get_grupos_produtos__idGrupoProduto_` | Obtém um grupo de produtos pelo ID. |
| PUT | `/grupos-produtos/{idGrupoProduto}` | `put_grupos_produtos__idGrupoProduto_` | Altera um grupo de produtos pelo ID. |

## Homologação

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/homologacao/produtos` | `get_homologacao_produtos` | Obtém o produto que será utilizado durante os demais passos da homologação, e, inicia o processo de validação, o qual de |
| POST | `/homologacao/produtos` | `post_homologacao_produtos` | Cria o produto da homologação. |
| DELETE | `/homologacao/produtos/{idProdutoHomologacao}` | `delete_homologacao_produtos__idProdutoHomologacao_` | Remove o produto da homologação pelo ID. |
| PUT | `/homologacao/produtos/{idProdutoHomologacao}` | `put_homologacao_produtos__idProdutoHomologacao_` | Altera o produto da homologação pelo ID. |
| PATCH | `/homologacao/produtos/{idProdutoHomologacao}/situacoes` | `patch_homologacao_produtos__idProdutoHomologacao__situacoes` | Altera a situação do produto da homologação pelo ID. |

## Listas de Preços

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/listas-precos` | `get_listas_precos` | Obtém listas de preços paginadas. O fator customizado (preço negociado, listas do tipo Customizada) não é exposto por es |
| GET | `/listas-precos/{idListaPreco}` | `get_listas_precos__idListaPreco_` | Obtém uma lista de preço pelo ID. O fator customizado (preço negociado, listas do tipo Customizada) não é exposto por es |

## Logísticas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/logisticas` | `get_logisticas` | Obtém logísticas paginados. |
| POST | `/logisticas` | `post_logisticas` | Cria uma logística. |
| DELETE | `/logisticas/{idLogistica}` | `delete_logisticas__idLogistica_` | Remove uma logística pelo ID. |
| GET | `/logisticas/{idLogistica}` | `get_logisticas__idLogistica_` | Obtém uma logística pelo ID. |
| PUT | `/logisticas/{idLogistica}` | `put_logisticas__idLogistica_` | Altera uma logística pelo ID. |

## Logísticas - Etiquetas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/logisticas/etiquetas` | `get_logisticas_etiquetas` | Obtém as etiquetas dos pedidos de venda a partir dos ID's dos pedidos. No momento, o filtro está limitado para apenas um |

## Logísticas - Objetos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/logisticas/objetos` | `post_logisticas_objetos` | Cria um objeto de logística personalizada. |
| DELETE | `/logisticas/objetos/{idObjeto}` | `delete_logisticas_objetos__idObjeto_` | Remove um objeto de logística personalizada que não esteja em uma PLP. |
| GET | `/logisticas/objetos/{idObjeto}` | `get_logisticas_objetos__idObjeto_` | Obtém um objeto de logística pelo ID. |
| PUT | `/logisticas/objetos/{idObjeto}` | `put_logisticas_objetos__idObjeto_` | Altera dados de um objeto de logística personalizada pelo ID. |

## Logísticas - Remessas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/logisticas/remessas` | `post_logisticas_remessas` | Cria uma remessa de postagem de uma logística. |
| DELETE | `/logisticas/remessas/{idRemessa}` | `delete_logisticas_remessas__idRemessa_` | Remove uma remessa de postagem pelo ID. |
| GET | `/logisticas/remessas/{idRemessa}` | `get_logisticas_remessas__idRemessa_` | Obtém uma remessa de postagem pelo ID. |
| PUT | `/logisticas/remessas/{idRemessa}` | `put_logisticas_remessas__idRemessa_` | Altera uma remessa de postagem pelo ID. |
| GET | `/logisticas/{idLogistica}/remessas` | `get_logisticas__idLogistica__remessas` | Obtém as remessas de postagem de uma logística pelo ID. |

## Logísticas - Serviços

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/logisticas/servicos` | `get_logisticas_servicos` | Obtém serviços de logísticas paginados. |
| POST | `/logisticas/servicos` | `post_logisticas_servicos` | Cria um serviço de logística personalizada. |
| GET | `/logisticas/servicos/{idLogisticaServico}` | `get_logisticas_servicos__idLogisticaServico_` | Obtém um servico de logística pelo ID. |
| PUT | `/logisticas/servicos/{idLogisticaServico}` | `put_logisticas_servicos__idLogisticaServico_` | Altera dados de um serviço de logística personalizada pelo ID. |
| PATCH | `/logisticas/{idLogisticaServico}/situacoes` | `patch_logisticas__idLogisticaServico__situacoes` | Desativa ou ativa um serviço de uma logística personalizada pelo ID. |

## Naturezas de Operações

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/naturezas-operacoes` | `get_naturezas_operacoes` | Obtém naturezas de operação paginadas. |
| POST | `/naturezas-operacoes/{idNaturezaOperacao}/obter-tributacao` | `post_naturezas_operacoes__idNaturezaOperacao__obter_tributacao` | Obtém regras de tributação que incidem sobre o item, dada uma natureza de operação. |

## Notas Fiscais Eletrônicas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/nfe` | `delete_nfe` | Remove múltiplas notas fiscais por IDs. |
| GET | `/nfe` | `get_nfe` | Obtém notas fiscais paginadas. |
| POST | `/nfe` | `post_nfe` | Cria uma nota fiscal. |
| GET | `/nfe/documento/{chaveAcesso}` | `get_nfe_documento__chaveAcesso_` | Obtém o PDF ou XML de uma nota fiscal pela chave de acesso. O formato desejado deve ser informado via query param. |
| GET | `/nfe/{idNotaFiscal}` | `get_nfe__idNotaFiscal_` | Obtém uma nota fiscal pelo ID. |
| PUT | `/nfe/{idNotaFiscal}` | `put_nfe__idNotaFiscal_` | Altera uma nota fiscal pelo ID. Notas com vínculos possuem restrições de atualização. Notas autorizadas não podem ter da |
| POST | `/nfe/{idNotaFiscal}/enviar` | `post_nfe__idNotaFiscal__enviar` | Envia uma nota fiscal pelo ID para emissão na Sefaz. |
| POST | `/nfe/{idNotaFiscal}/estornar-contas` | `post_nfe__idNotaFiscal__estornar_contas` | Estorna as contas de uma nota fiscal pelo ID. |
| POST | `/nfe/{idNotaFiscal}/estornar-estoque` | `post_nfe__idNotaFiscal__estornar_estoque` | Estorna o estoque de uma nota fiscal pelo ID. |
| POST | `/nfe/{idNotaFiscal}/lancar-contas` | `post_nfe__idNotaFiscal__lancar_contas` | Lança as contas de uma nota fiscal pelo ID. |
| POST | `/nfe/{idNotaFiscal}/lancar-estoque` | `post_nfe__idNotaFiscal__lancar_estoque` | Lança o estoque de uma nota fiscal pelo ID, no depósito padrão. |
| POST | `/nfe/{idNotaFiscal}/lancar-estoque/{idDeposito}` | `post_nfe__idNotaFiscal__lancar_estoque__idDeposito_` | Lança o estoque de uma nota fiscal pelo ID, especificando o ID do depósito. |

## Notas Fiscais de Consumidor Eletrônicas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/nfce` | `get_nfce` | Obtém notas fiscais de consumidor paginadas. |
| POST | `/nfce` | `post_nfce` | Cria uma nota fiscal de consumidor. |
| GET | `/nfce/{idNotaFiscalConsumidor}` | `get_nfce__idNotaFiscalConsumidor_` | Obtém uma nota fiscal de consumidor pelo ID. |
| PUT | `/nfce/{idNotaFiscalConsumidor}` | `put_nfce__idNotaFiscalConsumidor_` | Altera uma nota fiscal de consumidor. |
| POST | `/nfce/{idNotaFiscalConsumidor}/enviar` | `post_nfce__idNotaFiscalConsumidor__enviar` | Envia uma nota de consumidor pelo ID para emissão na Sefaz. |
| POST | `/nfce/{idNotaFiscalConsumidor}/estornar-contas` | `post_nfce__idNotaFiscalConsumidor__estornar_contas` | Estorna as contas de uma nota fiscal pelo ID. |
| POST | `/nfce/{idNotaFiscalConsumidor}/estornar-estoque` | `post_nfce__idNotaFiscalConsumidor__estornar_estoque` | Estorna o estoque de uma nota fiscal pelo ID. |
| POST | `/nfce/{idNotaFiscalConsumidor}/lancar-contas` | `post_nfce__idNotaFiscalConsumidor__lancar_contas` | Lança as contas de uma nota fiscal pelo ID. |
| POST | `/nfce/{idNotaFiscalConsumidor}/lancar-estoque` | `post_nfce__idNotaFiscalConsumidor__lancar_estoque` | Lança o estoque de uma nota fiscal pelo ID, no depósito padrão. |
| POST | `/nfce/{idNotaFiscalConsumidor}/lancar-estoque/{idDeposito}` | `post_nfce__idNotaFiscalConsumidor__lancar_estoque__idDeposito_` | Lança o estoque de uma nota fiscal pelo ID, especificando o ID do depósito. |

## Notas Fiscais de Serviço Eletrônicas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/nfse` | `get_nfse` | Obtém notas de serviços paginadas. |
| POST | `/nfse` | `post_nfse` | Cria uma nota de serviço. |
| GET | `/nfse/configuracoes` | `get_nfse_configuracoes` | Obtém todas as configurações de nota de serviço. |
| PUT | `/nfse/configuracoes` | `put_nfse_configuracoes` | Cria e altera configurações para emissão de notas de serviço. |
| DELETE | `/nfse/{idNotaServico}` | `delete_nfse__idNotaServico_` | Exclui uma nota de serviço pelo ID. |
| GET | `/nfse/{idNotaServico}` | `get_nfse__idNotaServico_` | Obtém uma nota de serviço pelo ID. |
| POST | `/nfse/{idNotaServico}/cancelar` | `post_nfse__idNotaServico__cancelar` | Cancela uma nota de serviço pelo ID. |
| POST | `/nfse/{idNotaServico}/enviar` | `post_nfse__idNotaServico__enviar` | Envia uma nota de serviço pelo ID. |

## Notificações

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/notificacoes` | `get_notificacoes` | Obtém todas as notificações de uma empresa no período informado. Caso período não seja informado, será considerado o ano |
| GET | `/notificacoes/quantidade` | `get_notificacoes_quantidade` | Obtém a quantidade de notificações de uma empresa no período informado. Caso período não seja informado, será considerad |
| POST | `/notificacoes/{idNotificacao}/confirmar-leitura` | `post_notificacoes__idNotificacao__confirmar_leitura` | Marca a notificação relacionada à empresa como lida. |

## Ordens de Produção

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/ordens-producao` | `get_ordens_producao` | Obtém ordens de produção paginadas. |
| POST | `/ordens-producao` | `post_ordens_producao` | Cria uma ordem de produção. |
| POST | `/ordens-producao/gerar-sob-demanda` | `post_ordens_producao_gerar_sob_demanda` | Gera ordens de produção sob demanda (abaixo do estoque mínimo). |
| DELETE | `/ordens-producao/{idOrdemProducao}` | `delete_ordens_producao__idOrdemProducao_` | Remove uma ordem de produção pelo ID. |
| GET | `/ordens-producao/{idOrdemProducao}` | `get_ordens_producao__idOrdemProducao_` | Obtém uma ordem de produção pelo ID. |
| PUT | `/ordens-producao/{idOrdemProducao}` | `put_ordens_producao__idOrdemProducao_` | Altera uma ordem de produção pelo ID. |
| PUT | `/ordens-producao/{idOrdemProducao}/situacoes` | `put_ordens_producao__idOrdemProducao__situacoes` | Altera a situação de uma ordem de produção pelo ID. |

## Ordens de Serviço

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/ordens/servico` | `get_ordens_servico` | Obtém ordens de serviço paginadas. |
| POST | `/ordens/servico` | `post_ordens_servico` | Cria uma ordem de serviço. |
| DELETE | `/ordens/servico/{idOrdemServico}` | `delete_ordens_servico__idOrdemServico_` | Remove uma ordem de serviço pelo ID. |
| GET | `/ordens/servico/{idOrdemServico}` | `get_ordens_servico__idOrdemServico_` | Obtém uma ordem de serviço pelo ID. |
| PUT | `/ordens/servico/{idOrdemServico}` | `put_ordens_servico__idOrdemServico_` | Altera uma ordem de serviço pelo ID. Os campos não informados são gravados com o valor padrão, portanto envie o recurso  |
| PATCH | `/ordens/servico/{idOrdemServico}/situacoes/{idSituacao}` | `patch_ordens_servico__idOrdemServico__situacoes__idSituacao_` | Altera a situação de uma ordem de serviço pelo ID. |

## Pedidos - Compras

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/pedidos/compras` | `get_pedidos_compras` | Obtém pedidos de compras paginados. |
| POST | `/pedidos/compras` | `post_pedidos_compras` | Cria um pedido de compra. |
| DELETE | `/pedidos/compras/{idPedidoCompra}` | `delete_pedidos_compras__idPedidoCompra_` | Remove um pedido de compra pelo ID. |
| GET | `/pedidos/compras/{idPedidoCompra}` | `get_pedidos_compras__idPedidoCompra_` | Obtém um pedido de compra pelo ID. |
| PUT | `/pedidos/compras/{idPedidoCompra}` | `put_pedidos_compras__idPedidoCompra_` | Altera um pedido de compra pelo ID. |
| POST | `/pedidos/compras/{idPedidoCompra}/estornar-contas` | `post_pedidos_compras__idPedidoCompra__estornar_contas` | Estorna as contas de um pedido de compra pelo ID. |
| POST | `/pedidos/compras/{idPedidoCompra}/estornar-estoque` | `post_pedidos_compras__idPedidoCompra__estornar_estoque` | Estorna o estoque de um pedido de compra pelo ID. |
| POST | `/pedidos/compras/{idPedidoCompra}/lancar-contas` | `post_pedidos_compras__idPedidoCompra__lancar_contas` | Lança as contas de um pedido de compra pelo ID. |
| POST | `/pedidos/compras/{idPedidoCompra}/lancar-estoque` | `post_pedidos_compras__idPedidoCompra__lancar_estoque` | Lança o estoque de um pedido de compra pelo ID. |
| PATCH | `/pedidos/compras/{idPedidoCompra}/situacoes/{idSituacao}` | `patch_pedidos_compras__idPedidoCompra__situacoes__idSituacao_` | Altera a situação de um pedido de compra pelo ID. |

## Pedidos - Vendas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/pedidos/vendas` | `delete_pedidos_vendas` | Remove pedidos de vendas pelos IDs. |
| GET | `/pedidos/vendas` | `get_pedidos_vendas` | Obtém pedidos de vendas paginados. |
| POST | `/pedidos/vendas` | `post_pedidos_vendas` | Cria um pedido de venda. |
| DELETE | `/pedidos/vendas/{idPedidoVenda}` | `delete_pedidos_vendas__idPedidoVenda_` | Remove um pedido de venda pelo ID. |
| GET | `/pedidos/vendas/{idPedidoVenda}` | `get_pedidos_vendas__idPedidoVenda_` | Obtém um pedido de venda pelo ID. |
| PUT | `/pedidos/vendas/{idPedidoVenda}` | `put_pedidos_vendas__idPedidoVenda_` | Altera um pedido de venda pelo ID. |
| POST | `/pedidos/vendas/{idPedidoVenda}/estornar-contas` | `post_pedidos_vendas__idPedidoVenda__estornar_contas` | Estorna as contas de um pedido de venda pelo ID. |
| POST | `/pedidos/vendas/{idPedidoVenda}/estornar-estoque` | `post_pedidos_vendas__idPedidoVenda__estornar_estoque` | Estorna o estoque de um pedido de venda pelo ID. |
| POST | `/pedidos/vendas/{idPedidoVenda}/gerar-nfce` | `post_pedidos_vendas__idPedidoVenda__gerar_nfce` | Gera nota fiscal de consumidor eletrônica a partir do pedido de venda pelo ID. |
| POST | `/pedidos/vendas/{idPedidoVenda}/gerar-nfe` | `post_pedidos_vendas__idPedidoVenda__gerar_nfe` | Gera nota fiscal eletrônica a partir do pedido de venda pelo ID. |
| POST | `/pedidos/vendas/{idPedidoVenda}/lancar-contas` | `post_pedidos_vendas__idPedidoVenda__lancar_contas` | Lança as contas de um pedido de venda pelo ID. |
| POST | `/pedidos/vendas/{idPedidoVenda}/lancar-estoque` | `post_pedidos_vendas__idPedidoVenda__lancar_estoque` | Lança o estoque de um pedido de venda pelo ID, no depósito padrão. |
| POST | `/pedidos/vendas/{idPedidoVenda}/lancar-estoque/{idDeposito}` | `post_pedidos_vendas__idPedidoVenda__lancar_estoque__idDeposito_` | Lança o estoque de um pedido de venda pelo ID, especificando o ID do depósito. |
| PATCH | `/pedidos/vendas/{idPedidoVenda}/situacoes/{idSituacao}` | `patch_pedidos_vendas__idPedidoVenda__situacoes__idSituacao_` | Altera a situação de um pedido de venda pelo ID. |

## Produtos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/produtos` | `delete_produtos` | Remove múltiplos produtos pelos IDs. |
| GET | `/produtos` | `get_produtos` | Obtém produtos paginados. |
| POST | `/produtos` | `post_produtos` | Cria um produto. |
| POST | `/produtos/situacoes` | `post_produtos_situacoes` | Altera a situação de múltiplos produtos pelos IDs. |
| DELETE | `/produtos/{idProduto}` | `delete_produtos__idProduto_` | Remove um produto pelo ID. |
| GET | `/produtos/{idProduto}` | `get_produtos__idProduto_` | Obtém um produto pelo ID. |
| PATCH | `/produtos/{idProduto}` | `patch_produtos__idProduto_` | Altera parcialmente um produto pelo ID. Somente os campos informados terão o valor alterado. |
| PUT | `/produtos/{idProduto}` | `put_produtos__idProduto_` | Altera um produto pelo ID. |
| PATCH | `/produtos/{idProduto}/situacoes` | `patch_produtos__idProduto__situacoes` | Altera a situação de um produto pelo ID. |

## Produtos - Estruturas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/produtos/estruturas` | `delete_produtos_estruturas` | Remove a estrutura de múltiplos produtos com composição pelos IDs. |
| GET | `/produtos/estruturas/{idProdutoEstrutura}` | `get_produtos_estruturas__idProdutoEstrutura_` | Obtém a estrutura de um produto com composição pelo ID. |
| PUT | `/produtos/estruturas/{idProdutoEstrutura}` | `put_produtos_estruturas__idProdutoEstrutura_` | Altera a estrutura de um produto com composição pelo ID. |
| DELETE | `/produtos/estruturas/{idProdutoEstrutura}/componentes` | `delete_produtos_estruturas__idProdutoEstrutura__componentes` | Remove os componentes de um produto com composição pelos IDs dos componentes. |
| POST | `/produtos/estruturas/{idProdutoEstrutura}/componentes` | `post_produtos_estruturas__idProdutoEstrutura__componentes` | Adiciona múltiplos componentes a uma estrutura pelo ID. |
| PATCH | `/produtos/estruturas/{idProdutoEstrutura}/componentes/{idComponente}` | `patch_produtos_estruturas__idProdutoEstrutura__componentes__idComponente_` | Altera um componente de uma estrutura pelo ID. |

## Produtos - Fornecedores

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/produtos/fornecedores` | `get_produtos_fornecedores` | Obtém produtos fornecedores paginados. |
| POST | `/produtos/fornecedores` | `post_produtos_fornecedores` | Cria um produto fornecedor. |
| DELETE | `/produtos/fornecedores/{idProdutoFornecedor}` | `delete_produtos_fornecedores__idProdutoFornecedor_` | Remove um produto fornecedor pelo ID. |
| GET | `/produtos/fornecedores/{idProdutoFornecedor}` | `get_produtos_fornecedores__idProdutoFornecedor_` | Obtém um produto fornecedor pelo ID. |
| PUT | `/produtos/fornecedores/{idProdutoFornecedor}` | `put_produtos_fornecedores__idProdutoFornecedor_` | Altera um produto fornecedor pelo ID. |

## Produtos - Lojas

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/produtos/lojas` | `get_produtos_lojas` | Obtém vínculos de produtos com lojas paginados. |
| POST | `/produtos/lojas` | `post_produtos_lojas` | Cria o vínculo de um produto com uma loja. |
| DELETE | `/produtos/lojas/{idProdutoLoja}` | `delete_produtos_lojas__idProdutoLoja_` | Remove o vínculo de um produto com uma loja pelo ID. |
| GET | `/produtos/lojas/{idProdutoLoja}` | `get_produtos_lojas__idProdutoLoja_` | Obtém um vínculo de produto com loja pelo ID. |
| PUT | `/produtos/lojas/{idProdutoLoja}` | `put_produtos_lojas__idProdutoLoja_` | Altera o vínculo de um produto com uma loja pelo ID. |

## Produtos - Lotes

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/produtos/lotes` | `delete_produtos_lotes` | Remove lotes de produtos pelos IDs. |
| GET | `/produtos/lotes` | `get_produtos_lotes` | Obtém lotes de produtos paginados. |
| PUT | `/produtos/lotes` | `put_produtos_lotes` | Cria/altera lotes de produtos. |
| GET | `/produtos/lotes/controla-lote` | `get_produtos_lotes_controla_lote` | Obtém a informação se determinados produtos possuem controle de lote. |
| GET | `/produtos/lotes/{idLote}` | `get_produtos_lotes__idLote_` | Obtém um lote de um produto pelo ID. |
| PUT | `/produtos/lotes/{idLote}` | `put_produtos_lotes__idLote_` | Altera um lote de um produto pelo ID. |
| PATCH | `/produtos/lotes/{idLote}/status` | `patch_produtos_lotes__idLote__status` | Altera o status de um lote do produto pelo ID. |
| POST | `/produtos/{idProduto}/lotes/controla-lote/desativar` | `post_produtos__idProduto__lotes_controla_lote_desativar` | Desativa controle de lotes para o produto pelo ID do produto. |

## Produtos - Lotes Lançamentos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/produtos/lotes/lancamentos/{idLancamento}` | `get_produtos_lotes_lancamentos__idLancamento_` | Obtém um lançamento de um lote de produto pelo ID do lançamento. |
| PATCH | `/produtos/lotes/lancamentos/{idLancamento}` | `patch_produtos_lotes_lancamentos__idLancamento_` | Altera a observação de um lançamento de um lote de um produto pelo ID do lançamento. |
| GET | `/produtos/lotes/{idLote}/lancamentos` | `get_produtos_lotes__idLote__lancamentos` | Obtém os lançamentos de um lote de produto pelo ID. |
| POST | `/produtos/lotes/{idLote}/lancamentos` | `post_produtos_lotes__idLote__lancamentos` | Inclui lançamento de um lote. |
| GET | `/produtos/{idProduto}/lotes/depositos/{idDeposito}/saldo` | `get_produtos__idProduto__lotes_depositos__idDeposito__saldo` | Obtém os saldos dos lotes de um produto por depósito. |
| GET | `/produtos/{idProduto}/lotes/depositos/{idDeposito}/saldo/soma` | `get_produtos__idProduto__lotes_depositos__idDeposito__saldo_soma` | Obtém a soma dos saldos dos lotes de um produto em um depósito. |
| GET | `/produtos/{idProduto}/lotes/saldo/soma` | `get_produtos__idProduto__lotes_saldo_soma` | Obtém o saldo total dos lotes de um produto pelo ID do produto. |
| GET | `/produtos/{idProduto}/lotes/{idLote}/depositos/{idDeposito}/saldo` | `get_produtos__idProduto__lotes__idLote__depositos__idDeposito__saldo` | Obtém o saldo de um lote de produto. |

## Produtos - Variações

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/produtos/variacoes/atributos/gerar-combinacoes` | `post_produtos_variacoes_atributos_gerar_combinacoes` | Ação responsável por retornar o produto pai com combinação de novas variações a partir dos atributos. Esta ação não pers |
| GET | `/produtos/variacoes/{idProdutoPai}` | `get_produtos_variacoes__idProdutoPai_` | Obtém o produto e variações pelo ID do produto pai. |
| PATCH | `/produtos/variacoes/{idProdutoPai}/atributos` | `patch_produtos_variacoes__idProdutoPai__atributos` | Altera o nome do atributo nas variações de um produto pai. |

## Propostas Comerciais

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| DELETE | `/propostas-comerciais` | `delete_propostas_comerciais` | Remove múltiplas propostas comerciais pelos IDs. |
| GET | `/propostas-comerciais` | `get_propostas_comerciais` | Obtém propostas comerciais paginadas. |
| POST | `/propostas-comerciais` | `post_propostas_comerciais` | Cria uma proposta comercial. |
| DELETE | `/propostas-comerciais/{idPropostaComercial}` | `delete_propostas_comerciais__idPropostaComercial_` | Remove uma proposta comercial pelo ID. |
| GET | `/propostas-comerciais/{idPropostaComercial}` | `get_propostas_comerciais__idPropostaComercial_` | Obtém uma proposta comercial pelo ID. |
| PUT | `/propostas-comerciais/{idPropostaComercial}` | `put_propostas_comerciais__idPropostaComercial_` | Altera uma proposta comercial pelo ID. |
| PATCH | `/propostas-comerciais/{idPropostaComercial}/situacoes` | `patch_propostas_comerciais__idPropostaComercial__situacoes` | Altera a situação de uma proposta comercial pelo ID. |

## Situações

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/situacoes` | `post_situacoes` | Cria uma situação. |
| DELETE | `/situacoes/{idSituacao}` | `delete_situacoes__idSituacao_` | Remove uma situação pelo ID. |
| GET | `/situacoes/{idSituacao}` | `get_situacoes__idSituacao_` | Obtém uma situação pelo ID. |
| PUT | `/situacoes/{idSituacao}` | `put_situacoes__idSituacao_` | Altera uma situação pelo ID. |

## Situações - Módulos

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/situacoes/modulos` | `get_situacoes_modulos` | Obtém módulos. |
| GET | `/situacoes/modulos/{idModuloSistema}` | `get_situacoes_modulos__idModuloSistema_` | Obtém situações de um módulo pelo ID. |
| GET | `/situacoes/modulos/{idModuloSistema}/acoes` | `get_situacoes_modulos__idModuloSistema__acoes` | Obtém as ações de um módulo pelo ID. |
| GET | `/situacoes/modulos/{idModuloSistema}/transicoes` | `get_situacoes_modulos__idModuloSistema__transicoes` | Obtém as transições de um módulo pelo ID. |

## Situações - Transições

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/situacoes/transicoes` | `post_situacoes_transicoes` | Cria uma transição. |
| DELETE | `/situacoes/transicoes/{idTransicao}` | `delete_situacoes_transicoes__idTransicao_` | Remove uma transição pelo ID. |
| GET | `/situacoes/transicoes/{idTransicao}` | `get_situacoes_transicoes__idTransicao_` | Obtém uma transição pelo ID. |
| PUT | `/situacoes/transicoes/{idTransicao}` | `put_situacoes_transicoes__idTransicao_` | Altera uma transição pelo ID. |

## Usuários

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| POST | `/usuarios/recuperar-senha` | `post_usuarios_recuperar_senha` | Envia solicitação de recuperação de senha por e-mail. |
| PATCH | `/usuarios/redefinir-senha` | `patch_usuarios_redefinir_senha` | Redefine senha do usuário utilizando token enviado por e-mail. |
| GET | `/usuarios/verificar-hash` | `get_usuarios_verificar_hash` | Valida o hash recebido por e-mail. |

## Vendedores

| Verbo | Path | operationId | Descrição |
|---|---|---|---|
| GET | `/vendedores` | `get_vendedores` | Obtém vendedores paginados. |
| GET | `/vendedores/{idVendedor}` | `get_vendedores__idVendedor_` | Obtém um vendedor pelo ID. |
