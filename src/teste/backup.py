import pygame
import mido
import rtmidi
import time
import os
import subprocess
import serial  # Necessário para comunicação serial
# pip install pygame mido python-rtmidi, pyserial


def get_midi_files(directory):
    """Retorna uma lista dos 5 primeiros arquivos MIDI na pasta."""
    midi_files = [f for f in os.listdir(directory) if f.endswith('.mid')]
    return midi_files[:5]  # Limita a 3 arquivos

# Initialize Pygame and set up the screen
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Didactic Piano Game")
    return screen

# MIDI setup
def init_midi():
    midi_out = rtmidi.MidiOut()
    available_ports = midi_out.get_ports()

    # Attempt to open the PianoVirtual port if available
    for port in available_ports:
        if "PianoVirtual" in port:
            midi_out.open_port(available_ports.index(port))
            print(f"Connected to MIDI port: {port}")
            return midi_out

    raise RuntimeError("No valid PianoVirtual port found. Please ensure loopMIDI is running and a virtual port named 'PianoVirtual' is created.")

# Arduino setup
def init_arduino():
    """
    Inicializa a conexão com o Arduino via porta serial.
    """
    try:
        arduino = serial.Serial('COM17', 9600)  # Substitua 'COM17' pela porta correta
        time.sleep(2)  # Aguarde a inicialização do Arduino
        print("Conexão com o Arduino estabelecida!")
        return arduino
    except serial.SerialException as e:
        print(f"Erro ao conectar com o Arduino: {e}")
        return None

# Send note list to Arduino
def send_notes_to_arduino(arduino, notes):
    note_indices = []
    note_mapping = {
        60: 1,   # C4
        61: 2,   # C#4
        62: 3,   # D4
        63: 4,   # D#4
        64: 5,   # E4
        65: 6,   # F4
        66: 7,   # F#4
        67: 8,   # G4
        68: 9,   # G#4
        69: 10,  # A4
        70: 11,  # A#4
        71: 12   # B4
    }

    for note in notes:
        if note in note_mapping:
            note_indices.append(note_mapping[note])
            #arduino.write(f"{note_mapping[note]}\n".encode())
            print(f"{note_mapping[note]}\n")

# Load MIDI file
def load_midi_file(file_path):
    return mido.MidiFile(file_path)

# Draw piano keys
def draw_piano_keys(screen, active_keys):
    white_keys = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
    black_keys = [61, 63, 66, 68, 70]  # C#4, D#4, F#4, G#4, A#4
    white_key_width = 40
    black_key_width = 25
    white_key_height = 200
    black_key_height = 120

    # Background color setup
    bg_color_light = (230, 240, 255)  # Light blue for the main background and spacings between keys
    bg_color_dark = (210, 230, 255)   # Slightly darker blue for black key areas

    screen.fill(bg_color_light)  # Fill the entire screen with the background color

    # Draw vertical background bars for visual differentiation
    black_key_width = 25
    black_key_positions = [100 + 40 - black_key_width // 2, 
                           100 + 2 * 40 - black_key_width // 2, 
                           100 + 4 * 40 - black_key_width // 2, 
                           100 + 5 * 40 - black_key_width // 2, 
                           100 + 6 * 40 - black_key_width // 2]
    for i in range(8):  # For white keys
        x = 100 + i * 40
        rect = pygame.Rect(x, 0, 40, 400)
        pygame.draw.rect(screen, (210, 220, 240), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=1)  # White outline for each vertical bar
    for i in range(5):  # For black keys
        x = black_key_positions[i]
        rect = pygame.Rect(x, 0, 25, 400)
        pygame.draw.rect(screen, (190, 210, 230), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=1)  # White outline for each vertical bar

    # Draw white keys
    for i, note in enumerate(white_keys):
        x = i * white_key_width + 100
        color = (255, 255, 255) if note not in active_keys else (0, 255, 0)
        pygame.draw.rect(screen, color, (x, 400, white_key_width, white_key_height))
        pygame.draw.rect(screen, (0, 0, 0), (x, 400, white_key_width, white_key_height), 2)

    # Draw black keys
    black_key_positions = [100 + white_key_width - black_key_width // 2, 
                           100 + 2 * white_key_width - black_key_width // 2, 
                           100 + 4 * white_key_width - black_key_width // 2, 
                           100 + 5 * white_key_width - black_key_width // 2, 
                           100 + 6 * white_key_width - black_key_width // 2]

    for i, note in enumerate(black_keys):
        x = black_key_positions[i]
        color = (0, 0, 0) if note not in active_keys else (0, 255, 0)
        pygame.draw.rect(screen, bg_color_dark, (x, 400, black_key_width, black_key_height))  # Draw background for black key area
        pygame.draw.rect(screen, color, (x, 400, black_key_width, black_key_height))

# Draw slider for BPM control
def draw_bpm_slider(screen, bpm):
    # Fundo do slider
    pygame.draw.rect(screen, (200, 200, 200), (20, 100, 20, 400))  # Slider (vertical)

    # Desenhar as linhas da régua
    font = pygame.font.Font(None, 18)
    for i in range(50, 201, 10):  # Ajuste para começar em 50
        y = 100 + ((200 - i) / 150) * 400
        pygame.draw.line(screen, (0, 0, 0), (15, y), (45, y), 1)
        bpm_text = font.render(f"{i}", True, (0, 0, 0))
        screen.blit(bpm_text, (50, y - 10))

    # Botão do slider
    slider_y = 100 + ((200 - bpm) / 150) * 400
    pygame.draw.circle(screen, (0, 0, 0), (30, int(slider_y)), 10)  # Botão do slider

    # Texto do BPM
    font = pygame.font.Font(None, 28)
    bpm_text = font.render(f"BPM: {bpm}", True, (0, 0, 0))
    screen.blit(bpm_text, (10, 520))  # Posição ajustada

# Draw metronome lines
def draw_metronome_lines(screen, current_time, bpm):
    # Calculate the speed of the lines to match the bars
    speed = (bpm / 60) * (400 / 4)
    interval = 400 / 16  # Divide into 16 sections

    # Calculate the starting position based on time to keep a continuous flow of lines
    start_y_position = 400 - (int(current_time * speed) % 400)

    # Define os limites da área de exibição (ajustar conforme o layout)
    left_limit = 100  # Margem esquerda (área onde as linhas começam)
    right_limit = 420  # Margem direita (área onde as linhas terminam)
    top_limit = 50  # Margem superior da zona de exibição
    bottom_limit = 400  # Margem inferior da zona de exibição

    # Draw lines at regular intervals
    for i in range(16):
        y_position = start_y_position - i * interval
        if y_position < top_limit:
            y_position += 400  # Wrap around to create continuous lines
        if top_limit <= y_position <= bottom_limit:  # Garante que está dentro da área
            pygame.draw.line(screen, (180, 180, 180), (left_limit, y_position), (right_limit, y_position), 1)


def draw_toolbar(screen, midi_playing, midi_files=None):
    # Barra de tarefas no topo
    toolbar_height = 50
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, 800, toolbar_height))  # Barra de ferramentas

    font = pygame.font.Font(None, 36)

    if midi_files is None:
        # Botão "Tocar MIDI"
        button_text = "Tocando..." if midi_playing else "Tocar MIDI"
        text_surface = font.render(button_text, True, (0, 0, 0))
        button_rect = pygame.Rect(10, 5, 180, 40)  # Botão movido para o canto esquerdo
        pygame.draw.rect(screen, (150, 150, 150), button_rect)
        screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))
    else:
        font = pygame.font.Font(None, 28)
        # Exibir botões de seleção de músicas
        for i, file in enumerate(midi_files):
            # Limita o texto do botão para evitar overflow
            file = file[:-4]
            truncated_file = file if len(file) <= 15 else file[:12] + "..."
            
            button_rect = pygame.Rect(10 + i * 160, 5, 150, 40)  # Espaçamento entre botões
            pygame.draw.rect(screen, (150, 150, 150), button_rect)  # Fundo cinza do botão
            pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)  # Borda preta
            text_surface = font.render(truncated_file, True, (0, 0, 0))
            screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 5))
    
    # Botão para trocar de jogo
    pygame.draw.rect(screen, (150, 50, 50), (650, 5, 140, 40))  # Fundo vermelho
    pygame.draw.rect(screen, (0, 0, 0), (650, 5, 140, 40), 2)  # Borda preta
    switch_text = font.render("Abrir Partitura", True, (255, 255, 255))
    screen.blit(switch_text, (660, 10))  # Ajusta o texto para dentro do botão

def draw_submenu(screen, midi_file, progress_position):
    pygame.draw.rect(screen, (240, 240, 240), (500, 50, 290, 500))  # Fundo do submenu
    font = pygame.font.Font(None, 28)

    # Título do submenu
    title = f"Tocando: {midi_file.split('/')[-1] if midi_file else 'Nenhum'}"
    title_surface = font.render(title, True, (0, 0, 0))
    screen.blit(title_surface, (510, 60))

    # Botão "Tocar"
    play_button = pygame.Rect(510, 120, 100, 40)
    pygame.draw.rect(screen, (150, 150, 150), play_button)
    play_text = font.render("Tocar", True, (0, 0, 0))
    screen.blit(play_text, (play_button.x + 25, play_button.y + 10))

    # Botão "Pausar"
    pause_button = pygame.Rect(620, 120, 100, 40)
    pygame.draw.rect(screen, (150, 150, 150), pause_button)
    pause_text = font.render("Pausar", True, (0, 0, 0))
    screen.blit(pause_text, (pause_button.x + 20, pause_button.y + 10))

    # Barra de progresso
    pygame.draw.rect(screen, (200, 200, 200), (510, 200, 200, 20))  # Fundo da barra
    pygame.draw.rect(screen, (0, 0, 0), (510, 200, 200, 20), 2)  # Contorno da barra

    # Indicador de posição
    progress_x = 510 + int(progress_position * 200)  # Calcula a posição do indicador
    pygame.draw.rect(screen, (0, 100, 255), (progress_x - 5, 200, 10, 20))  # Indicador



def get_midi_length(midi_file_path):
    """
    Retorna a duração (em segundos) do arquivo MIDI.
    """
    try:
        midi = mido.MidiFile(midi_file_path)
        total_time = 0
        for msg in midi:
            if not msg.is_meta:
                total_time += msg.time
        return total_time
    except Exception as e:
        print(f"Erro ao calcular a duração do arquivo MIDI: {e}")
        return 0  # Retorna 0 se ocorrer um erro



# Visual representation of notes to be played and currently pressed notes
def display_notes(screen, notes, current_time, active_keys, active_bars, bpm, metronome_light, midi_playing):
    draw_piano_keys(screen, active_keys)
    draw_bpm_slider(screen, bpm)
    draw_metronome_lines(screen, current_time, bpm)

    # Draw metronome light
    metronome_color = (255, 0, 0) if metronome_light else (100, 0, 0)
    pygame.draw.circle(screen, metronome_color, (30, 75), 15)  # Posição ajustada para o topo do slider


    # Draw active bars above the keys
    white_key_bars = []
    black_key_bars = []

    for note, bars in list(active_bars.items()):
        if note in [60, 62, 64, 65, 67, 69, 71, 72]:
            key_width = 40
            white_keys = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5
            x = (white_keys.index(note)) * key_width + 100  # Adjust the x position for white keys
            color = (100, 149, 237)  # Darker blue color for white keys (less dark than black key bars)
            outline_color = None
            for start_time, released in bars:
                bar_height = max(0, int((current_time - start_time) * (bpm / 60) * 400 / 4)) if released is None else int((released - start_time) * (bpm / 60) * 400 / 4)
                y_position = 400 - bar_height if released is None else 400 - bar_height - int((current_time - released) * (bpm / 60) * 400 / 4)
                if y_position + bar_height > 0:
                    white_key_bars.append((x + 1, y_position, key_width - 2, bar_height, color, outline_color))
        else:
            key_width = 25
            black_key_positions = [100 + 40 - key_width // 2, 
                                   100 + 2 * 40 - key_width // 2, 
                                   100 + 4 * 40 - key_width // 2, 
                                   100 + 5 * 40 - key_width // 2, 
                                   100 + 6 * 40 - key_width // 2]
            x = black_key_positions[[61, 63, 66, 68, 70].index(note)]
            color = (0, 0, 139)  # Navy blue color for black keys
            outline_color = (0, 0, 0)  # Black outline for black key bars
            for start_time, released in bars:
                bar_height = max(0, int((current_time - start_time) * (bpm / 60) * 400 / 4)) if released is None else int((released - start_time) * (bpm / 60) * 400 / 4)
                y_position = 400 - bar_height if released is None else 400 - bar_height - int((current_time - released) * (bpm / 60) * 400 / 4)
                if y_position + bar_height > 0:
                    black_key_bars.append((x + 1, y_position, key_width - 2, bar_height, color, outline_color))

    # Draw white key bars first
    for x, y, width, height, color, _ in white_key_bars:
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color, rect, border_radius=10)

    # Draw black key bars on top of white key bars
    for x, y, width, height, color, outline_color in black_key_bars:
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color, rect, border_radius=10)
        if outline_color:
            pygame.draw.rect(screen, outline_color, rect, width=1, border_radius=10)
    
    for note, timestamp in notes:
        x = (note - 60) * 20 + 100
        y = 500 - int((current_time - timestamp) * (bpm / 60) * 100 / 4)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, 15, 50))
    
    draw_toolbar(screen, midi_playing)
    

# Handle real-time keyboard input to play notes
def handle_keyboard_input(midi_out, active_keys, active_bars, bpm, midi_playing, midi_events, event_index, midi_start_time, midi_files, selecting_midi, midi_file, metronome_sound_on, submenu_visible, is_paused, progress_position):
    # O resto do código permanece o mesmo

    # Adicionamos parâmetros midi_playing, midi_events, event_index, midi_start_time 
    # para controle do estado de reprodução e reinício do MIDI quando necessário.
    
    keys = {
        pygame.K_a: 60,  # C4
        pygame.K_w: 61,  # C#4
        pygame.K_s: 62,  # D4
        pygame.K_e: 63,  # D#4
        pygame.K_d: 64,  # E4
        pygame.K_f: 65,  # F4
        pygame.K_t: 66,  # F#4
        pygame.K_g: 67,  # G4
        pygame.K_y: 68,  # G#4
        pygame.K_h: 69,  # A4
        pygame.K_u: 70,  # A#4
        pygame.K_j: 71,  # B4
        pygame.K_k: 72   # C5
    }

    running = True
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in keys:
                note = keys[event.key]
                midi_out.send_message([0x90, note, 80])  # Note on
                active_keys.add(note)
                if note not in active_bars:
                    active_bars[note] = []
                active_bars[note].append((time.time(), None))
        elif event.type == pygame.KEYUP:
            if event.key in keys:
                note = keys[event.key]
                midi_out.send_message([0x80, note, 0])  # Note off
                if note in active_keys:
                    active_keys.remove(note)
                if note in active_bars:
                    for i, (start_time, released) in enumerate(active_bars[note]):
                        if released is None:
                            active_bars[note][i] = (start_time, time.time())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique com o botão esquerdo
                x, y = event.pos
                if selecting_midi:
                    # Verifica se clicou em algum botão de música
                    for i, file in enumerate(midi_files):
                        if 10 + i * 160 <= x <= 10 + i * 160 + 150 and 5 <= y <= 45:
                            try:
                                midi_file = f"C:\\Users\\caval\\OneDrive\\Desktop\\janks\\musicas\\{file}"
                                midi_start_time = time.time()

                                # Obtemos o BPM e o compasso do arquivo MIDI
                                bpm, time_signature = get_midi_metadata(midi_file)
                                print(f"BPM ajustado para: {bpm}, Compasso: {time_signature[0]}/{time_signature[1]}")

                                midi_events = play_midi_events_in_real_time(midi_out, load_midi_file(midi_file), midi_start_time, bpm)
                                event_index = 0
                                midi_playing = True
                                selecting_midi = False  # Sai do estado de seleção
                                submenu_visible = True  # Exibe o submenu
                            except Exception as e:
                                print(f"Erro ao carregar arquivo MIDI: {e}")
                            return running, bpm, midi_playing, event_index, midi_events, selecting_midi, midi_start_time, midi_file, metronome_sound_on, submenu_visible, is_paused, progress_position


                # Check slider BPM
                if 20 <= x <= 40 and 100 <= y <= 500:  # Slider de BPM
                    # Check slider BPM
                    raw_bpm = 200 - ((y - 100) / 400) * 150
                    new_bpm = max(10, min(200, round(raw_bpm / 10) * 10))  # Round ajustado para a lógica correta
                    if new_bpm != bpm:  # Somente ajusta se o BPM mudar
                        print(f"BPM ajustado de {bpm} para {new_bpm}")
                        bpm_ratio = bpm / new_bpm  # Razão entre o BPM antigo e o novo
                        bpm = new_bpm
                        # Recalcula o tempo dos eventos restantes
                        current_time = time.time()
                        selected_time = progress_position * get_midi_length(midi_file)  # Tempo em segundos baseado na barra de progresso

                        midi_events = [
                            (
                                (event_time - selected_time) * bpm_ratio + (current_time - midi_start_time),
                                msg
                            )
                            for event_time, msg in midi_events if event_time >= selected_time
                        ]

                        event_index = 0  # Reinicia o índice de eventos, pois recalculamos os tempos

                # Verifica se clicou no botão para trocar de jogo
                if 650 <= x <= 790 and 5 <= y <= 45:  # Coordenadas do botão
                    pygame.quit()
                    subprocess.run(["python", "OneDrive\\Desktop\\janks\\partitura.py"])  # Substitua pelo caminho completo, se necessário
                    running = False
                    return running, bpm, midi_playing, event_index, midi_events, selecting_midi, midi_start_time, midi_file, metronome_sound_on, submenu_visible, is_paused, progress_position

                # Verifica se clicou na luz do metrônomo
                if 15 <= x <= 45 and 60 <= y <= 90:  # Coordenadas da luz do metrônomo
                    metronome_sound_on = not metronome_sound_on  # Alterna o estado do som
                    print(f"Som do metrônomo {'ligado' if metronome_sound_on else 'desligado'}")

                # Verifica se clicou na barra de progresso
                if submenu_visible and 510 <= x <= 710 and 200 <= y <= 220:
                    # Calcula a posição de progresso com base no clique
                    progress_position = max(0, min((x - 510) / 200, 1))  # Normaliza entre 0 e 1

                     # Calcula o tempo selecionado com base na barra de progresso
                    selected_time = progress_position * get_midi_length(midi_file)
                    
                    # Ajusta o índice de eventos para começar do tempo selecionado
                    event_index = next(
                        (i for i, (event_time, _) in enumerate(midi_events) if event_time >= selected_time), 
                        len(midi_events)
                    )


                # Verifica se clicou no botão "Tocar"
                if submenu_visible and 510 <= x <= 610 and 120 <= y <= 160:
                    is_paused = False
                    midi_playing = True
                    # Calcula o tempo selecionado com base na barra de progresso
                    selected_time = progress_position * get_midi_length(midi_file)
                    
                    # Ajusta o índice de eventos e atualiza midi_start_time
                    midi_start_time = time.time() - selected_time
                    event_index = next(
                        (i for i, (event_time, _) in enumerate(midi_events) if event_time >= selected_time), 
                        len(midi_events)
                    )


                # Verifica se clicou no botão "Pausar"
                elif submenu_visible and 620 <= x <= 720 and 120 <= y <= 160:
                    is_paused = True
                    midi_playing = False  # Mantém o estado de reprodução para recomeçar no mesmo ponto

                # Check botão "Tocar MIDI"
                if not selecting_midi and 10 <= x <= 190 and 5 <= y <= 45:
                    if midi_playing:
                        midi_playing = False
                        submenu_visible = False  # Oculta o submenu
                        for note in list(active_keys):
                            midi_out.send_message([0x80, note, 0])
                        active_keys.clear()
                        active_bars.clear()
                    else:
                        selecting_midi = True  # Exibir botões de seleção de músicas
                        
        elif event.type == pygame.QUIT:
            running = False

    return running, bpm, midi_playing, event_index, midi_events, selecting_midi, midi_start_time, midi_file, metronome_sound_on, submenu_visible, is_paused, progress_position



def get_midi_metadata(midi_file_path):
    """
    Retorna o BPM e o compasso (time signature) de um arquivo MIDI.
    """
    try:
        midi = mido.MidiFile(midi_file_path)
        bpm = 120  # Valor padrão de BPM
        time_signature = (4, 4)  # Valor padrão de compasso

        for track in midi.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    bpm = mido.tempo2bpm(msg.tempo)  # Converte microsegundos por beat para BPM
                    print(bpm)
                if msg.type == 'time_signature':
                    time_signature = (msg.numerator, msg.denominator)
                    print(time_signature)

        return bpm, time_signature
    except Exception as e:
        print(f"Erro ao processar o arquivo MIDI: {e}")
        return 120, (4, 4)  # Valores padrão em caso de erro


def play_midi_events_in_real_time(midi_out, midi_file, start_time, bpm_adjusted):
    """
    Lê eventos do arquivo MIDI e retorna uma lista de eventos para tocar em tempo real,
    ajustando o tempo de acordo com o BPM ajustado.
    """
    events = []
    bpm_original = 120  # BPM assumido como padrão se não especificado no MIDI
    elapsed_time = time.time() - start_time  # Tempo decorrido desde o início
    tempo_factor = bpm_original / bpm_adjusted  # Fator para escalonar o tempo

    for track in midi_file.tracks:
        current_time = elapsed_time
        for msg in track:
            if not msg.is_meta:
                # Ajusta o tempo do evento com base no fator de escala
                current_time += msg.time * tempo_factor
                events.append((current_time / 1000, msg))  # Convert tempo para segundos

    events.sort(key=lambda x: x[0])  # Ordena os eventos pelo tempo
    return events



    

def main():
    screen = init_pygame()
    midi_out = init_midi()
    arduino = init_arduino()

    midi_file = 'musicas/São João.mid'
    midi_files = get_midi_files('C:\\Users\\caval\\OneDrive\\Desktop\\janks\\musicas')  # Obtém os arquivos MIDI
    if not midi_files:
        print("Nenhum arquivo MIDI encontrado na pasta 'musicas'.")
        pygame.quit()
        return
    print(f"Arquivos MIDI encontrados: {midi_files}")

    active_keys = set()
    active_bars = {}
    bpm = 120  # BPM inicial
    metronome_last_time = time.time()
    metronome_light = False
    metronome_sound_on = False  # Inicialmente o som do metrônomo está ligado
    # Variáveis adicionais para o compasso
    time_signature = (4,4)  # Número de batidas por compasso (ex: 3 para valsa, 4 para 4/4, 2 para marcha)
    beat_counter = 0  # Contador de batidas dentro do compasso
    submenu_visible = False  # Define se o sub-menu está visível
    progress_position = 0  # Posição inicial da barra de progresso (em porcentagem)
    is_paused = False


    # Variáveis para controle de reprodução MIDI
    midi_playing = False
    midi_file = None  # Nenhum arquivo MIDI selecionado inicialmente
    selecting_midi = False  # Controla se estamos selecionando uma música
    midi_start_time = time.time()
    midi_events = play_midi_events_in_real_time(
        midi_out, load_midi_file(midi_file), midi_start_time, bpm
    )

    event_index = 0

    running = True
    while running:
        current_time = time.time()

        #print(f"Estado: tocando MIDI: {midi_playing}, selecionando MIDI: {selecting_midi}")

        # Processa eventos MIDI apenas quando tocando
        if midi_playing and not selecting_midi and not is_paused:

            while event_index < len(midi_events) and current_time - midi_start_time >= midi_events[event_index][0]:
                event_time, msg = midi_events[event_index]
                if not msg.is_meta:
                    midi_out.send_message(msg.bytes())
                    print(msg.bytes())
                    if msg.type == 'note_on' and msg.velocity > 0:
                        active_keys.add(msg.note)
                        if msg.note not in active_bars:
                            active_bars[msg.note] = []
                        active_bars[msg.note].append((current_time, None))
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        if msg.note in active_keys:
                            active_keys.remove(msg.note)
                        if msg.note in active_bars:
                            for i, (start_time, released) in enumerate(active_bars[msg.note]):
                                if released is None:
                                    active_bars[msg.note][i] = (start_time, current_time)
                event_index += 1


            # Finaliza a reprodução do MIDI
            if event_index >= len(midi_events):
                is_paused = True

        # Lógica do metrônomo
        metronome_duration = 0.05  # Duração da luz em segundos
        if current_time - metronome_last_time >= 60 / bpm:
            metronome_light = True  # Acende a luz
            metronome_last_time = current_time

            # Incrementa o contador de batidas
            beat_counter = (beat_counter + 1) % time_signature[0]  # Reseta ao atingir o número do compasso

            if metronome_sound_on:  # Verifica se o som está ativado
                if beat_counter == 0:
                    # Som diferenciado para a primeira batida do compasso
                    midi_out.send_message([0x90, 110, 50])  # Nota forte no MIDI
                else:
                    # Som regular para outras batidas
                    midi_out.send_message([0x90, 100, 50])  # Nota regular no MIDI

        elif current_time - metronome_last_time >= metronome_duration:
            metronome_light = False  # Apaga a luz após o tempo definido
            
            if metronome_sound_on:  # Verifica se o som está ativado
                midi_out.send_message([0x90, 100, 0])  # Desliga o som do metrônomo regular
                midi_out.send_message([0x90, 110, 0])  # Desliga o som do metrônomo forte




        # Processa entrada e alterna estados
        # Passar midi_file como parte do estado retornado
        running, bpm, midi_playing, event_index, midi_events, selecting_midi, midi_start_time, midi_file, metronome_sound_on, submenu_visible, is_paused, progress_position = handle_keyboard_input(
            midi_out, active_keys, active_bars, bpm, midi_playing, midi_events, event_index, midi_start_time, midi_files, selecting_midi, midi_file, metronome_sound_on, submenu_visible, is_paused, progress_position
        )

        # Renderiza a interface com base no estado atual
        if selecting_midi:
            draw_toolbar(screen, midi_playing, midi_files)  # Exibe os botões de músicas
        else:
            display_notes(screen, [], current_time, active_keys, active_bars, bpm, metronome_light, midi_playing)
        # Renderiza o submenu se visível


        if submenu_visible or selecting_midi:
            draw_submenu(screen, midi_file, progress_position)
        
        pygame.display.flip() 
    pygame.quit()




if __name__ == "__main__":
    main()
