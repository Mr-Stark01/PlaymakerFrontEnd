import gradio as gr
import sqlite3
import bcrypt

def authenticate(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    record = cursor.fetchone()
    conn.close()

    if record and bcrypt.checkpw(password.encode(), record[0]):
        return "Logged in successfully!"
    else:
        return "Login failed. Incorrect username or password."

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
        with gr.Tab("Login"):
            username = gr.Textbox(label="Username")
            password = gr.Textbox(label="Password", type="password")
            login_result = gr.Text(label="Login result")
            gr.Button("Login").click(authenticate, inputs=[username, password], outputs=login_result)

        with gr.Tab("Register"):
            new_username = gr.Textbox(label="New Username")
            new_password = gr.Textbox(label="New Password", type="password")
            register_result = gr.Text(label="Registration result")
            gr.Button("Register").click(register, inputs=[new_username, new_password], outputs=register_result)

    return interface
    
