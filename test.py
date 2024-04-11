import tkinter as tk
from tkinter import filedialog
from ibm_watson import SpeechToTextV1 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sounddevice as sd
import numpy as np  
from scipy.io.wavfile import write as write_wav 

class SpeechToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversion de la voix en texte")
        self.root.configure(bg="#edf7f2")  # Couleur de fond printanière

        # Zone supérieure avec un bouton pour enregistrer et arrêter l'audio
        self.record_frame = tk.Frame(self.root, bg="#edf7f2")
        self.record_frame.pack(pady=20)

        self.recording = False  # Variable pour suivre l'état de l'enregistrement

        self.record_button = tk.Button(self.record_frame, text="Enregistrer l'audio", command=self.toggle_recording, bg="#003366", fg="white", padx=10, pady=5, font=("Helvetica", 12))
        self.record_button.pack(side=tk.LEFT, padx=20)

        self.upload_button = tk.Button(self.record_frame, text="Télécharger l'audio", command=self.upload_file, bg="#003366", fg="white", padx=10, pady=5, font=("Helvetica", 12))
        self.upload_button.pack(side=tk.LEFT)

        # Zone inférieure avec la boîte pour afficher le texte converti
        self.text_display = tk.Text(self.root, height=10, width=50, bg="#b3d9ff", fg="#000000", font=("Helvetica", 14, "bold"))
        self.text_display.pack(pady=20)

        apiUrl = "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/a9b1e68e-4304-472f-a94a-f076c2f1806d"
        myKey = "9r63ExBLvZ7p07OcLZAzylLFBJoz7pMTO5rRG0rqD4Op"
        auth = IAMAuthenticator(myKey)
        self.Speech2Text = SpeechToTextV1(authenticator=auth)
        self.Speech2Text.set_service_url(apiUrl)

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
            self.record_button.config(text="Convertir en texte ", bg="red")  # Changer le texte et la couleur du bouton
        else:
            self.stop_recording()
            self.record_button.config(text="Enregistrer l'audio", bg="#003366")  # Changer le texte et la couleur du bouton

    def start_recording(self):
        self.recording = True
        self.duration = 5  # Durée d'enregistrement souhaitée (en secondes)
        frames = int(self.duration * 44100)  # Calcul du nombre de trames
        self.audio_data = sd.rec(frames, samplerate=44100, channels=1, dtype=np.int16)  # Enregistrement audio
        sd.wait()  # Attendre la fin de l'enregistrement
        self.convert_audio_to_text()  # Appel de la fonction de conversion après l'enregistrement

    def stop_recording(self):
        self.recording = False
        write_wav("Rue-de-Lille.wav", 44100, self.audio_data)  # Écriture des données audio dans un fichier WAV
        self.convert_audio_to_text()  # Appel de la fonction de conversion après l'enregistrement

    def convert_audio_to_text(self):
        content_type = "audio/wav"
        with open("Thank-you-for-contact.wav", "rb") as audio_file:
            response = self.Speech2Text.recognize(audio=audio_file, content_type=content_type).get_result()
            if response["results"]:
                recognized_text = response["results"][0]["alternatives"][0]["transcript"]
            else:
                recognized_text = "No speech could be recognized."
    
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, recognized_text)


    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.wav")])
        if file_path:
            content_type = "audio/wav"
            with open(file_path, "rb") as audio_file:
                response = self.Speech2Text.recognize(audio=audio_file, content_type=content_type).get_result()
                recognized_text = response["results"][0]["alternatives"][0]["transcript"]
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(tk.END, recognized_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextGUI(root)
    root.mainloop()
