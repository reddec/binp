all: generate-api

bin/swagger.jar:
	mkdir -p bin
	wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/5.0.0/openapi-generator-cli-5.0.0.jar -O bin/swagger.jar

generate-api: bin/swagger.jar
	rm -rf src/api/internal/*
	mkdir -p src/api/internal
	java -jar bin/swagger.jar generate -g typescript-fetch --additional-properties=typescriptThreePlus=true -o src/api/internal -i  http://127.0.0.1:8000/internal/openapi.json