import requests

def get_puzzle_data(puzzle_id):
    api_url = f"https://lichess.org/api/puzzle/{puzzle_id}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        puzzle_data = response.json()
        return puzzle_data

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

# Replace 'your_puzzle_id' with the actual puzzle ID you want to retrieve
puzzle_id_to_fetch = '0128O'
puzzle_data = get_puzzle_data(puzzle_id_to_fetch)

if puzzle_data:
    print("Puzzle Data:")
    print(puzzle_data)
else:
    print("Failed to retrieve puzzle data.")