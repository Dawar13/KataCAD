.PHONY: setup dev lint clean check-health api-only web-only

setup:
	pnpm install
	cd apps/api && python3.11 -m venv .venv && \
		. .venv/bin/activate && pip install --upgrade pip && pip install -e ".[dev]"

dev:
	docker compose up -d api
	pnpm --filter web dev

api-only:
	docker compose up api

web-only:
	pnpm --filter web dev

lint:
	pnpm --parallel --filter web lint
	cd apps/api && . .venv/bin/activate && ruff check . && black --check .

clean:
	docker compose down -v
	rm -rf apps/web/.next apps/web/node_modules
	rm -rf apps/api/.venv apps/api/__pycache__
	rm -rf node_modules

check-health:
	./scripts/check-health.sh
