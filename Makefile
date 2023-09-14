proto_make:
	python -m grpc_tools.protoc -I./logfetcher/proto/ --python_out=logfetcher/proto/ --pyi_out=logfetcher/proto/ --grpc_python_out=logfetcher/proto/ logfetcher/proto/log_service.proto

	

black:
	poetry run black ./dcbot
	poetry run black ./logfetcher
	poetry run black ./logapp


isort:
	poetry run isort ./dcbot --profile black
	poetry run isort ./logfetcher --profile black
	poetry run isort ./logapp --profile black

mypy:
	poetry run mypy ./dcbot --no-namespace-packages
	poetry run mypy ./logfetcher --no-namespace-packages
	poetry run mypy ./logapp --no-namespace-packages

ruff:
	poetry run ruff ./dcbot
	poetry run ruff ./logfetcher
	poetry run ruff ./logapp

precommit: isort black ruff

module_run:
	poetry run python -m dcbot

app_run:
	uvicorn logapp.app:app --reload --access-log

docker_bot_build:
	docker buildx build -f bot_Dockerfile -t docker.io/whitebigshark/dcbot:latest .

docker_bot_run:
	docker run --net=host --env-file .env docker.io/whitebigshark/dcbot:latest

docker_log_build:
	docker buildx build -f log_Dockerfile -t docker.io/whitebigshark/log-bot:latest .

docker_log_run:
	docker run --net=host --env-file .env docker.io/whitebigshark/log-bot:latest

docker_app_build:
	docker buildx build -f app_Dockerfile -t docker.io/whitebigshark/log-app:latest .

docker_app_run:
	docker run --net=host --env-file .env docker.io/whitebigshark/log-app:latest

docker_crawler_build:
	docker buildx build -f crawler_Dockerfile -t docker.io/whitebigshark/crawler-server:latest .

docker_crawler_run:
	docker run --net=host --env-file .env docker.io/whitebigshark/crawler-server:latest  

docker_push:
	docker push docker.io/whitebigshark/dcbot:latest
	docker push docker.io/whitebigshark/log-bot:latest
	docker push docker.io/whitebigshark/log-app:latest

k8s_deploy:
	envsubst < charts/values.yaml | microk8s helm upgrade --install bot ./charts -f -

k8s_delete_deployment:
	microk8s kubectl delete deployment bot-dps-checker

get_pods:
	microk8s kubectl get pods

run_fetcher:
	docker run -dit --network wow-net --name logs -p 8080:8080 docker.io/whitebigshark/log-fetcher:latest

all_services:
	docker run --net=host --env-file .env docker.io/whitebigshark/crawler-server:latest  &> crawler-log &
	docker run --net=host --env-file .env docker.io/whitebigshark/app-server:latest  &> app-log &
	docker run --net=host --env-file .env docker.io/whitebigshark/dc-bot:latest  &> bot-log &
	docker run --net=host --env-file .env docker.io/whitebigshark/log-server:latest  &> log-log &