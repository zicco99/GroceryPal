echo "server will start on localhost:5001"
docker build -t grocerypalserver . 

echo "------------------------------------"
echo "server will start on localhost:5001"
echo "------------------------------------"
docker run -p 5001:80 grocerypalserver

