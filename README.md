# API de Reserva de Salas de Estudo

Este projeto tem como objetivo o desenvolvimento de uma API REST para gerenciamento de reservas de salas de estudo.

O sistema deve seguir arquitetura em camadas e respeitar regras de negócio relacionadas a cadastro, reservas, conflitos de horário e cancelamento.

A atividade foi planejada para você desenvolver aproximadamente 50% do código.

---

## Objetivo

Construir uma API capaz de:

- cadastrar usuários
- cadastrar salas
- realizar reservas
- listar reservas
- cancelar reservas
- validar conflitos de horário
- aplicar regras de limite por usuário

---

## Contexto

Uma instituição precisa organizar o uso de salas de estudo em grupo.

Cada usuário pode reservar salas por faixa de horário, mas o sistema deve impedir conflitos e controlar limites de uso.

---

## Estrutura do Projeto

A aplicação deve seguir a seguinte organização:

```text
salas_api/
├── domain/
├── schemas/
├── repositories/
├── services/
├── api/routes/
└── main.py
Entidades do Sistema
Usuario
Representa a pessoa que faz a reserva.

Campos esperados:

id
nome
email
Sala
Representa uma sala disponível para reserva.

Campos esperados:

id
nome
capacidade
bloco
Reserva
Representa uma reserva realizada por um usuário para uma sala.

Campos esperados:

id
usuario_id
sala_id
data
hora_inicio
hora_fim
status
Status possíveis da reserva
A reserva pode assumir os seguintes estados:

active
canceled
finished
Regras de Negócio
1. Cadastro de usuário
não permitir email duplicado
nome e email são obrigatórios
2. Cadastro de sala
capacidade deve ser maior que zero
nome da sala deve ser obrigatório
3. Criação da reserva
não pode reservar sala para horário passado
hora final deve ser maior que hora inicial
a mesma sala não pode ter reservas com sobreposição de horário na mesma data
o mesmo usuário não pode ter duas reservas com sobreposição de horário na mesma data
um usuário pode ter no máximo 2 reservas ativas por dia
a duração máxima de uma reserva é de 2 horas
4. Cancelamento
apenas reservas com status active podem ser canceladas
reservas já canceladas não podem ser canceladas novamente
reservas finalizadas não podem ser canceladas
5. Finalização
apenas reservas ativas podem ser finalizadas
uma reserva só pode ser finalizada após o horário de término
O que o aluno deve desenvolver
O aluno deve completar:

validações de negócio
implementações nos services
integração entre rota e service
regras de conflito de horário
regras de transição de status
respostas esperadas da API
