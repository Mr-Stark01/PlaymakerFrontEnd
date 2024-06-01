import gradio as gr
import sqlite3
import bcrypt
import pandas as pd
from launch import switch

def video_identity(video):
    # Simulating some video processing and returning a CSV file
    data = {
        "Frame": [1, 2, 3],
        "Detail": ["Frame1 Detail", "Frame2 Detail", "Frame3 Detail"]
    }
    df = pd.DataFrame(data)
    csv_file = "video_metadata.csv"
    df.to_csv(csv_file, index=False)
    return csv_file

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    record = cursor.fetchone()
    conn.close()

    if record and bcrypt.checkpw(password.encode(), record[0]):
        return "Login succeeded", gr.update(visible=True)
    else:
        return "Login failed. Incorrect username or password.", gr.update(visible=False)

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
        
        with gr.Tabs(visible=False) as tabs:
            with gr.TabItem("Video"):
                video_interface = gr.Interface(fn=video_identity, inputs="video", outputs="file")
                video_interface.render()
            with gr.TabItem("Payment"):
                payment = gr.Text(label="Paypal:")

        with gr.Tab("Login"):
            username = gr.Textbox(label="Username")
            password = gr.Textbox(label="Password", type="password")
            login_result = gr.Text(label="Login result")
            login_button = gr.Button("Login")
            login_button.click(authenticate, inputs=[username, password], outputs=[login_result, tabs])

        with gr.Tab("Register"):
            new_username = gr.Textbox(label="New Username")
            new_password = gr.Textbox(label="New Password", type="password")
            register_result = gr.Text(label="Registration result")
            gr.Button("Register").click(register, inputs=[new_username, new_password], outputs=register_result)

        def update_tabs(tab_state):
            tabs.change()
            if tab_state == "Video":
                tabs.select("Video")  # Selecting the first tab (Video)
            elif tab_state == "Payment":
                tabs.select("Payment")  # Selecting the second tab (Payment)
            return gr.update()

        tabs.change(fn=update_tabs, inputs=tab_state, outputs=[])

    return interface