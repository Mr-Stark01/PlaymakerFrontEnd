import gradio as gr

def video_identity(video):
    return video

class webui:
    def __init__(self) -> None:
        # Create Interface instances
        interface1 = gr.Interface(fn=video_identity, inputs="video", outputs="video")
        interface2 = gr.Interface(fn=video_identity, inputs="video", outputs="video")

        # Pass the Interface instances to TabbedInterface
        demo = gr.TabbedInterface([interface1, interface2], ["Hello World", "Bye World"])
        return demo;
