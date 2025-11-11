# MPU-6050 — Sensores na BitDogLab

**Dupla:** Vinicius Ventura Andreossi (195125 / @viniandrs), João Pedro Schultz Oliveira (206484 / @jpschultzoliveira)  
**Turma:** EA801 — 2025S2  
**Repositório:** https://github.com/viniandrs/sensor_mpu6050_ventura_schultz

## 1. Descrição do sensor
- Fabricante / modelo: TDK InvenSense / MPU-6050
- Princípio de funcionamento: É uma Unidade de Medição Inercial (IMU) de 6 eixos, que combina um giroscópio de 3 eixos (para medir velocidade angular) e um acelerômetro de 3 eixos (para medir aceleração linear) em um único chip. Ambos os sensores são digitalizados internamente por conversores Analógico-Digital (ADC) de 16 bits. O MPU-6050 também contém um "Digital Motion Processor" (DMP) capaz de processar algoritmos complexos de fusão de sensores.
- Tensão/consumo típicos: 2.375V a 3.46V / 3.8mA (Modo de operação total, com giroscópio e acelerômetro ativos).
- Faixa de medição / resolução: 

    Giroscópio: Faixa programável de ±250, ±500, ±1000 ou ±2000 graus por segundo (dps).

    Acelerômetro: Faixa programável de ±2g, ±4g, ±8g ou ±16g.

    Resolução: 16 bits para ambos os sensores. A sensibilidade (LSB) depende da faixa selecionada:

    Acelerômetro: Varia de 16384 LSB/g (na faixa de ±2g) a 2048 LSB/g (na faixa de ±16g).

    Giroscópio: Varia de 131 LSB/°/s (na faixa de ±250°/s) a 16.4 LSB/°/s (na faixa de ±2000°/s).
- Datasheet (URL): https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf

## 2. Conexões de hardware
- Tabela indicando as conexões entre BitDogLab e sensor:
- Observações (resistores, alimentação externa, níveis lógicos):

**Tabela de conexões (imagem em `docs/`):**  
![Conexões MPU-6050](https://github.com/viniandrs/sensor_mpu6050_ventura_schultz/blob/main/docs/tabela_conexoes_mpu6050.png)

**Observações:**

Níveis Lógicos: O sensor MPU-6050 opera com VDD entre 2.375V e 3.46V. O pino VLOGIC define os níveis de tensão da interface I²C. Para garantir compatibilidade com a Raspberry Pi Pico (que opera em 3.3V), ambos VDD e VLOGIC do sensor são conectados ao pino 3V3 da BitDogLab.

Endereço I²C: O pino ADO é conectado ao GND para definir o endereço I²C do escravo como 0x68. Se fosse conectado ao 3V3, o endereço seria 0x69.

Resistores de Pull-Up: A comunicação I²C exige resistores de pull-up nas linhas SDA e SCL. Estamos assumindo o uso de um módulo MPU-6050 (como o GY-521) que já inclui esses resistores (geralmente 10kΩ ou 4.7kΩ) na placa do módulo. Se o chip MPU-6050 estivesse sendo usado diretamente, seria necessário adicionar resistores de pull-up externos (ex: 4.7kΩ) ligados ao 3V3.

Conector: A conexão foi realizada no conector I2C 0 (J6) da BitDogLab.


## 3. Dependências
- MicroPython/C versão:
- Bibliotecas utilizadas:
- Como instalar (passo a passo):

## 4. Como executar
```bash
# MicroPython (Thonny): copiar src/main.py para a placa e rodar
# C (Pico SDK): ver docs/compilacao.md
```

## 5. Exemplos de uso
- `src/exemplo_basico.py` — leitura bruta  
- `src/exemplo_filtrado.py` — leitura com média móvel  
- `test/` — códigos de teste com instruções  

## 6. Resultados e validação
- Prints/plots, fotos do setup, limitações, ruídos, dicas.

## 7. Licença
- Ver arquivo `LICENSE`.

---

> **Checklist de entrega**
> - [ ] README preenchido  
> - [ ] Foto/diagrama em `docs/`  
> - [ ] Código comentado em `src/`  
> - [ ] Testes em `test/` com instruções  
> - [ ] `relatorio.md` com lições aprendidas

## 📁 7. Estrutura do Repositório

O projeto segue o padrão definido pela disciplina EA801 — Sistemas Embarcados, 
visando padronizar as entregas e facilitar o reuso dos códigos e documentação.

Todos os arquivos de código devem estar em src/.
Diagramas, fotos, gráficos e documentos vão em docs/.
Scripts ou logs de teste ficam em test/.
O relatório técnico (relatorio.md) documenta todo o processo de engenharia.

Mantenha os nomes dos arquivos em minúsculas, sem acentos ou espaços, usando _ ou -.

```text
template_sensor/
├── README.md          → Descrição completa do projeto (sensor, ligações, execução e checklist)
├── relatorio.md       → Relatório técnico da dupla (resultados, análise e conclusões)
├── LICENSE            → Licença MIT de uso e distribuição
├── .gitignore         → Regras para ignorar arquivos temporários e binários
│
├── docs/              → Documentação e mídias
│   ├── ligacao.jpg    → Diagrama ou foto da ligação na BitDogLab
│   ├── esquema.pdf    → Esquemático opcional
│   └── outros arquivos de apoio
│
├── src/               → Códigos-fonte principais
│   ├── main.py        → Código principal (MicroPython)
│   ├── main.c         → Versão alternativa (C / Pico SDK)
│   ├── exemplos/      → Códigos ilustrativos adicionais
│   └── bibliotecas/   → Drivers, módulos auxiliares
│
└── test/              → Testes e validações
    ├── test_basico.py → Teste de leitura e resposta do sensor
    ├── test_ruido.py  → Avaliação de ruído ou estabilidade
    └── logs/          → Registros experimentais, dados e gráficos

```
