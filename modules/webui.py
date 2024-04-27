import gradio as gr

def upload_file(files):
    file_paths = [file.name for file in files]
    return file_paths

def video_identity(video):
    return video

class webui:
    def __init__(self) -> None:
        demo = gr.Interface(video_identity, 
                            gr.Video(), 
                            "playable_video", 
                            )
        demo.launch()


