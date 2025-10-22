# ==========================================
# CONFIGURACIÓN
# ==========================================
CONTAINER_NAME = mysql-babycare
MYSQL_ROOT_PASSWORD = root123
MYSQL_DATABASE = babycare
MYSQL_IMAGE = mysql:8.0
MYSQL_PORT = 3306
SQL_FILE = database/setup_mysql.sql

# ==========================================
# TAREAS
# ==========================================

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


# Levantar el contenedor MySQL
run:
	@echo "🚀 Iniciando contenedor MySQL..."
	docker run --name $(CONTAINER_NAME) \
		-e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
		-e MYSQL_DATABASE=$(MYSQL_DATABASE) \
		-p $(MYSQL_PORT):3306 \
		-d $(MYSQL_IMAGE)
	@echo "⏳ Esperando a que el contenedor esté listo..."
	sleep 20
	@echo "✅ Contenedor $(CONTAINER_NAME) iniciado."

# Crear la base de datos dentro del contenedor
db-setup:
	@echo "📦 Cargando el script SQL dentro del contenedor..."
	docker cp $(SQL_FILE) $(CONTAINER_NAME):/setup.sql
	@echo "🛠️  Ejecutando script de creación de base de datos..."
	docker exec -i $(CONTAINER_NAME) sh -c "mysql -u root -p$(MYSQL_ROOT_PASSWORD) $(MYSQL_DATABASE) < /setup.sql"
	@echo "✅ Base de datos creada y configurada."

# Ejecuta todo: contenedor + script de base de datos
setup: requirements run db-setup
	@echo "🎉 Entorno backend configurado con éxito."

# Conectarse al contenedor MySQL
connect:
	@echo "🔗 Conectando a la base de datos dentro del contenedor..."
	docker exec -it $(CONTAINER_NAME) mysql -u root -p$(MYSQL_ROOT_PASSWORD) $(MYSQL_DATABASE)

# Mostrar estado del contenedor
status:
	@echo "🔍 Estado del contenedor:"
	docker ps -a | grep $(CONTAINER_NAME) || echo "⚠️  No hay contenedor MySQL corriendo."

# Detener contenedor sin eliminar
stop:
	@echo "🛑 Deteniendo contenedor..."
	docker stop $(CONTAINER_NAME)
	@echo "✅ Contenedor detenido."

# Eliminar completamente el contenedor
clean:
	@echo "🧹 Eliminando contenedor y datos..."
	docker rm -f $(CONTAINER_NAME)
	@echo "✅ Contenedor eliminado."

## Lint using flake8
lint:
	flake8 webservice


.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
