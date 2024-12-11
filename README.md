# Micro_Piano

## Usando venv
- Cria venv usando `python3 -m venv .venv`
- Ativa o venv usando `source .venv/bin/activate`
- Baixa os bibliotecas necessarios usando `pip3 install -r requirements.txt`
- Vai ter chance que teria que dar um refresh no ambiente de trabalho
- Vai ter que baixar o seguinte para usar os fontes do partituras.py -> https://fonts.google.com/selection

## Descrição do Código

O código no arquivo `partituras.py` é um script Python que cria uma interface gráfica (GUI) para um editor de partituras musicais usando a biblioteca `tkinter`. Aqui está um resumo das funcionalidades:

### Importações e Configuração:
- Importa bibliotecas necessárias (`tkinter`, `tempfile`, `os`, `mido`, `pygame`).
- Define variáveis globais para gerenciar a partitura.

### Manipulação de MIDI:
- Funções para criar, exportar, importar e tocar arquivos MIDI:
  - `midi()`: Cria um arquivo MIDI a partir das notas.
  - `export_midi()`: Exporta o arquivo MIDI criado para o sistema de arquivos do usuário.
  - `play_midi()`: Toca o arquivo MIDI criado usando `pygame`.
  - `import_midi()`: Importa um arquivo MIDI e desenha as notas na partitura.

### Gerenciamento de Notas e Partitura:
- Funções para selecionar, posicionar e desenhar notas na partitura:
  - `select_note()`: Solicita ao usuário a seleção de um tipo de nota e nota musical.
  - `get_note_position()`: Obtém a posição vertical de uma nota com base na clave.
  - `advance_note_position()`: Avança a posição para a próxima nota.
  - `pausa()`: Desenha um símbolo de pausa na partitura.
  - `draw_note_on_staff()`: Desenha uma nota musical ou pausa na partitura.

### Desenho da Partitura:
- Funções para desenhar a partitura e lidar com redimensionamento:
  - `select_clef()`: Redesenha a partitura quando a clave é alterada.
  - `select_meter()`: Redesenha a partitura quando o compasso é alterado.
  - `draw_partitura()`: Desenha a partitura inicial com claves, linhas e compassos.
  - `resize_canvas()`: Redesenha a partitura quando o canvas é redimensionado.

### Configuração da GUI:
- Configura a janela principal e os elementos da GUI:
  - Cria frames, canvas, botões e menus dropdown para interação do usuário.
  - Vincula eventos para redimensionamento e mudanças de seleção.
  - Inicializa o desenho da partitura.

O script permite aos usuários criar, editar, exportar, importar e tocar partituras musicais de forma visual e interativa.