import os
import pandas as pd
import logging
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

logger = logging.getLogger("text2sql")


class PandasGptAgent:
    def __init__(self, api_key: str):
        self.api_key = "sk-customergpt-dev-Otayp2OBMkZiJfRtDPilT3BlbkFJQ2u29xMhe5eT2QIKaOX4"
        os.environ['OPENAI_API_KEY'] = api_key

    @staticmethod
    def fetch_column_descriptions(file_path: str) -> str:
        """Fetches column descriptions from a text file"""
        with open(file_path, 'r') as file:
            descriptions = file.read().strip()
        return descriptions

    def create_agent(self, csv_file_path: str, txt_file_path: str, custom_prompt: str):
        default_prompt = (
            "A csv file is given to you and you need to perform question and answering by keeping the data of the csv in mind"
        )

        if not custom_prompt:
            custom_prompt = default_prompt

        c360 = pd.read_csv(csv_file_path)
        column_descriptions = self.fetch_column_descriptions(txt_file_path)

        if column_descriptions:
            prefix = (
                custom_prompt +
                " Description of some of the columns in the table are given as {col1}: {description1}; {col2}: {description2}; etc" +
                column_descriptions +
                ". Some columns may not have this description, try to infer the meaning from the name of the column in such cases."
            )
        else:
            prefix = custom_prompt + " Try to infer the meaning of columns from their names."

        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125"),
            c360,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix=prefix
        )

        return agent

    @staticmethod
    def chat_prompt(prompt, agent):
        logger.info(f"Prompt: {prompt}")
        response = agent.run(prompt)
        logger.info(f"Response: {response}")
        return response


def setup_logging():
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("text2sql.log")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# import os
# import pandas as pd
# import logging
# from langchain.agents.agent_types import AgentType
# from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
# from langchain_openai import ChatOpenAI
#
# logger = logging.getLogger("text2sql")
#
# class LRUCache:
#     def __init__(self, capacity):
#         self.capacity = capacity
#         self.cache = {}
#         self.order = []
#
#     def get(self, key):
#         if key in self.cache:
#             self.order.remove(key)
#             self.order.append(key)
#             return self.cache[key]
#         else:
#             return None
#
#     def put(self, key, value):
#         if len(self.cache) >= self.capacity:
#             lru_key = self.order.pop(0)
#             del self.cache[lru_key]
#         self.cache[key] = value
#         self.order.append(key)
#
# class PandasGptAgent:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         os.environ['OPENAI_API_KEY'] = api_key
#         self.cache = LRUCache(capacity=100)
#
#     @staticmethod
#     def fetch_column_descriptions(file_path: str) -> str:
#         """Fetches column descriptions from a text file"""
#         with open(file_path, 'r') as file:
#             descriptions = file.read().strip()
#         return descriptions
#
#     def create_agent(self, csv_file_path: str, txt_file_path: str, custom_prompt: str):
#         default_prompt = (
#             "A csv file is given to you and you need to perform question and answering by keeping the data of the csv in mind"
#         )
#
#         if not custom_prompt:
#             custom_prompt = default_prompt
#
#         c360 = pd.read_csv(csv_file_path)
#         column_descriptions = self.fetch_column_descriptions(txt_file_path)
#
#         if column_descriptions:
#             prefix = (
#                 custom_prompt +
#                 " Description of some of the columns in the table are given as {col1}: {description1}; {col2}: {description2}; etc" +
#                 column_descriptions +
#                 ". Some columns may not have this description, try to infer the meaning from the name of the column in such cases."
#             )
#         else:
#             prefix = custom_prompt + " Try to infer the meaning of columns from their names."
#
#         agent = create_pandas_dataframe_agent(
#             ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125"),
#             c360,
#             verbose=True,
#             agent_type=AgentType.OPENAI_FUNCTIONS,
#             prefix=prefix
#         )
#
#         return agent
#
#     def chat_prompt(self, prompt, agent, history):
#         if (cached_result := self.cache.get(prompt)):
#             # logger.info(f"Prompt: {prompt} (Cached)")
#             # logger.info(f"Response: {cached_result}")
#             return cached_result
#         else:
#             if history is None:
#                 response = agent.run(prompt)
#                 self.cache.put(prompt, response)
#             else:
#                 full_prompt = self.convert_history_to_prompt(prompt, history)
#                 response = agent.run(full_prompt)
#                 self.cache.put(prompt, response)
#             # logger.info(f"Prompt: {prompt}")
#             # logger.info(f"Response: {response}")
#             return response
#
#     @staticmethod
#     def convert_history_to_prompt(new_message: str, history):
#         prev_conv = "Previous Conversation:\n\t" + ";\t ".join(
#             [f"{role}: {message}" for role, message in history]
#         )
#         return prev_conv + "\n" + "Given the previous conversation, answer the following query:\nUser: " + new_message
#
# def setup_logging():
#     logger.setLevel(logging.DEBUG)
#
#     file_handler = logging.FileHandler("text2sql.log")
#     file_handler.setLevel(logging.INFO)
#
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.DEBUG)
#
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levellevel)s - %(message)s")
#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)
#
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
