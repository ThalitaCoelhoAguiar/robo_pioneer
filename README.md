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

    Mario Andres  Pastrana Triana (mario.pastrana@ieee.org)
   Thalita Coelho Aguiar (222030324@aluno.unb.br)
