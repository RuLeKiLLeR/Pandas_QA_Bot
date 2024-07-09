import gradio as gr
import os
import shutil
import argparse
from Pandas_QA_Bot.backend.main import PandasGptAgent, setup_logging

# Argument parsing
parser = argparse.ArgumentParser(description="A script to handle profiles project and custom prompt.")
parser.add_argument('--custom_prompt', type=str, required=False, default="",
                    help='The custom prompt value.')
args = parser.parse_args()

setup_logging()

agent_class = PandasGptAgent(api_key="sk-customergpt-dev-Otayp2OBMkZiJfRtDPilT3BlbkFJQ2u29xMhe5eT2QIKaOX4")
global agent


def on_submit(csv_file, desc_file):
    global csv_path
    global desc_path
    if csv_file is not None:
        csv_path = os.path.join("data", csv_file.name)
        shutil.move(csv_file.name, csv_path)

    if desc_file is not None:
        desc_path = os.path.join("data", desc_file.name)
        shutil.move(desc_file.name, desc_path)

    global agent
    agent = agent_class.create_agent(csv_path, desc_path, args.custom_prompt)

    return gr.update(visible=True)


with gr.Blocks() as demo:
    with gr.Tab("Upload"):
        gr.Markdown("# Welcome to our dataset QA Bot")
        csv_upload = gr.File(label="Upload CSV File", file_types=[".csv"])
        desc_upload = gr.File(label="Upload Column Descriptions (Text File)", file_types=[".txt"])
        submit_btn = gr.Button("Submit")

    with gr.Tab("Chat") as chat_tab:
        gr.Markdown("# Chat Interface")
        chat_interface = gr.ChatInterface(
            fn=lambda prompt, history: PandasGptAgent.chat_prompt(prompt, agent),
            title="Dataset QA Bot",
            examples=["Who is our highest paying customer?", "Which CSM has most enterprise accounts?",
                      "What percentage of our customers use Transformations?"]
        )

        feedback_good = gr.Button("Good Response")
        feedback_bad = gr.Button("Bad Response")

    submit_btn.click(on_submit, [csv_upload, desc_upload], chat_tab)

demo.launch()

# import gradio as gr
# import os
# import shutil
# import argparse
# import logging
# from Pandas_QA_Bot.backend.main import PandasGptAgent, setup_logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
# )
# logger = logging.getLogger("text2sql")
# # Argument parsing
# parser = argparse.ArgumentParser(description="A script to handle profiles project and custom prompt.")
# parser.add_argument('--custom_prompt', type=str, required=False, default="",
#                     help='The custom prompt value.')
# args = parser.parse_args()
#
# setup_logging()
#
# agent_class = PandasGptAgent(api_key="sk-customergpt-dev-Otayp2OBMkZiJfRtDPilT3BlbkFJQ2u29xMhe5eT2QIKaOX4")
#
#
#
#
# def on_submit(csv_file, desc_file):
#     global csv_path, desc_path, agent
#     if csv_file is not None:
#         csv_path = os.path.join("data", csv_file.name)
#         shutil.move(csv_file.name, csv_path)
#
#     if desc_file is not None:
#         desc_path = os.path.join("data", desc_file.name)
#         shutil.move(desc_file.name, desc_path)
#
#     agent = agent_class.create_agent(csv_path, desc_path, "")
#     return gr.update(visible=True)
#
#
# def chat_fn(prompt, history):
#     global agent
#     if history is None:
#         history = []
#     response = agent_class.chat_prompt(prompt, agent, history)
#     history.append(("user", prompt))
#     history.append(("assistant", response))
#     return history
#
#
# def feedback_fn(feedback, history):
#     if history is None:
#         history = []
#     if len(history) < 2:
#         return history
#
#     user_prompt = history[-2][1]
#     assistant_response = history[-1][1]
#
#     if feedback == "positive":
#         # Handle positive feedback
#         print("Positive feedback received")
#     elif feedback == "negative":
#         # Handle negative feedback
#         feedback_str = (
#             f"Feedback: User marked this as a bad response. Please review and improve.\n"
#         )
#         history[-1] = ("assistant", assistant_response + "\n" + feedback_str)
#
#     return history
#
#
# with gr.Blocks() as demo:
#     with gr.Tab("Upload"):
#         gr.Markdown("# Welcome to our dataset QA Bot")
#         csv_upload = gr.File(label="Upload CSV File", file_types=[".csv"])
#         desc_upload = gr.File(label="Upload Column Descriptions (Text File)", file_types=[".txt"])
#         submit_btn = gr.Button("Submit")
#
#     with gr.Tab("Chat") as chat_tab:
#         history = []
#         gr.Markdown("# Chat Interface")
#         with gr.Row():
#             inp = gr.Textbox(placeholder="What is your name?")
#             out = gr.Textbox()
#         btn = gr.Button("Run")
#         btn.click(fn=chat_fn, inputs=[inp, history], outputs=out)
#
#         feedback_good = gr.Button("Good Response")
#         feedback_bad = gr.Button("Bad Response")
#
#     # Link actions to interface components
#     submit_btn.click(on_submit, [csv_upload, desc_upload], chat_tab)
#     feedback_good.click(lambda history: feedback_fn("positive", history), None, chat_tab)
#     feedback_bad.click(lambda history: feedback_fn("negative", history), None, chat_tab)
#
# # Launch the demo interface
# demo.launch()