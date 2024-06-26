import gradio as gr
import sqlite3
import bcrypt
import pandas as pd
from modules.AImodel import run_detector

def video_identity(video):
    # Simulating some video processing and returning a CSV file
    data = {
        "Frame": [1, 2, 3],
        "Detail": ["Frame1 Detail", "Frame2 Detail", "Frame3 Detail"]
    }
    return run_detector.callFunc(video)
    #df = pd.DataFrame(data)
    #csv_file = "video_metadata.csv"
    #df.to_csv(csv_file, index=False)
    #return csv_file

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    record = cursor.fetchone()
    conn.close()

    if record and bcrypt.checkpw(password.encode(), record[0]):
        return "Login succeeded", gr.update(visible=True), gr.update(visible=False)
    else:
        return "Login failed. Incorrect username or password.", gr.update(visible=False),gr.update(visible=True)

def register(username, password):
    if username and password:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            conn.commit()
            return "Registration successful!"
        except sqlite3.IntegrityError:
            return "Registration failed. Username already exists."
        finally:
            conn.close()
    return "Please enter a username and password."

def create_login_interface():
    with gr.Blocks() as interface:
        tab_state = gr.Textbox(value="", visible=False)
        with gr.Tabs(visible=False) as Interfacetabs:
            with gr.TabItem("Video"):
                #run_detector.run_detector
                video_interface = gr.Interface(fn=video_identity, inputs="video", outputs="video")
            with gr.TabItem("Payment"):
                payment = gr.Textbox(value="paypal.me/dsf39248sdf",label="Paypal:")
                revo = gr.Image(value="rev.png" ,label="Revolut:")
        with gr.Tabs(visible=True) as loginTabs:
            with gr.TabItem("Login"):
                username = gr.Textbox(label="Username")
                password = gr.Textbox(label="Password", type="password")
                login_result = gr.Text(label="Login result")
                login_button = gr.Button("Login")
                login_button.click(authenticate, inputs=[username, password], outputs=[login_result, Interfacetabs,loginTabs])
            with gr.TabItem("Register"):
                new_username = gr.Textbox(label="New Username")
                new_password = gr.Textbox(label="New Password", type="password")
                register_result = gr.Text(label="Registration result")
                gr.Button("Register").click(register, inputs=[new_username, new_password], outputs=register_result)

    return interface