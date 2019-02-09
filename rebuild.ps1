docker stop flask_container
docker build . -t flask_image
docker container prune -f
docker run --name flask_container -p 80:80 flask_image
