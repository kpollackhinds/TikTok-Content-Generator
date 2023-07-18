from apiclient.discovery import build
from key import getKey

def makeRequest(input = None):
    api_key = getKey() #change this with your own api key
    youtube = build('youtube','v3',developerKey = api_key)
    request = youtube.search().list(q='Countless ')
    return



def main():
    print(type(youtube))

    return

if __name__ == "__main__":
    main()