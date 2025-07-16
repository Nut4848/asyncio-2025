import requests

url = "https://pokeapi.co/api/v2/pokemon/pikachu"
response = requests.get(url)

data = response.json()

print("Name:",data["name"])
print("ID:",data["id"])
print("Height:",data["height"])
print("Weight:",data["weight"])
print("Types:",[t["type"] ["name"] for t in data ["types"]])