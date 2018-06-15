import json

def transfer(fileIn,fileOut):
    with open(fileOut, 'r+') as f:
        obj = json.load(f)
        results = obj['results']
        with open(fileIn,'r') as oldf:
            for line in oldf.readlines():
                results.append(json.loads(line))
        obj['results'] = results
        f.close()
    f = open(fileOut,'w')
    json.dump(obj,f)

if __name__ == "__main__":
    convert('results.jsonl','results.json')
