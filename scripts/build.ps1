docker build -f docker/Dockerfile -t flask-k8s-app:v1 ..
minikube image load flask-k8s-app:v1
Write-Host "Image built and loaded into Minikube"