FROM python:3.10.10-slim AS builder
WORKDIR /build/
RUN pip3 install "poetry==1.4.0"
COPY pyproject.toml poetry.lock README.md ./
COPY ragavan ./ragavan
RUN poetry config virtualenvs.create false
RUN poetry build

FROM python:3.10.10-slim AS runner
WORKDIR /root/
COPY --from=builder /build/dist/ragavan-*-py3-none-any.whl ./
RUN pip3 install ragavan-*-py3-none-any.whl
EXPOSE 8050
CMD ["ragavan"]
