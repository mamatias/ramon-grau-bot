from transformers import AutoTokenizer, AutoModelWithLMHead, AutoModelForCausalLM

class generador:
    def __init__(self, modelName='datificate/gpt2-small-spanish') -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        # self.model = AutoModelWithLMHead.from_pretrained(modelName)
        self.model = AutoModelForCausalLM.from_pretrained(modelName)
        
    def generarTexto(self, prompt='Hola loco lindo, planteó feliz'):
        inputs = self.tokenizer(prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]
        # outputs = self.model.generate(input_ids=inputs, num_beams=5, num_return_sequences=3, max_length=200)
        outputs = self.model.generate(inputs, max_length=150, do_sample=True, top_p=0.95, top_k=60)
        return self.tokenizer.batch_decode(outputs, skip_special_tokens=True)


def main():
    print('\n\nPrueba local de la librería\n\n')
    Gen = generador()
    texto = Gen.generarTexto()

    print('\n\n'+texto[0])

if __name__ == '__main__':
    main()