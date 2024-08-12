from database import Database
from constants import *
from tabulate import tabulate
from argparse import BooleanOptionalAction

import openai
openai.api_key = '''sk-svcacct-as8gPXUSIwsqZL9_AitrCHCSo623SLy-sUkm_85rD_cIC5wkST3BlbkFJXcAyZkYxGm5if3drq7Ch4eB9yrgSHpiR7nLzhibEU7u3ZNVLQA
'''


def generate(theme=None, prompt=None, model='gpt-4', max_tokens=60, temperature=0.7):
    theme = 'Any' if not theme else theme
    if not prompt:
        prompt = 'Give me some encouragement (theme: {theme}).'
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'system', 
            'content': 'You are a helpful assistant that generates positive words and sentences.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature  # Controls the randomness; lower is more deterministic
    )
    print(response)
    return response['choices'][0]['message']['content'].strip()


def subparsers(parser):
    subparsers = parser.add_subparsers(
        title='subcommands', help='interact with {POSITIVE_WORDS} based on chatgpt', dest='action'
    )

    gen_parser = subparsers.add_parser('generate', help='Generate some positivity')
    gen_parser.add_argument('-t', '--theme', default=None, help='theme of the positive words')
    gen_parser.add_argument('-p', '--prompt', default=None, help='prompt fed into the model')
    gen_parser.add_argument('-m', '--model', default='gpt-4', help='model queried')
    gen_parser.add_argument('-max', '--max-tokens', default=60, help='maximum number of tokens in the response')
    gen_parser.add_argument('-tmp', '--temperature', default=0.7, help='controls the randomness of the response (lower is more deterministic), a value in [0,1]')

    return subparsers

def handle_cli(args):
    if args.action == 'generate':
        print(generate(theme=args.theme, prompt=args.prompt, 
                       model=args.model, max_tokens=args.max_tokens,
                       temperature=args.temperature))
   
