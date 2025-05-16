import os
import re
import time
import random
import requests
import subprocess

model = "llama3"

def main():

    while True:

        url, lines = fetch_web()
        line = random.choice(lines)

        print()
        slow_print(" Fetched from\n  " + url)
        print()

        slow_print(" Translate this sentence:\n" + word_wrap(line))

        # =================================================================
        
        prompt = f"""
        Give me the translation of this into English: {line}.
        Just give the answer. I don't want any long comments.
        If there are any proper nouns, leave them in the sentence.
        Keep the structure of the sentence the same.
        This is for my translation practice.
        Your answer:
        """
        result, _ = ask(prompt)
        
        # =================================================================
        
        answer = input("\n Press ENTER to see the translation...").strip()
        print()

        slow_print(f" {model}'s translation:\n" + word_wrap(result))
        print()

        answer = input("\n Type 'exit' to stop,\n or anything else to continue: ").strip()
        print()

        if answer=='exit':
            exit()
        else :
            print("-"*64)

def fetch_web():
    # Path to the folder containing .dat files
    folder_path = os.path.join(os.path.dirname(__file__), 'novel_data')

    # Get all .dat files in the folder
    dat_files = [f for f in os.listdir(folder_path) if f.endswith('.dat')]

    if not dat_files:
        print("No .dat files found in 'novel_data' folder.")
        exit()

    # Pick a random .dat file
    chosen_file = random.choice(dat_files)
    file_base = os.path.splitext(chosen_file)[0]

    # Read the number n from the file
    file_path = os.path.join(folder_path, chosen_file)
    try:
        with open(file_path, 'r') as f:
            n = int(f.read().strip())
    except ValueError:
        print(f"Invalid number in file: {chosen_file}")
        exit()

    # Check if chapter n+1 exists
    next_url = f'https://ncode.syosetu.com/{file_base}/{n + 1}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.212 Safari/537.36'
    }

    try:
        response = requests.head(next_url, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            # Chapter n+1 exists; update the file
            n += 1
            with open(file_path, 'w') as f:
                f.write(str(n))
    except requests.exceptions.RequestException:
        pass  # If the request fails, just continue with existing `n`

    # Pick a random number i between 1 and n
    i = random.randint(1, n)

    # Construct the URL
    url = f'https://ncode.syosetu.com/{file_base}/{i}/'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        html = html.replace("<br />", "")
        html = replace_ruby_tags(html)
        matches = re.findall(r'<p id="L\d+">(.*?)</p>', html, re.DOTALL)
        lines = [match.strip() for match in matches]
        lines = split_japanese_sentences(lines)
        return url, lines
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        exit()

def split_japanese_sentences(lines):

    exception_brackets = [
        ("「", "」"),  # Japanese corner brackets
        ("『", "』"),  # Double corner brackets
        ("（", "）"),  # Full-width parentheses
        ("(", ")"),    # Half-width parentheses
        ("【", "】"),  # Black lenticular brackets
        ("［", "］"),  # Full-width square brackets
        ("[", "]"),    # Half-width square brackets
        ("〈", "〉"),  # Single angle brackets
        ("《", "》"),  # Double angle brackets
        ("｛", "｝"),  # Full-width curly brackets
        ("{", "}"),    # Half-width curly brackets
        ("＜", "＞"),  # Full-width less-than/greater-than
        ("<", ">"),    # Half-width angle brackets
        ("“", "”"),    # Curly double quotes
        ("‘", "’"),    # Curly single quotes
        ('"', '"'),    # Straight double quotes (English)
        ("'", "'"),    # Straight single quotes (English)
    ]



    split_lines = []

    # Create a mapping for opening and closing brackets
    open_to_close = {op: cl for op, cl in exception_brackets}
    close_to_open = {cl: op for op, cl in exception_brackets}
    open_set = set(open_to_close.keys())
    close_set = set(close_to_open.keys())

    for line in lines:
        buffer = ""
        stack = []
        for char in line:
            if char in open_set:
                stack.append(open_to_close[char])
            elif char in close_set:
                if stack and stack[-1] == char:
                    stack.pop()

            buffer += char

            # Split only if outside brackets
            if char == "。" and not stack:
                split_lines.append(buffer)
                buffer = ""

        # Add any remaining content
        if buffer:
            split_lines.append(buffer)

    return split_lines

def replace_ruby_tags(text):
    # Regex pattern to match ruby tags with reading
    pattern = re.compile(
        r'<ruby>(.*?)<rp>\(</rp><rt>(.*?)</rt><rp>\)</rp></ruby>',
        re.DOTALL
    )

    # Replace with "base[reading]" format
    return pattern.sub(r'\1[\2]', text)

def ask(prompt):
    command = f'ollama run {model} "{prompt}"'
    result = subprocess.run(command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True)
    output = result.stdout.strip(' \n')
    error = result.stderr
    return output, error

def slow_print(text, interval=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(interval)
    print()

def word_wrap(text, width=64):
    line_start = '    │ '
    ret = ""
    iblock = 0
    nblock = len(text.split("\n"))
    for block in text.split("\n"):
        lines = []
        words = block.split()
        current_line = []

        for word in words:
            # Check if adding this word exceeds the specified width
            if len(' '.join(current_line + [word])) <= width:
                current_line.append(word)
            else:
                # Join the current line into a string and add it to the lines list
                lines.append(' '.join(current_line))
                # Start a new line with the current word
                current_line = [word]

        # Add the last line if there's any leftover text
        if current_line:
            lines.append(' '.join(current_line))

        # Create the box around the text
        box_width = width + 2  # Add 2 for the border padding
        lines_with_border = []  # Top border

        for line in lines:
            lines_with_border.append(line_start + line.ljust(width))
        ret += '\n'.join(lines_with_border)
        if iblock<nblock-1:
            ret += "\n"+line_start
        iblock += 1
    while (line_start+line_start) in ret:
        ret = ret.replace(line_start+line_start,line_start)
    return ret

main()