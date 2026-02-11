from app import create_app

app = create_app()
with app.test_client() as client:
    response = client.get('/')
    print(f'Status: {response.status_code}')
    print(f'Content-Type: {response.content_type}')
    if response.status_code == 200:
        print(f'Data (first 500 chars): {response.data[:500]}')
    else:
        print(f'Response: {response.data.decode()}')
