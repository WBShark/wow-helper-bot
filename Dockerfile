FROM python:3.11.2
ARG USERNAME=potya

ENV LANG "C.UTF-8"

ENV POETRY_VERSION 1.4.0

RUN set -ex; pip install --no-cache-dir poetry==$POETRY_VERSION;

RUN poetry --version

RUN groupadd -g 1000 ${USERNAME}
RUN useradd -u 1000 -g ${USERNAME} --create-home -d /${USERNAME} ${USERNAME}

COPY --chown=${USERNAME}:${USERNAME} ./dpschecker /${USERNAME}/dpschecker

WORKDIR ${USERNAME}
USER ${USERNAME}

RUN touch README.md
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.in-project true
RUN poetry install 

ENV PATH="/${USERNAME}/.venv/bin:$PATH"


ENTRYPOINT [ "python", "-m", "dpschecker" ]