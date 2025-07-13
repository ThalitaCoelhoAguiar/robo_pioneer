# robo_pioneer
Robótica

# Controle de Robô Pioneer no CoppeliaSim

Este repositório contém dois métodos distintos de controle para um robô móvel Pioneer no simulador **CoppeliaSim**, desenvolvidos no contexto do projeto EVA/MARIA da Universidade de Brasília (FGA):

- **`path_pioneer_M_questao2_trab1.py`**: Controle baseado em *waypoints* com orientação por PID.
- **`Primitivas_Pioneer_questao1_trab1.py`**: Controle baseado em primitivas de movimento (reta e giro), usado para formar trajetórias como "L", "M", etc.

## 📁 Estrutura do Repositório

├── path_pioneer_M_questao2_trab1.py # Controle com PID e waypoints
├── Primitivas_Pioneer_questao1_trab1.py # Controle com primitivas (reta + curva)
├── Pioneer_experiment.csv # Dados de saída (posição do robô)
└── README.md # Este arquivo

- Python 3.x
- [CoppeliaSim](https://www.coppeliarobotics.com/)
- Biblioteca `sim.py` (incluída no CoppeliaSim para comunicação remota)
- Pacotes Python:
  - `numpy`
  - `math`
  - `csv`
 
##  Como Usar

### 1. Inicie o CoppeliaSim
- Certifique-se de que o servidor remoto está ativo (porta padrão: `19999`).
- Carregue uma cena com o robô **Pioneer_p3dx** (e opcionalmente a bola, se necessário).
- Acione o Real-time(o relógio no Coppelia)

### 2. Execute um dos scripts

**Controle com Waypoints (PID):**
```bash
python path_Pioneer.py
Controle com Primitivas (reta + curva):


No path_Pioneer.py, edite a lista:

waypoints = [
    [-1.75, -0.75],
    [-0.9625, -1.4125],
    [-0.175, -0.75],
    [-0.175, -2.05],
]

No primitivas.py, você pode editar:

if __name__ == "__main__":
    crb01 = Pioneer()
    x = 1.5      # deslocamento no eixo X (após o giro)
    y = 2    # deslocamento inicial no eixo Y
    v = 0.1      # velocidade linear (m/s)

    crb01.executar_movimento_L_com_primitivas(x, y, v)


1) Uma visão geral da situação

1.1) Para rodar as simulações
Para a simulação:

- Python 3.x
- [CoppeliaSim](https://www.coppeliarobotics.com/)
- Biblioteca `sim.py` (incluída no CoppeliaSim para comunicação remota)
- Pacotes Python:
  - `numpy`
  - `math`
  - `csv`
 
##  Como Usar

### 1. Inicie o CoppeliaSim
- Certifique-se de que o servidor remoto está ativo (porta padrão: `19999`).
- Carregue uma cena com o robô **Pioneer_p3dx** (e opcionalmente a bola, se necessário).
- Acione o Real-time(o relógio no Coppelia)

### 2. Execute um dos scripts

1.2) Base teórica

Em ambas as simulações utiliza-se robô com duas rodas, logo implementa-se o robô com a definição das rodas e a distância entre as rodas. Para que haja a moviementação foi definida a velocidade de cada uma das rodas evidenciadas a seguir:

v = (v_R + v_L) / 2  
ω = (v_R - v_L) / L


2) Uma visão geral de cada abordagem

Demo 2:

2.1) Fazer com que o robô percorra uma sequência de dois ou mais pontos: "demo1.py".
Foi utilizado como base o programa path_Pioneer.py
 A movimentação foi baseada na implementação do tempo que o robô cumpre cada um dos comandos.
Para correlacionar com o input de distancia, definiu-se o tempo como t=Velocidade_linear*distância.
evidenciado na linha do código:
....
Dessa forma, foram definidos 3 tipos de movimentos:
1_Seguir reto
2_Girar para esquerda
3_Girar para direita

Para a movimentação do robô para direita ou esquerda foi necessário também a definição do raio que o robo segue quando gira. O robô segue em linha reta no eixo y, e então, robô segue aproximada uma trajetoria de arco de 90 graus e segue para o próximo comando que é seguir reto no eixo X. O tempo de movimentação foi calculado sobre a distancia definida do main subtraida do raio da trajetória, uma vez que que no giro, o robo acrescenta um raio na trajeotria  tanto no eixo x como no y.

As três movimentações implmentadas são evidenciadas a seguir:

            if primitiva == 1:
                omega = 0
            elif primitiva == 2:
                radio_ideal = 0.5
                omega = -self.v_linear / (-radio_ideal)  # curva à esquerda
            elif primitiva == 3:
                radio_ideal = 0.5
                omega = -self.v_linear / radio_ideal     # curva à direita
            else:
                omega = 0





3) as equações em Latex utilizadas para explicar a modelagem do robô
4) uma descrição (pseudo código) dos programas "demo1.py" e "demo2.py" explicando a lógica do 
