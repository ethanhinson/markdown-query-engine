from MarkdownQueryEngine.app.config import AppConfig
from llama_index.core import Settings

config = AppConfig()

Settings.llm = config.get_llm()
Settings.embed_model = config.get_embed_model()

from MarkdownQueryEngine.app.query import query
from llama_index.core  import (
    SimpleDirectoryReader,
)
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator
)

import nest_asyncio
import random 
import time

nest_asyncio.apply()

def evaluate_response_time_and_accuracy(chunk_size, eval_questions, faithfulness_evaluator, relevancy_evaluator):
    total_response_time = 0
    total_faithfulness = 0
    total_relevancy = 0

    response_vectors = []
    Settings.chunk_size = chunk_size
    Settings.chunk_overlap = round(chunk_size/10,0)

    num_questions = len(eval_questions)

    for question in eval_questions:
        start_time = time.time() 
        response_vector = query(question)
        elapsed_time = time.time() - start_time
        faithfulness_result = faithfulness_evaluator.evaluate_response( response=response_vector ).passing
        relevancy_result = relevancy_evaluator.evaluate_response( query=question, response=response_vector ).passing
        response_vectors.append({"chunk_size" : chunk_size,
                                 "question" : question,
                                 "response_vector" : response_vector,
                                 "faithfulness_result" : faithfulness_result,
                                 "relevancy_result" : relevancy_result})

        total_response_time += elapsed_time
        total_faithfulness += faithfulness_result
        total_relevancy += relevancy_result
    
    # Get average score over all questions
    average_response_time = total_response_time / num_questions
    average_faithfulness = total_faithfulness / num_questions
    average_relevancy = total_relevancy / num_questions

    return average_response_time, average_faithfulness, average_relevancy, response_vectors

def generate_eval_questions(config: AppConfig):
    documents = SimpleDirectoryReader(
        input_dir=config.data_file_path,
        recursive=True,
        required_exts=[".md", ".mdx"]
    ).load_data()
    eval_documents = [documents[random.randint(0, len(documents)-1)] for _ in range(10)]

    eval_questions_all = []
    num_questions_per_chunk = 1

    q_gen_query = f"You are a senior software engineer who is an expert in Node.js. \
            Your task is to setup {num_questions_per_chunk} questions. \
            The questions must be related to following \
            1. Managing monorepos with Nx. 2. Optimizing build times with Nx. 3. General Nx questions \
            Restrict the questions to the context information provided."
    data_generator = RagDatasetGenerator.from_documents(eval_documents, question_gen_query=q_gen_query)
    eval_questions = data_generator.generate_questions_from_nodes()
    eval_questions_all.append(eval_questions.to_pandas()['query'].to_list())

    questions = eval_questions.to_pandas()['query'].to_list() 
    print(questions)

    return questions

if __name__ == "__main__":
    config = AppConfig()
    questions = generate_eval_questions(config)
    faithfulness = FaithfulnessEvaluator()
    relevancy = RelevancyEvaluator()
    response_vectors_all = []
    for chunk_size in [128, 256, 512, 1024, 2048]:
        avg_time, avg_faithfulness, avg_relevancy, response_vectors = evaluate_response_time_and_accuracy(chunk_size, questions, faithfulness, relevancy)
        [response_vectors_all.append(i) for i in response_vectors]
        print(f"Chunk size {chunk_size} - Average Response time: {avg_time:.2f}s, Average Faithfulness: {avg_faithfulness:.2f}, Average Relevancy: {avg_relevancy:.2f}")
        time.sleep(20)
