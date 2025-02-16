import urllib2
import json
from ghidra.program.model.listing import Function
from ghidra.util.task import ConsoleTaskMonitor
import threading

BASE_URL = "https://puter.com"
API_URL = "https://api.puter.com"
signup_payload = {
    "referrer": "http://127.0.0.1:5500/",
    "is_temp": True
}
signup_headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Origin": BASE_URL,
    "Referer": BASE_URL + "/?embedded_in_popup=true&request_auth=true",
}
def post_request(url, payload, headers):
    try:
        req = urllib2.Request(url, json.dumps(payload))
        for key, value in headers.items():
            req.add_header(key, value)
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as e:
        print("HTTP Error: {} - {}".format(e.code, e.reason))
    except urllib2.URLError as e:
        print("URL Error: {}".format(e.reason))
    except Exception as e:
        print("Unexpected error: {}".format(str(e)))
    return None
def create_new_session():
    response = post_request(BASE_URL + "/signup", signup_payload, signup_headers)
    if not response or "token" not in response:
        print("Signup failed!", response)
        exit()
    token = response["token"]
    app_token_payload = {"origin": "http://127.0.0.1:5500"}
    app_token_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "User-Agent": signup_headers["User-Agent"],
        "Origin": BASE_URL,
        "Referer": BASE_URL + "/",
    }
    response = post_request(API_URL + "/auth/get-user-app-token", app_token_payload, app_token_headers)
    if not response or "token" not in response:
        print("App token request failed!", response)
        exit()
    
    return response["token"]
new_token = create_new_session()
def ai_response(maincode):
    call_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Bearer " + new_token,
        "User-Agent": signup_headers["User-Agent"],
        "Origin": "http://127.0.0.1:5500",
        "Referer": "http://127.0.0.1:5500/",
    }
    main_prompt = ("Rewrite the function and respond only with code, no explanation, no markdown. "
                   "Change 'goto' into if/else/for where possible, use better variable names, "
                   "remove dead code, take function arguments and strings from comments like 'string:', "
                   "transform this pseudocode into C.")
    call_payload = {
        "interface": "puter-chat-completion",
        "driver": "claude",
        "test_mode": False,
        "method": "complete",
        "args": {
            "messages": [{"content": main_prompt + " " + maincode}],
            "model": "claude-3-5-sonnet-latest"
        }
    }
    response = post_request(API_URL + "/drivers/call", call_payload, call_headers)
    if response and "result" in response and "message" in response["result"]:
        text_content = response['result']['message']['content'][0]['text']
        return text_content.replace('```c', '').replace('```', '').strip()
    return None
program = getCurrentProgram()
function_manager = program.getFunctionManager()
all_functions = list(function_manager.getFunctions(True))
def process_function(function):
    print("Processing Function: {}".format(function.getName()))
    listing = program.getListing()
    code_units = listing.getCodeUnits(function.getBody(), True)
    
    function_code = "\n".join(str(code_unit) for code_unit in code_units)
    ai_response_text = ai_response(function_code)
    separator = "\n==============================================\n"
    new_comment = separator + ai_response_text + separator
    function.setComment(new_comment)    
threads = []
for function in all_functions:
    if len(threads) >= 10:
        for t in threads:
            t.join()
        threads = []
    thread = threading.Thread(target=process_function, args=(function,))
    thread.start()
    threads.append(thread)
for t in threads:
    t.join()
print("All functions processed with AI!!")
