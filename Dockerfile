###############################################################################
# Builder Stage: Code kopieren, Submodule aktualisieren, Wheel bauen
###############################################################################
FROM cgr.dev/chainguard/wolfi-base AS builder
ARG PYVERSION=3.12
ARG GUNICORN==23.0.0
ARG PSYCOPG2==2.9.9
ARG PI_VERSION=3.11dev2

# Grundlegende Umgebungsvariablen
ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/privacyidea/venv/bin:$PATH"

# Installiere Python, pip, Build-Tools und Git
RUN apk add --no-cache python-${PYVERSION} py${PYVERSION}-pip build-base git

WORKDIR /privacyidea

# Anstatt hier den Repo per "git clone" zu holen, 
# wird davon ausgegangen, dass der Repository-Inhalt (inkl. .git) bereits
# als Build-Kontext vorliegt.
COPY . /privacyidea

# Damit Git das Arbeitsverzeichnis als sicher einstuft
##RUN git config --global --add safe.directory '*'

# Aktualisiere die Submodule, damit auch z. B. der Webauthn-Client vorhanden ist
#RUN git submodule update --recursive --init

# Erstelle ein Virtualenv und installiere Build-Tools
RUN python3 -m venv /privacyidea/venv && \
    /privacyidea/venv/bin/pip install --upgrade pip && \
    /privacyidea/venv/bin/pip install build

# Erstelle einen symbolischen Link für das Webauthn‑Submodul,
# falls erforderlich (das Submodul liegt z. B. unter static/contrib/js/webauthn-client)
## RUN ln -s /privacyidea/static/contrib/js/webauthn-client /privacyidea/webauthn

# Baue das privacyIDEA‑Paket als Wheel (ohne externe PyPI‑Abhängigkeiten)
RUN /privacyidea/venv/bin/python -m build --wheel --outdir /privacyidea/dist

# Installiere das gebaute Wheel und weitere Runtime-Abhängigkeiten
RUN /privacyidea/venv/bin/pip install --find-links=/privacyidea/dist /privacyidea/dist/*.whl && \
    /privacyidea/venv/bin/pip install psycopg2-binary==${PSYCOPG2} gunicorn==${GUNICORN}

# Kopiere Konfigurationsdateien und Skripte in das Image
COPY deploy/docker/entrypoint.sh /privacyidea/venv/bin/entrypoint.sh
COPY deploy/docker/healthcheck.py /privacyidea/venv/bin/healthcheck.py
COPY deploy/docker/pi.cfg /privacyidea/etc/pi.cfg
COPY deploy/docker/logging.cfg /privacyidea/etc/logging.cfg

###############################################################################
# Final Stage: Schlankes Runtime‑Image – nur benötigte Dateien übernehmen
###############################################################################
FROM cgr.dev/chainguard/wolfi-base
ARG PYVERSION=3.12

# Laufzeit‑Einstellungen
ENV PYTHONUNBUFFERED=1 \
    PATH="/privacyidea/venv/bin:/privacyidea/bin:$PATH" \
    PRIVACYIDEA_CONFIGFILE="/privacyidea/etc/pi.cfg" \
    PYTHONPATH=/privacyidea

WORKDIR /privacyidea
VOLUME /privacyidea/etc/persistent

# Installiere den Python-Interpreter (ohne Build‑Tools)
RUN apk add --no-cache python-${PYVERSION}

# Kopiere nur die für den Runtime-Betrieb benötigten Verzeichnisse aus der Builder Stage:
# - Das Virtualenv (enthält das installierte privacyIDEA‑Paket und zugehörige Skripte)
# - Die Konfigurationsdateien
# - Den Webauthn-Ordner (falls vom Package benötigt)
COPY --from=builder /privacyidea/venv /privacyidea/venv
COPY --from=builder /privacyidea/etc /privacyidea/etc
#COPY --from=builder /privacyidea/webauthn /privacyidea/webauthn

# Exponiere den Port (Variable PORT sollte beim Build oder Laufzeit gesetzt werden)
EXPOSE ${PORT}

# Starte den privacyIDEA‑Server über das EntryPoint-Skript
ENTRYPOINT ["entrypoint.sh"]

