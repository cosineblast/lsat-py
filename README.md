
# O que é isso

Este projeto é um pequeno estudo no desenvolvimento do problema de satisfabilidade para a
[lógica de Łukasiewicz](https://en.wikipedia.org/wiki/%C5%81ukasiewicz_logic).

Ele usa o programa de resolução de constraints inteiras [SCIP](https://scipopt.org/) para isto.

## Executando o Projeto

Você precisará do projeto `scip` versão 0.9.1 instalado em seu sistema para executar este projeto.

Utilize um `venv` python da seguinte forma:

```
python3 -m venv env
pip install -r requirements.txt
. env/bin/activate
python3 src/lsat.py
```

