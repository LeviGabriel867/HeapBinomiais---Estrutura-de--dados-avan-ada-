class BinomialHeapNode:
    def __init__(self, key, patient_id):
        self.key = key  # Prioridade do paciente
        self.patient_id = patient_id  # ID do paciente
        self.parent = None
        self.child = None
        self.sibling = None
        self.degree = 0

    def __str__(self):
        return f"Paciente ID: {self.patient_id}, Prioridade: {self.key}"

    def __repr__(self):
        return self.__str__()

    def print_node(self, level=0):
        print(' ' * level * 2, f"Paciente {self.patient_id} com prioridade {self.key}")
        if self.child:
            self.child.print_node(level + 1)
        if self.sibling:
            self.sibling.print_node(level)



class BinomialHeap:
    def __init__(self):
        self.head = None

    def merge(self, h1, h2):
        if not h1:
            return h2
        if not h2:
            return h1

        if h1.degree <= h2.degree:
            h1.sibling = self.merge(h1.sibling, h2)
            return h1
        else:
            h2.sibling = self.merge(h1, h2.sibling)
            return h2

    def union(self, other_heap):
        if not self.head:
            return other_heap
        if not other_heap.head:
            return self

        new_heap = BinomialHeap()
        new_heap.head = self.merge(self.head, other_heap.head)

        if not new_heap.head:
            return new_heap

        prev = None
        current = new_heap.head
        next = current.sibling

        while next:
            if (current.degree != next.degree) or (next.sibling and next.sibling.degree == current.degree):
                prev = current
                current = next
            else:
                if current.key >= next.key:  # Alterado para maior prioridade primeiro
                    current.sibling = next.sibling
                    self.link(next, current)
                else:
                    if not prev:
                        new_heap.head = next
                    else:
                        prev.sibling = next
                    self.link(current, next)
                    current = next
            next = current.sibling

        return new_heap

    def link(self, y, z):
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def insert(self, node):
        new_heap = BinomialHeap()
        new_heap.head = node
        self.head = self.union(new_heap).head

    def extract_max(self):  # Alterado para extrair o paciente com maior prioridade
        if not self.head:
            return None

        prev_max = None
        max_node = self.head
        prev = None
        current = self.head

        while current.sibling:
            if current.sibling.key > max_node.key:  # Alterado para maior prioridade primeiro
                prev_max = current
                max_node = current.sibling
            current = current.sibling

        if prev_max:
            prev_max.sibling = max_node.sibling
        else:
            self.head = max_node.sibling

        child = max_node.child
        new_heap = BinomialHeap()

        while child:
            next = child.sibling
            child.sibling = new_heap.head
            new_heap.head = child
            child = next

        self.head = self.union(new_heap).head
        return max_node


class Consultorio:
    def __init__(self, id):
        self.id = id
        self.fila_prioritaria = BinomialHeap()
        self.fila_nao_prioritaria = BinomialHeap()

    def inserir_paciente(self, prioridade, patient_id, prioritario):
        if prioridade < 1 or prioridade > 5:
            print(f"Erro: A prioridade deve estar entre 1 e 5. Prioridade fornecida: {prioridade}")
            return
        
        new_node = BinomialHeapNode(prioridade, patient_id)
        if prioritario:
            print(f"Inserindo paciente prioritário {patient_id} na fila do consultório {self.id}")
            self.fila_prioritaria.insert(new_node)
        else:
            print(f"Inserindo paciente não prioritário {patient_id} na fila do consultório {self.id}")
            self.fila_nao_prioritaria.insert(new_node)
        self.debug_print_heap(self.fila_prioritaria, "Prioritária")
        self.debug_print_heap(self.fila_nao_prioritaria, "Não Prioritária")

    def atender_paciente(self):
        if self.fila_prioritaria.head:
            return self.fila_prioritaria.extract_max()
        elif self.fila_nao_prioritaria.head:
            return self.fila_nao_prioritaria.extract_max()
        return None

    def debug_print_heap(self, heap, label):
        print(f"Status da Fila {label}:")
        if heap.head:
            heap.head.print_node()
        else:
            print("Vazia")

class CentralHospitalar:
    def __init__(self):
        self.consultorios = {1: Consultorio(1), 2: Consultorio(2), 3: Consultorio(3)}
        self.historico = []

    def chegada_paciente(self, prioridade, patient_id, consultorio_id, prioritario):
        if consultorio_id in self.consultorios:
            self.consultorios[consultorio_id].inserir_paciente(prioridade, patient_id, prioritario)
            self.historico.append(f"INC {'P' if prioritario else 'N'} {prioridade} - {consultorio_id}")
        else:
            print(f"Erro: O consultório {consultorio_id} não existe. Por favor, adicione o paciente em um consultório existente.")

    def atendimento_paciente(self, consultorio_id):
        if consultorio_id in self.consultorios:
            consultorio = self.consultorios[consultorio_id]
            paciente_atendido = consultorio.atender_paciente()
            if paciente_atendido:
                self.historico.append(f"ATT {paciente_atendido.patient_id} - {consultorio_id}")
                print(f"Paciente {paciente_atendido.patient_id} foi atendido no consultório {consultorio_id}.")
                
                # Verifica qual seria o próximo paciente, sem removê-lo da fila
                proximo_paciente_prioritario = consultorio.fila_prioritaria.head
                proximo_paciente_nao_prioritario = consultorio.fila_nao_prioritaria.head
                
                if proximo_paciente_prioritario:
                    print(f"O próximo paciente a ser atendido será {proximo_paciente_prioritario.patient_id}.")
                elif proximo_paciente_nao_prioritario:
                    print(f"O próximo paciente a ser atendido será {proximo_paciente_nao_prioritario.patient_id}.")
                else:
                    print("Não há mais pacientes na fila para serem atendidos.")
            else:
                print(f"Consultório {consultorio_id} não tem pacientes para atender.")
        else:
            print(f"Erro: O consultório {consultorio_id} não existe.")

    def abrir_consultorio(self, consultorio_id):
        if consultorio_id not in self.consultorios:
            self.consultorios[consultorio_id] = Consultorio(consultorio_id)
            print(f"Consultório {consultorio_id} foi aberto.")
        else:
            print(f"Consultório {consultorio_id} já está aberto.")

    def fechar_consultorio(self, consultorio_id):
        if consultorio_id in self.consultorios:
            if len(self.consultorios) > 3:
                consultorio = self.consultorios.pop(consultorio_id)
                self.redistribuir_pacientes(consultorio)
                print(f"Consultório {consultorio_id} foi fechado e os pacientes foram redistribuídos.")
            else:
                print("Erro: Não é possível fechar o consultório. Devem permanecer pelo menos três consultórios abertos.")
        else:
            print(f"Erro: O consultório {consultorio_id} não existe.")

    def redistribuir_pacientes(self, consultorio):
        for id, other_consultorio in self.consultorios.items():
            while consultorio.fila_prioritaria.head:
                node = consultorio.fila_prioritaria.extract_max()  # Atualizado para usar extract_max
                print(f"Redistribuindo paciente prioritário {node.patient_id} do consultório fechado para o consultório {id}")
                other_consultorio.inserir_paciente(node.key, node.patient_id, True)

        for id, other_consultorio in self.consultorios.items():
            while consultorio.fila_nao_prioritaria.head:
                node = consultorio.fila_nao_prioritaria.extract_max()  # Atualizado para usar extract_max
                print(f"Redistribuindo paciente não prioritário {node.patient_id} do consultório fechado para o consultório {id}")
                other_consultorio.inserir_paciente(node.key, node.patient_id, False)

    def exibir_status(self):
        print("Status dos Consultórios:")
        for id, consultorio in self.consultorios.items():
            print(f"\nConsultório {id}:")
            if consultorio.fila_prioritaria.head:
                print("  Fila Prioritária:")
                self._print_fila(consultorio.fila_prioritaria.head)
            else:
                print("  Fila Prioritária: Vazia")

            if consultorio.fila_nao_prioritaria.head:
                print("  Fila Não Prioritária:")
                self._print_fila(consultorio.fila_nao_prioritaria.head)
            else:
                print("  Fila Não Prioritária: Vazia")

    def _print_fila(self, node, level=0):
        if node:
            print(' ' * (level * 2) + f"Paciente ID: {node.patient_id}, Prioridade: {node.key}")
            if node.child:
                self._print_fila(node.child, level + 1)
            if node.sibling:
                self._print_fila(node.sibling, level)


def main():
    central = CentralHospitalar()
    while True:
        print("\nMenu:")
        print("1. Chegada de um novo paciente")
        print("2. Atendimento de um paciente")
        print("3. Abertura de um novo consultório")
        print("4. Fechamento de um consultório")
        print("5. Exibir status dos consultórios")
        print("6. Gerar histórico")
        print("7. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            prioridade = int(input("Digite a prioridade (1-5): "))
            patient_id = int(input("Digite o ID do paciente: "))
            consultorio_id = int(input("Digite o ID do consultório: "))
            prioritario = input("Paciente prioritário? (s/n): ").lower() == 's'
            central.chegada_paciente(prioridade, patient_id, consultorio_id, prioritario)
        elif escolha == "2":
            consultorio_id = int(input("Digite o ID do consultório para o atendimento: "))
            central.atendimento_paciente(consultorio_id)
        elif escolha == "3":
            consultorio_id = int(input("Digite o ID do novo consultório: "))
            central.abrir_consultorio(consultorio_id)
        elif escolha == "4":
            consultorio_id = int(input("Digite o ID do consultório a ser fechado: "))
            central.fechar_consultorio(consultorio_id)
        elif escolha == "5":
            central.exibir_status()
        elif escolha == "6":
            with open("historico.txt", "w") as file:
                for entry in central.historico:
                    file.write(entry + "\n")
            print("Histórico gerado no arquivo 'historico.txt'.")
        elif escolha == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
