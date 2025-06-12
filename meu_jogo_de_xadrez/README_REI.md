# Implementação do Rei - Lógica de Cheque e Cheque Mate

## Funcionalidades Implementadas

### 1. Classe Rei (`movimento_rei.py`)
- **Movimentos básicos**: O rei pode mover uma casa em qualquer direção (horizontal, vertical ou diagonal)
- **Validação de movimentos**: Não pode mover para casas ocupadas por peças próprias
- **Interface consistente**: Mesma estrutura da classe Peao para fácil integração

### 2. Sistema de Detecção de Cheque (`regras.py`)
- **`rei_em_cheque()`**: Verifica se um rei está sendo atacado
- **`casa_atacada_por()`**: Verifica se uma casa está sob ataque
- **Suporte para ataques de peões e reis** (extensível para outras peças)

### 3. Sistema de Validação de Movimentos
- **`movimento_deixa_rei_em_cheque()`**: Simula movimentos para verificar se deixam o rei em cheque
- **`obter_movimentos_validos()`**: Filtra movimentos que não colocam o próprio rei em perigo
- **Validação em tempo real**: Só permite movimentos que não violam as regras de cheque

### 4. Detecção de Fim de Jogo
- **`cheque_mate()`**: Verifica se há cheque mate
- **`empate_por_afogamento()`**: Verifica empate quando não há movimentos válidos mas o rei não está em cheque

### 5. Integração com Tabuleiro
- **Método `calcular_casas_destacadas()` atualizado**: Detecta automaticamente o tipo de peça
- **Suporte para rei e peão**: Calcula movimentos válidos respeitando as regras de cheque

## Como Usar

### Executar o Exemplo Completo
```bash
python exemplo_com_rei.py
```

### Integrar no Seu Código Principal

1. **Importe as classes necessárias**:
```python
from jogo.movimento_rei import Rei
from jogo.regras import rei_em_cheque, cheque_mate, empate_por_afogamento
```

2. **Crie os reis**:
```python
# Carregue as imagens
white_king_img = load_image('whiteking.png')
black_king_img = load_image('blackking.png')

# Crie os reis nas posições iniciais
rei_branco = Rei("Branco", (4, 7), white_king_img, tabuleiro)
rei_preto = Rei("Preto", (4, 0), black_king_img, tabuleiro)

# Adicione às listas de peças
tabuleiro.pecas_brancas.append(rei_branco)
tabuleiro.pecas_pretas.append(rei_preto)
```

3. **Verificar cheque e cheque mate**:
```python
# Verificar se há cheque
if rei_em_cheque(tabuleiro, turno_atual):
    print(f"Cheque ao rei {turno_atual}!")

# Verificar cheque mate
if cheque_mate(tabuleiro, turno_atual):
    print(f"Cheque mate! {cor_adversaria} venceu!")

# Verificar empate
if empate_por_afogamento(tabuleiro, turno_atual):
    print("Empate por afogamento!")
```

4. **Usar no loop de eventos**:
```python
# O rei funciona igual aos peões
for peca in todas_pecas:
    if peca.rect.collidepoint(event.pos):
        tabuleiro.calcular_casas_destacadas(peca)  # Automaticamente detecta rei
        peca.iniciar_movimento(event)
```

## Características Técnicas

### Detecção Automática de Tipo de Peça
- **Rei**: Detectado pelo atributo `ja_moveu`
- **Peão**: Detectado pelo atributo `en_passant_ativo`
- **Extensível**: Fácil de adicionar outras peças no futuro

### Simulação de Movimentos
- **Sem efeitos colaterais**: Os movimentos são simulados e desfeitos
- **Estado preservado**: O tabuleiro retorna ao estado original após verificação
- **Performance otimizada**: Verificações rápidas sem modificar o jogo real

### Validação de Regras
- **Movimentos ilegais bloqueados**: Rei não pode se mover para casa atacada
- **Cheque obrigatório**: Deve sair de cheque se estiver em cheque
- **Prevenção de auto-cheque**: Não pode fazer movimento que coloque o próprio rei em cheque

## Extensibilidade

### Para Adicionar Outras Peças:
1. Crie a classe da peça (ex: `movimento_torre.py`)
2. Adicione método `get_movimentos_possiveis()`
3. Atualize `casa_atacada_por()` em `regras.py`
4. Adicione detecção em `calcular_casas_destacadas()`

### Funcionalidades Futuras:
- **Roque**: Movimento especial do rei
- **Torres, Bispos, Cavalos, Rainhas**: Outras peças do xadrez
- **Histórico de jogadas**: Para implementar regras como repetição
- **Interface gráfica melhorada**: Indicadores visuais de cheque

## Arquivos Modificados/Criados

1. **`movimento_rei.py`**: Nova classe Rei
2. **`regras.py`**: Funções de cheque e cheque mate
3. **`tabuleiro.py`**: Suporte para cálculo de movimentos do rei
4. **`exemplo_com_rei.py`**: Exemplo completo funcional
5. **`README_REI.md`**: Esta documentação

## Testando a Implementação

O arquivo `exemplo_com_rei.py` inclui:
- ✅ Movimentação básica do rei
- ✅ Detecção de cheque em tempo real
- ✅ Prevenção de movimentos ilegais
- ✅ Detecção de cheque mate
- ✅ Detecção de empate por afogamento
- ✅ Interface visual com status do jogo

Execute o exemplo e teste diferentes cenários de cheque e cheque mate! 