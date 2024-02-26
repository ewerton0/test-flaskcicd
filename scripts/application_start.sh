echo "Running container..."
docker run --name flask_app -d -p 5000:5000 156769710368.dkr.ecr.us-east-1.amazonaws.com/flask_image:latest