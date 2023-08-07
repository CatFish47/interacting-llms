from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class AgentGodel:
    def __init__(self, instruction):
        """Constructor method that initializes the Godel agent

        Parameters
        ----------
            instruction : str
                instructions for how the agent should respond
        """

        self.tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/GODEL-v1_1-large-seq2seq")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "microsoft/GODEL-v1_1-large-seq2seq")
        self.context = []
        self.knowledge = ""
        self.instruction = instruction

    def set_instruction(self, instruction):
        """Sets the instruction for Godel

        Parameters
        ----------
            instruction : str
                instructions for how the agent should respond
        """

        self.instruction = instruction

    def prompt(self, question, knowledge=None):
        """Prompts the agent

        Parameters
        ----------
            question : str
                the user prompt for the agent
            knowledge : str
                any relevant knowledge to answer the question

        Returns
        -------
        str
            the response of the agent
        """

        self.context.append(question)
        if knowledge is not None:
            self.knowledge = knowledge

        if self.knowledge != '':
            knowledge = '[KNOWLEDGE] ' + knowledge
        dialog = ' EOS '.join(self.context)
        query = f"{self.instruction} [CONTEXT] {dialog} {knowledge}"
        input_ids = self.tokenizer(f"{query}", return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids, max_length=128,
                                      min_length=8, top_p=0.9, do_sample=True)
        output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        self.context.append(output)

        return output

    def clear_context(self):
        """Clears the context"""

        self.context = []
