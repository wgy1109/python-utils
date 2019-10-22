import oauth2 as oauth

# Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key="55d9929d-2e1f-46d8-97cd-cede98933044",
                          secret="client_secret")

# Request token URL for Twitter.
request_token_url = "http://openapi.avcp.idriverplus.com/api-auth/oauth/token"

# Create our client.
client = oauth.Client(consumer)

# The OAuth Client request works just like httplib2 for the most part.
resp, content = client.request(request_token_url, "GET")
print(resp)
print(content)

