# Makefile for Autodarts Manager
.PHONY: help install update status start stop restart logs

help:
	@echo "Autodarts Manager"
	@echo "================="
	@echo "make install  - Install autodarts"
	@echo "make update   - Update autodarts"
	@echo "make status   - Check status"
	@echo "make start    - Start service"
	@echo "make stop     - Stop service"
	@echo "make restart  - Restart service"
	@echo "make logs     - View logs"

install:
	@sudo python3 scripts/autodarts_installer.py install

update:
	@sudo python3 scripts/autodarts_installer.py update

status:
	@python3 scripts/autodarts_installer.py status

start:
	@sudo python3 scripts/autodarts_installer.py start

stop:
	@sudo python3 scripts/autodarts_installer.py stop

restart:
	@sudo python3 scripts/autodarts_installer.py restart

logs:
	@python3 scripts/autodarts_installer.py logs
