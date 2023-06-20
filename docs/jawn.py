import json

fp = open('docs/sample_instructions.json')
x = json.load(fp)
x['job']['userID'] = '1231iu23u1231nksajnasd98asnd9'
print(x)