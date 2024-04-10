NAME 					= Ft_Transcendence

DATABASE_DIR			= ./database
DATABASE_HIDDEN_FILE	= .database_already_set

BACKEND_DIR				= ./backend
BACKEND_ENV				= ./backend/.env

FRONTEND_DIR			= ./frontend
FRONTEND_ENV			= ./frontend/.env

DOCKER_COMPOSE_FILE		= ./docker-compose.yaml

# add later '--env-file ${FRONTEND_ENV}' to DOCKER_COMPOSE below
DOCKER_COMPOSE			= docker compose \
							--env-file ${BACKEND_ENV} \
							-f ${DOCKER_COMPOSE_FILE}

# Colors
C_RESET = \033[0;39m
GREEN = \033[0;92m
YELLOW = \033[0;93m
BLUE = \033[0;94m
B_MAGENTA = \033[1;35m
CYAN = \033[0;96m

all: up

up:
	${DOCKER_COMPOSE} up --build --detach
	@echo "${GREEN}${NAME} is up!${C_RESET}"

down:
	${DOCKER_COMPOSE} down --rmi all -v
	@echo "${GREEN}${NAME} is down!${C_RESET}"

start:
	${DOCKER_COMPOSE} start
	@echo "${GREEN}${NAME} has started!${C_RESET}"

stop:
	${DOCKER_COMPOSE} stop
	@echo "${GREEN}${NAME} has stopped!${C_RESET}"

clean: down clear_database_dir

# docker system prune is probably too much, might have to make it more limited
fclean: clean
	docker system prune

clear_database_dir:
	@if [ -z "$$(ls -A ${DATABASE_DIR})" ]; then \
		rm -rf ${DATABASE_DIR}/${WORDPRESS_DATA_DIR}/*; \
		echo "${YELLOW}database directory cleared of its contents!${C_RESET}"; \
	fi

.PHONY: all up down start stop clean fclean clear_database_dir