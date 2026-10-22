# Instruções de impressão e uso

Cada haste se encaixa num scanbody de minipilar cônico e dá a ele uma forma única, para o scanner não confundir implantes vizinhos. É uma alternativa de baixo custo aos scanbodies horizontais comerciais, e o script adapta o encaixe a outros scanbodies mudando uma medida. **Meça o seu scanbody antes de imprimir.**

## Arquivos do conjunto

| Arquivo | Haste | Largura | Símbolos no topo |
| --- | --- | --- | --- |
| `haste_A_triangulos_12mm_L3.0_fenda0.6.stl` | 12 mm | 3,0 mm | 3 triângulos |
| `haste_B_quadrados_15mm_L3.5_fenda0.6.stl` | 15 mm | 3,5 mm | 3 quadrados |
| `haste_C_cilindros_18mm_L4.0_fenda0.6.stl` | 18 mm | 4,0 mm | 3 cilindros |
| `haste_D_misto_21mm_L4.5_fenda0.6.stl` | 21 mm | 4,5 mm | cilindro, triângulo, quadrado |
| `src/haste_scanbody.py` | — | — | Gerador paramétrico (Python 3, sem bibliotecas extras) |

Todas têm anel de 4 mm de altura com fenda de 0,6 mm oposta à haste, e chanfro de 0,5 mm num dos lados da haste. Use uma haste diferente em cada implante da arcada. Encaixado na base do scanbody, o anel afasta os tecidos moles ao redor dele e deixa o chanfro do scanbody livre e visível para o scanner.

## Antes de imprimir: medir e ajustar

1. Meça o diâmetro externo do cilindro do scanbody com paquímetro ou micrômetro, em 3 pontos. Anote a média.
2. Abra `src/haste_scanbody.py` e troque `D_SCANBODY = 4.80` pela sua medida.
3. Se quiser, ajuste no topo do arquivo:
    - `FOLGA` (0,05 mm): menor = encaixe mais justo.
    - `FENDA` (0,6 mm): `0` gera anel fechado.
    - `VARIANTES`: comprimento, largura, símbolos e vãos de cada haste.
4. Rode `python3 src/haste_scanbody.py stl`. Os STL são gerados na pasta `stl/`, e o script avisa se algum vão ficou menor que 0,8 mm.

## Impressão

| Item | Recomendação |
| --- | --- |
| Tecnologia | Resina (SLA, DLP ou LCD); FDM não tem resolução para os símbolos e a fenda |
| Resina | Uso intraoral: biocompatível (guia cirúrgico ou modelo biocompatível). Teste em bancada: resina de modelo comum |
| Cor | Opaca e clara (branco, bege ou cinza claro); evite transparente e brilhante, que o scanner capta mal |
| Camada | 50 µm |
| Orientação | Anel em pé, base apoiada na plataforma, haste horizontal |
| Suportes | Só sob a haste, finos, longe dos símbolos e da fenda |
| Lavagem | Álcool isopropílico, conforme o fabricante; limpe bem dentro do anel e da fenda |
| Pós-cura | Tempo e temperatura do fabricante da resina |

Depois da cura, retire os suportes com cuidado e confira se a fenda está aberta de ponta a ponta. Imprima primeiro uma haste para testar o encaixe.

## Uso

1. **Desinfete** as hastes antes do uso, com método compatível com a resina (em geral, desinfecção química; não autoclavar sem confirmar com o fabricante).
2. **Instale os scanbodies** nos minipilares com o torque indicado pelo fabricante.
3. **Encaixe as hastes** descendo o anel pelo topo do scanbody até a base, com a fenda para o lado oposto ao da haste. Use uma haste diferente em cada implante. O anel afasta os tecidos moles ao redor do scanbody; confira se o chanfro do scanbody ficou totalmente visível acima do anel.
4. **Direcione as hastes** para o implante vizinho, sem tocar no scanbody ao lado nem no tecido. A ponta de cada haste deve ficar a 1–3 mm da haste seguinte; se não alcançar, ajuste o comprimento em `VARIANTES`.
5. **Una as hastes com resina** para que nenhuma mude de posição durante o escaneamento:
    - Use resina de baixa contração: acrílica autopolimerizável pela técnica do pincel ou resina fotopolimerizável.
    - Aplique em pequenos incrementos na ponta de cada haste, ligando-a à haste vizinha; polimerize cada incremento antes do próximo.
    - Não cubra os símbolos nem o chanfro, e mantenha a união afastada da mucosa.
    - Espere a polimerização completa antes de escanear.
6. **Confira a estabilidade:** nenhuma haste pode girar nem inclinar. Se algo mexer, refaça a união antes de escanear.
7. **Escaneie** seguindo a estratégia do fabricante do scanner, passando pelas hastes em sequência contínua de uma extremidade à outra da arcada.
8. **Remova o conjunto.** Com implantes paralelos, as hastes unidas saem juntas por cima dos scanbodies. Com implantes divergentes, desparafuse os scanbodies e retire tudo em bloco (scanbodies, hastes e união), sem cortar nada. Fora da boca, solte cada scanbody do seu anel pela fenda. Se preferir, a união também pode ser cortada com disco.
9. **Escaneie sem as hastes**, se o fluxo do seu software pedir o scanbody isolado para o alinhamento de biblioteca.
10. **Descarte** as hastes e a união após o uso clínico; são de uso único.

## Limitação: não serve como index

O conjunto de hastes unidas não substitui um index nem uma guia de verificação (verification jig). Os anéis ficam presos por atrito ao scanbody, não parafusados ao minipilar, e a fenda e a folga permitem pequenos movimentos. A resina impressa e a resina de união também se contraem. Por isso ele não transfere a posição dos implantes para um modelo físico nem comprova a passividade de uma prótese. Para isso, use um index parafusado sobre cilindros de titânio ou uma prova de estrutura.

## Problemas comuns e ajustes

| Problema | Ajuste no script |
| --- | --- |
| Anel não entra ou trinca ao encaixar | Aumentar `FOLGA` para 0,08–0,10 ou `FENDA` para 0,8 |
| Haste solta ou gira | Reduzir `FOLGA` para 0,00; conferir se a medida do scanbody está correta |
| Fenda fechada após a impressão | Aumentar `FENDA`; revisar exposição da resina (superexposição fecha frestas) |
| Haste encosta no scanbody vizinho | Diminuir o comprimento dessa haste em `VARIANTES` ou girar o anel para outra direção |
| Símbolos pouco definidos na malha | Aumentar `MARC_ALT` ou a largura da haste; usar resina opaca e fosca |
| Haste quebra na remoção | Aumentar `ALT_HASTE` ou a largura; usar resina mais tenaz |
| Anel cobre o chanfro do scanbody | Reduzir `ALTURA_ANEL` (padrão 4,0 mm) até o chanfro ficar livre |

## Licença e aviso de uso

- **Código:** licença MIT.
- **Modelos STL e esta documentação:** CC BY 4.0. Pode usar, modificar e redistribuir citando a fonte.

Este é um acessório experimental, não um dispositivo médico registrado. Quem o imprime e usa é responsável pela escolha da resina, pela desinfecção e por validar a precisão no próprio fluxo. Neodent e Grand Morse são marcas de seus titulares; este projeto não tem vínculo com o fabricante.
