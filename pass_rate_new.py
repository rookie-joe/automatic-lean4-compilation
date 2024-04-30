import os
import subprocess
from argparse import ArgumentParser
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import glob
import tempfile

def wrapped_function(item):
    results = []
    passed = 0
    total = 0

    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, f"test.lean")

    with open(temp_file, "w") as f:
        f.write(item['cmd'])

    # Rest of the function code...
    # Process the item using the temporary file
    # ...

    # Clean up the temporary file
    data = '{"path": "%s", "allTactics": true}' %(temp_file)
    command = 'echo \'%s\' | lake exe repl' % data

    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        #         stdout = result.stdout.decode('utf-8')
        json_stdout = json.loads(stdout)
        if "messages" not in json_stdout.keys():
            passed += 1
        # results.append({'item': item['content'], 'stdout': stdout, 'stderr': stderr, 'status': 'pass'})
        results.append({ 'stdout': stdout, 'stderr': stderr, 'status': 'pass'})
    except subprocess.CalledProcessError as e:
        # results.append({'item': item['content'], 'error': str(e), 'status': 'nopass'})
        results.append({ 'error': str(e), 'status': 'nopass'})
    total += 1

    pass_rate = passed / (passed + total) * 100


    return {'results': results, 'pass_rate': pass_rate}



def multi(command_list, output_path):
    results = []
    passed = 0
    total = 0
    def execute_command(item):
        temp_dir = '/opt/jianqiao'
        temp_file = os.path.join(temp_dir, f"test_{item['index']}.lean")  # Ensure unique filenames
        with open(temp_file, "w") as f:
            f.write(item['cmd'])

        data = '{"path": "%s", "allTactics": true}' % temp_file
        command = f'echo \'{data}\' | lake exe repl'

        try:
            result = subprocess.run(command, shell=True, check=True,timeout=600,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout = result.stdout.decode('utf-8')
            stderr = result.stderr.decode('utf-8')

            if "messages" not in json.loads(stdout) and not len(stderr):
                return {'stdout': stdout, 'stderr': stderr, 'status': 'pass' , 'statement':item['statement'], 'content': item['content']}
            else:
                return {'stdout': stdout, 'stderr': stderr, 'status': 'nopass', 'statement':item['statement'] , 'content': item['content']}

        except subprocess.TimeoutExpired as e:
            return {'error': str(e), 'status': 'nopass_limit', 'statement':item['statement'], 'content': item['content']}

        except subprocess.CalledProcessError as e:
            return {'error': str(e), 'status': 'nopass_error', 'statement':item['statement'], 'content': item['content']}

        os.remove(temp_file)

    total = len(command_list)

    with ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(execute_command, {'index': i, 'cmd': cmd['cmd'], 'statement':cmd['statement'], 'content':cmd['content']}) for i, cmd in enumerate(command_list)]
        for future in tqdm(futures, total=total, desc="Processing Commands"):
            result = future.result()
            results.append(result)
            if result['status'] == 'pass':
                passed += 1

    pass_rate = (passed / total) * 100
    print(f"total test: {total}")
    print(f"Pass rate: {pass_rate}%")

    output_file = f"pass_rate_results/{output_path}"
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(f"{output_file}", 'w') as f:
        json.dump({'results': results, 'pass_rate': pass_rate}, f, indent=2, ensure_ascii=False)

import re
def remove_simp_pattern_from_end(s):
    pattern = r'@\[simp\s*.*?\]$'
    return re.sub(pattern, '', s)

def main(args):
    command_list = []
    file_pattern = os.path.join(args.input_path, '[0-9]*.json')
    for file_path in glob.glob(file_pattern):
        with open(file_path, 'r', encoding='utf-8') as rf:
            for line in rf.readlines():
                try:
                    json_item = json.loads(line)
                    json_item['cmd']  = '\n\n'.join([json_item['working_file'],   json_item['statement']])
                except:
                    import pdb
                    pdb.set_trace()
                command_list.append(json_item)
    command_list = command_list
    multi(command_list, args.output_path)

if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--input_path', type=str, default='')
    arg_parser.add_argument('--output_path', type=str, default='total.json')
    args = arg_parser.parse_args()
    main(args)



