import requests
import os

def download_repo(username, download_path):
    # Construct the API URL to fetch user's repositories
    url = f"https://api.github.com/users/{username}/repos"

    # Make a GET request to the GitHub API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        repositories = response.json()

        # Create a folder for the downloaded repositories
        user_folder_path = os.path.join(download_path, username)
        os.makedirs(user_folder_path, exist_ok=True)

        # Iterate over each repository and download it
        for repo in repositories:
            repo_name = repo["name"]
            repo_url = repo["html_url"]
            print(f"Downloading repository '{repo_name}'...")

            # Construct the direct zip download URL
            zip_url = f"https://codeload.github.com/{username}/{repo_name}/zip/refs/heads/main"

            # Make a GET request to download the zip file
            zip_response = requests.get(zip_url)

            # Check if the request was successful
            if zip_response.status_code == 200:
                # Write the content to a zip file
                zip_path = os.path.join(user_folder_path, f"{repo_name}.zip")
                with open(zip_path, 'wb') as f:
                    f.write(zip_response.content)
            
                print(f"Repository '{repo_name}' downloaded successfully at '{zip_path}'")
            else:
                print(f"Failed to download repository '{repo_name}'. Status code: {zip_response.status_code}")

        # Check for pagination
        while 'next' in response.links:
            next_page_url = response.links['next']['url']
            response = requests.get(next_page_url)
            repositories = response.json()

            for repo in repositories:
                repo_name = repo["name"]
                repo_url = repo["html_url"]
                print(f"Downloading repository '{repo_name}'...")

                # Construct the direct zip download URL
                zip_url = f"https://codeload.github.com/{username}/{repo_name}/zip/refs/heads/main"

                # Make a GET request to download the zip file
                zip_response = requests.get(zip_url)

                # Check if the request was successful
                if zip_response.status_code == 200:
                    # Write the content to a zip file
                    zip_path = os.path.join(user_folder_path, f"{repo_name}.zip")
                    with open(zip_path, 'wb') as f:
                        f.write(zip_response.content)
                
                    print(f"Repository '{repo_name}' downloaded successfully at '{zip_path}'")
                else:
                    print(f"Failed to download repository '{repo_name}'. Status code: {zip_response.status_code}")

    else:
        print(f"Failed to fetch repositories for user '{username}'. Status code: {response.status_code}")

if __name__ == "__main__":
    # Provide the GitHub username
    github_username = input("Enter the GitHub username: ")

    # Provide the path where you want to save the downloaded repositories
    download_path = input("Enter the path where you want to save the repositories (press Enter for current directory): ")
    if download_path == "":
        download_path = "."

    download_repo(github_username, download_path)
