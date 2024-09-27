from database import Database
from constants import *
from tabulate import tabulate

import google.generativeai as genai
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# limits gRPC logs to errors only
os.environ['GRPC_VERBOSITY'] = 'ERROR'
# limits Google logging (used by Abseil) to warnings and errors
os.environ['GLOG_minloglevel'] = '1'
genai.configure(api_key=os.environ['API_KEY'])

# model temperature range
MIN_TEMP = 0.0
MAX_TEMP = 2.0

def generate(context=None, prompt=None, max_tokens=60, temperature=0.7):
    context = 'Any' if not context else context
    if not prompt:
        prompt = f'Please give me some encouragement (context: {context}).'

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature
        ),
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH
        }
    )
    return response.text

def subparsers(parser):
    subparsers = parser.add_subparsers(
        title='subcommands', help=f'interact with AI {POSITIVITY}', dest='action'
    )

    gen_parser = subparsers.add_parser('generate', help='Generate some positivity')
    gen_parser.add_argument('-c', '--context', default=None, help='context to embed into the prompt')
    gen_parser.add_argument('-p', '--prompt', default=None, help='prompt fed into the model')
    gen_parser.add_argument('-m', '--max-tokens', default=60, type=int, help='maximum number of tokens in the response')
    gen_parser.add_argument('-t', '--temperature', default=0.7, type=float, help=f'controls the randomness of the response (lower is more deterministic); a real value in the range [{MIN_TEMP:.1f}, {MAX_TEMP:.1f}]')

    return subparsers

def handle_cli(args):
    if args.action == 'generate':
        print(generate(context=args.context, 
                       prompt=args.prompt, 
                       max_tokens=args.max_tokens,
                       temperature=args.temperature))
   
