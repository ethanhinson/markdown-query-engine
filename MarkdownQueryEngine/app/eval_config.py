import yaml
from llama_index.core  import (
    SimpleDirectoryReader,
)
from llama_index.core.llama_dataset.generator import RagDatasetGenerator
import random 
class EvalConfig:
    def __init__(self, path: str, data_path: str):
        self.path = path
        self.data_path = data_path

    def loadYaml(self):
        with open(self.path, 'r') as file:
            return yaml.safe_load(file)
        
    def question_generator_prompt(self):
        return self.loadYaml()['question_generator_prompt']
    
    def get_eval(self):
        return self.loadYaml()['eval']
    
    def get_persona(self):
        return self.get_eval()['persona']
    
    def get_question_contexts(self):
        return self.get_eval()['question_contexts']
    
    def get_questions(self):
        questions = self.get_eval()['questions']
        if questions:
            return questions
        else:
            return self.generate_eval_questions()
    
    def generate_eval_questions(self):
        documents = SimpleDirectoryReader(
            input_dir=self.data_file_path,
            recursive=True,
            required_exts=[".md", ".mdx"]
        ).load_data()
        eval_documents = [documents[random.randint(0, len(documents)-1)] for _ in range(10)]

        eval_questions_all = []
        num_questions_per_chunk = 1

        data_generator = RagDatasetGenerator.from_documents(eval_documents, question_gen_query=self.format_question_generator_prompt(num_questions_per_chunk))
        eval_questions = data_generator.generate_questions_from_nodes()
        eval_questions_all.append(eval_questions.to_pandas()['query'].to_list())

        questions = eval_questions.to_pandas()['query'].to_list() 
        print(questions)

        return questions
    
    def format_question_generator_prompt(self, num_questions_per_chunk = 1):
        question_contexts = self.get_question_contexts()
        list_of_contexts = []
        for context in question_contexts:
            list_of_contexts.append(context)
        return f"{self.get_persona()} \
                Your task is to setup {num_questions_per_chunk} questions. \
                The questions must be related to following \
                {list_of_contexts.join('\n')} \
                Restrict the questions to the context information provided."
                
    def eval_questions(self):
        if self.loadYaml()['eval_questions']:
            return self.loadYaml()['eval_questions']
        else:
            return self.generate_eval_questions()
    