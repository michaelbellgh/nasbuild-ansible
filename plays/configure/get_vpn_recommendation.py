
import requests, json
response = requests.get("https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations")
j = json.loads(response.content)

print(j)