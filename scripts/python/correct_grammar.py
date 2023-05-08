import openai
import argparse

openai.api_key = ""

def main():
    parser = argparse.ArgumentParser(description="Fix the grammar using ChatGPT")
    parser.add_argument("sentence", type=ascii, help="Sentence to be corrected")
    parser.add_argument('-v', '--version', type=int, choices=[3, 4], default=3)
    args = parser.parse_args()
    v = 'gpt-3.5-turbo' if args.version == 3 else 'gpt-4'
    correct_grammar(args.sentence, v)

def correct_grammar(sentence, model):
    print("Fixing grammar for:\n", sentence)
    prompt = f"Correct the grammar for this sentence, no need to rewrite, just fix the grammar and output the correct version: {sentence}"
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    message = f"{completion.choices[0].message.content}"
    print(f"Correct version (using model {model}):")
    print(message)

if __name__ == '__main__':
    main()