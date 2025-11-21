import wave
import math
import struct
import os
import random

# Configurações de áudio
SAMPLE_RATE = 44100

def save_wav(filename, data):
    # Garante que a pasta existe
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Pasta criada: {folder}")

    # Escreve o arquivo WAV
    with wave.open(filename, 'w') as f:
        f.setnchannels(1) # Mono
        f.setsampwidth(2) # 2 bytes (16 bit)
        f.setframerate(SAMPLE_RATE)
        
        # Converte os dados flutuantes para bytes binários
        binary_data = bytearray()
        for sample in data:
            # Clampa o valor entre -1 e 1
            sample = max(min(sample, 1.0), -1.0)
            # Converte para inteiro 16-bit assinado
            int_val = int(sample * 32767)
            binary_data.extend(struct.pack('<h', int_val))
            
        f.writeframes(binary_data)
    print(f"Arquivo gerado: {filename}")

def generate_jump_sound():
    # Gera um som de "pulo" (frequência subindo rápido)
    duration = 0.3
    n_samples = int(SAMPLE_RATE * duration)
    data = []
    
    for i in range(n_samples):
        t = i / SAMPLE_RATE
        # A frequência sobe de 200Hz para 600Hz (efeito slide)
        freq = 200 + (400 * (t / duration))
        # Onda quadrada (som estilo 8-bit/game antigo)
        val = 0.5 if math.sin(2 * math.pi * freq * t) > 0 else -0.5
        # Volume diminui no final (fade out)
        volume = 1.0 - (t / duration)
        data.append(val * volume)
    
    save_wav("sounds/jump.wav", data)

def generate_music():
    # Gera uma melodia simples em loop (estilo 8-bit)
    bpm = 180
    beat_duration = 60 / bpm
    # Notas de uma escala maior (C, E, G, A...)
    notes = [261.63, 329.63, 392.00, 440.00, 392.00, 329.63] 
    full_song = []

    # Repete a melodia 4 vezes para o arquivo não ser muito curto
    for _ in range(4):
        for note_freq in notes:
            n_samples = int(SAMPLE_RATE * beat_duration)
            for i in range(n_samples):
                t = i / SAMPLE_RATE
                # Onda triangular (som mais suave que quadrada)
                # Fórmula para onda triangular simples
                val = 2 * abs(2 * (t * note_freq - math.floor(t * note_freq + 0.5))) - 1
                full_song.append(val * 0.3) # Volume baixo (0.3) para música de fundo

    save_wav("music/bg_music.wav", full_song)

# Executa
if __name__ == "__main__":
    print("Gerando arquivos de áudio...")
    generate_jump_sound()
    generate_music()
    print("Concluído! Agora rode o jogo principal.")