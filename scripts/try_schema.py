from pydantic import ValidationError

from easy_leaflet.schema import parse_llm_output

good = '{"found": true, "answer": "Não beba álcool.", "excerpts": [1]}'
with_fences = '```json\n{"found": false, "answer": "Não encontrei.", "excerpts": []}\n```'
broken = '{"found": "talvez", "answer": "Não sei."}'

print(parse_llm_output(good))
print(parse_llm_output(with_fences))

try:
    parse_llm_output(broken)
except ValidationError as error:
    print("BROKEN ANSWER WAS REJECTED:")
    print(error)