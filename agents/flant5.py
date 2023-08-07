from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class AgentFlan:
    def __init__(self):
        """Constructor method that initializes the Flan T5 agent."""

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-large")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")

    def raw_prompt(self, question, max_len=50):
        """Prompts the agent without formatting

        Parameters
        ----------
            question : str
                the user prompt for the agent
        """

        inputs = self.tokenizer(question, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=max_len)
        output = self.tokenizer.batch_decode(
            outputs, skip_special_tokens=True)[0]

        return output

    def prompt(self, question, context):
        """Prompts the agent

        Parameters
        ----------
            question : str
                the user prompt for the agent
            context : str
                any relevant context to answer the question

        Returns
        -------
        str
            the response of the agent
        """

        parsed_in = f"Question: {question} Context: {context}"
        return self.raw_prompt(parsed_in)
