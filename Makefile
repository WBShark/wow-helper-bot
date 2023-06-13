proto_make:
	python -m grpc_tools.protoc -I./logfetcher/proto/ --python_out=logfetcher/proto/ --pyi_out=logfetcher/proto/ --grpc_python_out=logfetcher/proto/ logfetcher/proto/log_service.proto

	

black:
	poetry run black ./dpschecker
	poetry run black ./logfetcher


isort:
	poetry run isort ./dpschecker --profile black
	poetry run isort ./logfetcher --profile black

mypy:
	poetry run mypy ./dpschecker --no-namespace-packages
	poetry run mypy ./logfetcher --no-namespace-packages

ruff:
	poetry run ruff ./dpschecker
	poetry run ruff ./logfetcher

precommit: isort black ruff

module_run:
	poetry run python -m dpschecker

docker_bot_build:
	docker buildx build -f bot_Dockerfile -t docker.io/whitebigshark/dc-bot:latest .

docker_bot_run:
	docker run --net=host --env-file .env docker.io/whitebigshark/dc-bot:latest

docker_log_build:
	docker buildx build -f log_Dockerfile -t docker.io/whitebigshark/log-bot:latest .

docker_log_run:
	docker run --net=host --memory="3g" --env-file .env docker.io/whitebigshark/log-bot:latest 

docker_push:
	docker push docker.io/whitebigshark/dc-bot:latest
	docker push docker.io/whitebigshark/log-bot:latest

k8s_deploy:
	envsubst < charts/values.yaml | microk8s helm upgrade --install bot ./charts -f -

k8s_delete_deployment:
	microk8s kubectl delete deployment bot-dps-checker

get_pods:
	microk8s kubectl get pods

run_fetcher:
	docker run -dit --network wow-net --name logs -p 8080:8080 docker.io/whitebigshark/log-fetcher:latest