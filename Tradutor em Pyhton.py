import customtkinter as ctk
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import os
import threading
import time

# Configurações Globais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppTradutorPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Inicializa o mixer de áudio logo na abertura do app
        pygame.mixer.init()

        # --- ALTERADO: Nome da janela ---
        self.title("Tradutor Lucas-DEV")
        self.geometry("600x650")
        self.resizable(False, False)

        self.idiomas = {
            "Inglês": "en", "Espanhol": "es", "Francês": "fr",
            "Alemão": "de", "Italiano": "it", "Japonês": "ja"
        }

        # --- INTERFACE ---
        # --- ALTERADO: Título visual do app ---
        self.titulo = ctk.CTkLabel(self, text="TRADUTOR LUCAS-DEV", font=("Segoe UI", 28, "bold"),
                                   text_color="#3b8ed0")
        self.titulo.pack(pady=(20, 10))

        self.card = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        self.card.pack(padx=30, pady=10, fill="both", expand=True)

        self.label_lang = ctk.CTkLabel(self.card, text="Traduzir para:", font=("Segoe UI", 13, "bold"))
        self.label_lang.pack(pady=(15, 0))

        self.combo_idioma = ctk.CTkOptionMenu(self.card, values=list(self.idiomas.keys()), width=180)
        self.combo_idioma.pack(pady=10)
        self.combo_idioma.set("Inglês")

        self.label_entrada = ctk.CTkLabel(self.card, text="Texto original (Português):", font=("Segoe UI", 12))
        self.label_entrada.pack(anchor="w", padx=45)

        self.entrada = ctk.CTkTextbox(self.card, width=500, height=100, corner_radius=10, border_width=2)
        self.entrada.pack(pady=(5, 15), padx=20)
        self.entrada.insert("0.0", "Digite seu texto em Português aqui...")

        self.label_saida_titulo = ctk.CTkLabel(self.card, text="Tradução:", font=("Segoe UI", 13, "bold"),
                                               text_color="#1fcf6d")
        self.label_saida_titulo.pack(anchor="w", padx=45)

        self.saida_texto = ctk.CTkTextbox(self.card, width=500, height=100, corner_radius=10,
                                          border_width=2, fg_color="#1e1e1e", state="disabled")
        self.saida_texto.pack(pady=(5, 10), padx=20)

        self.btn_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.btn_traduzir = ctk.CTkButton(self.btn_frame, text="Traduzir & Ouvir", command=self.acao_principal,
                                          font=("Segoe UI", 14, "bold"), fg_color="#1f6aa5", width=180)
        self.btn_traduzir.grid(row=0, column=0, padx=10)

        self.btn_limpar = ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar,
                                        fg_color="#444444", width=100)
        self.btn_limpar.grid(row=0, column=1, padx=10)

    def falar(self, texto, lang_code):
        def thread_audio():
            filename = f"speech_{int(time.time())}.mp3"
            try:
                tts = gTTS(text=texto, lang=lang_code)
                tts.save(filename)

                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
:t
                while pygame.mixer.music.get_busy()yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
                    pygame.time.Clock().tick(10)

                pygame.mixer.music.unload(
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                print(f"Erro no áudio: {e}")
            finally:
                self.btn_traduzir.configure(text="Traduzir & Ouvir", state="normal")

        threading.Thread(target=thread_audio, daemon=True).start()

    def acao_principal(self):
        texto_original = self.entrada.get("1.0", "end-1c").strip()
        idioma_nome = self.combo_idioma.get()
        sigla = self.idiomas[idioma_nome]

        if texto_original and texto_original != "Digite seu texto em Português aqui...":
            self.btn_traduzir.configure(text="Processando...", state="disabled")

            try:
                resultado = GoogleTranslator(source='pt', target=sigla).translate(texto_original)

                self.saida_texto.configure(state="normal")
                self.saida_texto.delete("1.0", "end")
                self.saida_texto.insert("1.0", resultado)
                self.saida_texto.configure(state="disabled")

                self.falar(resultado, sigla)
            except Exception:
                self.saida_texto.configure(state="normal")
                self.saida_texto.insert("1.0", "Erro de conexão!")
                self.saida_texto.configure(state="disabled")
                self.btn_traduzir.configure(text="Traduzir & Ouvir", state="normal")
        else:
            self.saida_texto.configure(state="normal")
            self.saida_texto.insert("1.0", "Por favor, digite algo.")
            self.saida_texto.configure(state="disabled")

    def limpar(self):
        self.entrada.delete("1.0", "end")
        self.saida_texto.configure(state="normal")
        self.saida_texto.delete("1.0", "end")
        self.saida_texto.configure(state="disabled")


if __name__ == "__main__":
    app = AppTradutorPro()
    app.mainloop()