
---

# README - Sistema de Gerenciamento de Filas de Atendimento Hospitalar

## Introdução
Este sistema foi desenvolvido como parte da disciplina de Estruturas de Dados Avançadas, no curso de Ciência da Computação e contém a contribuição de @Levi Gabriel, @Sávio Rosa e @Lucas Freitas. Ele simula a gestão de filas de atendimento em um hospital, utilizando Heaps Binomiais para organizar pacientes em filas prioritárias e não prioritárias. O sistema gerencia a chegada de novos pacientes, o atendimento dos pacientes em consultórios, e a redistribuição de pacientes quando um consultório é fechado.

## Anotações Utilizadas no Arquivo de Saída

### "INC P 5 - 1"
- **Significado:** Esta anotação indica que um paciente prioritário com prioridade 5 foi inserido no consultório 1.
- **Detalhe:** "INC" é a abreviação de "inclusão". "P" indica que o paciente é prioritário, "5" refere-se à prioridade do paciente (em uma escala de 1 a 5), e "1" é o ID do consultório onde o paciente foi incluído.

### "INC N 3 - 2"
- **Significado:** Esta anotação indica que um paciente não prioritário com prioridade 3 foi inserido no consultório 2.
- **Detalhe:** "INC" é a abreviação de "inclusão". "N" indica que o paciente não é prioritário, "3" refere-se à prioridade do paciente, e "2" é o ID do consultório onde o paciente foi incluído.

### "ATT 1 - 1"
- **Significado:** Esta anotação indica que o paciente com ID 1 foi atendido no consultório 1.
- **Detalhe:** "ATT" é a abreviação de "atendimento". O número "1" que segue "ATT" é o ID do paciente que foi atendido, e o segundo "1" é o ID do consultório onde o atendimento ocorreu.

### "Redistribuindo paciente prioritário 2 do consultório fechado para o consultório 3"
- **Significado:** Esta mensagem indica que o paciente prioritário com ID 2 foi redistribuído para o consultório 3 após o fechamento de um consultório.
- **Detalhe:** Quando um consultório é fechado, seus pacientes são redistribuídos entre os consultórios restantes. Essa mensagem específica refere-se à transferência de um paciente prioritário.

### "Paciente 1 foi atendido no consultório 1."
- **Significado:** Esta mensagem indica que o paciente com ID 1 foi atendido no consultório 1.
- **Detalhe:** Essa saída é gerada quando um paciente é retirado da fila e atendido, confirmando que o atendimento foi realizado.

### "O próximo paciente a ser atendido será 2."
- **Significado:** Esta mensagem indica que o próximo paciente a ser atendido no consultório é o paciente com ID 2.
- **Detalhe:** Esta mensagem é exibida após o atendimento de um paciente para informar ao operador do sistema qual será o próximo paciente a ser atendido.

### "Erro: O consultório 1 não existe. Por favor, adicione o paciente em um consultório existente."
- **Significado:** Esta mensagem de erro é exibida quando se tenta adicionar um paciente a um consultório inexistente.
- **Detalhe:** Garante que o sistema não permita a inserção de pacientes em consultórios que não foram previamente abertos.

## Uso e Execução
Para executar o sistema, basta rodar o arquivo principal em Python. A interação com o sistema é feita via menu no terminal, onde o usuário pode escolher entre as diversas operações disponíveis, como adicionar pacientes, atender pacientes, abrir ou fechar consultórios, e exibir o status atual das filas de atendimento.

O histórico das operações realizadas pode ser salvo em um arquivo `historico.txt` para consulta futura.

---

