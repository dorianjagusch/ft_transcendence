NAME 					= Ft_Transcendence

BACKEND_DIR				= ./backend
BACKEND_ENV				= ./backend/.env

FRONTEND_DIR			= ./frontend
FRONTEND_ENV			= ./frontend/.env

DOCKER_COMPOSE_FILE		= ./docker-compose.yaml
DOCKER_COMPOSE_PROD_FILE= ./production.yaml

# add later '--env-file ${FRONTEND_ENV}' to DOCKER_COMPOSE below
DOCKER_COMPOSE			= docker compose \
							--env-file ${BACKEND_ENV} \
							-f ${DOCKER_COMPOSE_FILE}
DOCKER_COMPOSE_PROD		= docker compose \
							--env-file ${BACKEND_ENV} \
							-f ${DOCKER_COMPOSE_PROD_FILE}

# Colors
C_RESET = \033[0;39m
GREEN = \033[0;92m
YELLOW = \033[0;93m
BLUE = \033[0;94m
B_MAGENTA = \033[1;35m
CYAN = \033[0;96m

all: up

up:
	sudo ${DOCKER_COMPOSE} up --build --detach
	@echo "${GREEN}${NAME} is up!${C_RESET}"

prod:
	${DOCKER_COMPOSE_PROD} up --build --detach
	@echo "${GREEN}${NAME} deployed to production!${C_RESET}"

start:
	${DOCKER_COMPOSE} start
	@echo "${GREEN}${NAME} has started!${C_RESET}"

stop:
	${DOCKER_COMPOSE} stop
	@echo "${GREEN}${NAME} has stopped!${C_RESET}"

clean: stop
	sudo ${DOCKER_COMPOSE} down -v
	@echo "${GREEN}${NAME} has been cleaned!${C_RESET}"

fclean: clean
	${DOCKER_COMPOSE} down --rmi all --volumes --remove-orphans
	python3 ./clear_migrations.py

re: fclean all

.PHONY: all up down start stop clean fclean
