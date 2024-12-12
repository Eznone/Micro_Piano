# Micro_Piano

## O Teclado

Os arquivos para o teclado são os seguintes:

### BlackKeys_Ver3.stl e WhitekKeys_Ver3.stl

- Contêm chaves que devem ser montadas no Keys_Base.stl.

### Keys_Base.stl

- Design inicial feito para furar as chaves durante as fases iniciais do projeto.

### Roof_Base.stl

- Feito para segurar os fios que completam a conexão das chaves através do uso de fio terra passando pela chave e a conexão sendo concluída através do contato no telhado.

### Base_Structure.stl

- Projetado para polir o teclado e ter estabilidade devido aos fios que passam por baixo do teclado, garantindo que as teclas voltem para cima após serem pressionadas.

Tudo foi passado por uma impressora 3D para trazer o modelo do teclado.

## Usando venv

- Cria venv usando Macbook `python3 -m venv .venv` ou Windows `python -m venv .venv`
- Ativa o venv usando `source .venv\bin\activate` ou Windows `.venv\Scripts\activate`
- Baixa os bibliotecas necessarios usando `pip3 install -r requirements.txt`
- Vai ter chance que teria que dar um refresh no ambiente de trabalho
- Vai ter que baixar o seguinte para usar os fontes do partituras.py -> https://fonts.google.com/selection

## partituras.py

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

## MicroTeclado.ino

MicroTeclado.ino é um sketch para Arduino que configura e gerencia um teclado musical com botões e LEDs. Ele inclui os seguintes componentes principais:

### Inicialização dos Botões:

- Inicializa 12 objetos GFButton, cada um associado a um pino específico.

### Inicialização dos LEDs:

- Define arrays para LEDs vermelhos e verdes, cada um associado a pinos específicos.

### Função de Configuração (setup):

- Configura os pinos dos LEDs como saídas e define seu estado inicial como LOW.

### Função de Loop (loop):

- Verifica continuamente o estado dos botões, atualiza os LEDs com base nos botões pressionados e processa a entrada serial para controlar os LEDs.

## jogo_piano2.py

O código a seguir é um script Python que integra Pygame, Mido e comunicação serial para criar um jogo didático de piano. Aqui está um resumo das funcionalidades:

### Importações e Configuração:

- Importa bibliotecas necessárias (`pygame`, `mido`, `rtmidi`, `time`, `os`, `subprocess`, `serial`).
- Define funções para inicializar Pygame, MIDI e Arduino.

### Manipulação de Arquivos MIDI:

- `get_midi_files(directory)`: Retorna uma lista dos 5 primeiros arquivos MIDI na pasta.
- `load_midi_file(file_path)`: Carrega um arquivo MIDI.
- `get_midi_metadata(midi_file_path)`: Retorna o BPM e o compasso de um arquivo MIDI.
- `play_midi_events_in_real_time(midi_out, midi_file, start_time, bpm_adjusted)`: Lê eventos do arquivo MIDI e retorna uma lista de eventos para tocar em tempo real.

### Desenho da Interface:

- `draw_piano_keys(screen, active_keys)`: Desenha as teclas do piano.
- `draw_bpm_slider(screen, bpm)`: Desenha um controle deslizante para o BPM.
- `draw_metronome_lines(screen, current_time, bpm)`: Desenha linhas do metrônomo.
- `draw_toolbar(screen, midi_playing, midi_files=None)`: Desenha a barra de ferramentas.
- `draw_submenu(screen, midi_file, progress_position)`: Desenha o submenu.

### Interação com o Arduino:

- `init_arduino()`: Inicializa a conexão com o Arduino via porta serial.
- `send_notes_to_arduino(arduino, notes)`: Envia uma lista de notas para o Arduino.

### Controle do Jogo:

- `handle_keyboard_input(...)`: Lida com a entrada do teclado em tempo real para tocar notas.
- `display_notes(...)`: Representação visual das notas a serem tocadas e notas atualmente pressionadas.

### Função Principal:

- `main()`: Inicializa Pygame, MIDI, Arduino e controla o loop principal do jogo.

## backup.py

O código a seguir é um script Python que integra Pygame, Mido e comunicação serial para criar um jogo didático de piano. Aqui está um resumo das funcionalidades:

### Importações e Configuração:

- Importa bibliotecas necessárias (`pygame`, `mido`, `rtmidi`, `time`, `os`, `subprocess`, `serial`).
- Define funções para inicializar Pygame, MIDI e Arduino.

### Manipulação de Arquivos MIDI:

- `get_midi_files(directory)`: Retorna uma lista dos 5 primeiros arquivos MIDI na pasta.
- `load_midi_file(file_path)`: Carrega um arquivo MIDI.

### Configuração do MIDI e Arduino:

- `init_midi()`: Inicializa a configuração MIDI e tenta abrir a porta "PianoVirtual".
- `init_arduino()`: Inicializa a conexão com o Arduino via porta serial.
- `send_notes_to_arduino(arduino, notes)`: Envia uma lista de notas para o Arduino.

### Desenho da Interface:

- `draw_piano_keys(screen, active_keys)`: Desenha as teclas do piano.
- `draw_bpm_slider(screen, bpm)`: Desenha um controle deslizante para o BPM.
- `draw_metronome_lines(screen, current_time, bpm)`: Desenha linhas do metrônomo.
- `draw_toolbar(screen, midi_playing, midi_files=None)`: Desenha a barra de ferramentas.
- `draw_submenu(screen, midi_file, progress_position)`: Desenha o submenu.

### Controle do Jogo:

- `handle_keyboard_input(...)`: Lida com a entrada do teclado em tempo real para tocar notas.
- `display_notes(...)`: Representação visual das notas a serem tocadas e notas atualmente pressionadas.

### Função Principal:

- `main()`: Inicializa Pygame, MIDI, Arduino e controla o loop principal do jogo.

> **Nota:** O arquivo `backup.py` foi criado apenas como um teste e não deve ser considerado o arquivo principal.
